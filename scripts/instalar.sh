#!/bin/bash

echo "Iniciando instalação do Sistema de Gestão de Igrejas"
echo "=================================================="

# Verifica se está rodando como root
if [ "$EUID" -ne 0 ]; then
    echo "Por favor, execute o script como root (sudo ./instalar.sh)"
    exit 1
fi

# Configurações
INSTALL_DIR="/var/www/igreja"
SCRIPTS_DIR="$INSTALL_DIR/scripts"
LOG_DIR="$INSTALL_DIR/logs"
BACKUP_DIR="$INSTALL_DIR/backups"

# Função para exibir mensagens
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_DIR/install.log"
}

# Função para verificar erro
check_error() {
    if [ $? -ne 0 ]; then
        log "ERRO: $1"
        exit 1
    fi
}

# Atualiza o sistema
log "Atualizando o sistema..."
apt update && apt upgrade -y
check_error "Falha ao atualizar o sistema"

# Instala dependências necessárias
log "Instalando dependências do sistema..."
apt install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
    python3 \
    python3-pip \
    python3-venv \
    postgresql \
    postgresql-contrib \
    nginx \
    git \
    build-essential \
    libpq-dev \
    python3-dev \
    netcat \
    certbot \
    python3-certbot-nginx \
    ufw \
    fail2ban \
    supervisor \
    redis-server
check_error "Falha ao instalar dependências"

# Instala Docker
log "Instalando Docker..."
if ! command -v docker &> /dev/null; then
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
      $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
    apt update
    apt install -y docker-ce docker-ce-cli containerd.io
    check_error "Falha ao instalar Docker"
fi

# Instala Docker Compose
log "Instalando Docker Compose..."
if ! command -v docker-compose &> /dev/null; then
    curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
    check_error "Falha ao instalar Docker Compose"
fi

# Configura permissões do Docker
log "Configurando permissões do Docker..."
usermod -aG docker $SUDO_USER

# Cria estrutura de diretórios
log "Criando estrutura de diretórios..."
mkdir -p "$INSTALL_DIR"/{backend,nginx,media,static,logs,backups,secrets}
mkdir -p "$INSTALL_DIR/nginx/"{conf.d,ssl,logs}
mkdir -p "$INSTALL_DIR/backend/"{staticfiles,media}

# Copia arquivos do projeto
log "Copiando arquivos do projeto..."
cp -r backend/* "$INSTALL_DIR/backend/"
cp -r nginx/conf.d/* "$INSTALL_DIR/nginx/conf.d/"
cp docker-compose*.yml "$INSTALL_DIR/"
cp -r scripts "$INSTALL_DIR/"

# Configura permissões
log "Configurando permissões..."
chown -R www-data:www-data "$INSTALL_DIR"
chmod -R 755 "$INSTALL_DIR"
chmod -R 775 "$INSTALL_DIR/backend/media"
chmod -R 775 "$INSTALL_DIR/backend/staticfiles"
chmod +x "$INSTALL_DIR/scripts/"*.sh

# Configura ambiente virtual Python
log "Configurando ambiente virtual Python..."
cd "$INSTALL_DIR/backend"
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
check_error "Falha ao instalar dependências Python"

# Configura variáveis de ambiente
log "Configurando variáveis de ambiente..."
if [ ! -f "$INSTALL_DIR/backend/.env" ]; then
    cp "$INSTALL_DIR/backend/.env.example" "$INSTALL_DIR/backend/.env"
    # Gera uma chave secreta aleatória
    SECRET_KEY=$(python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
    sed -i "s/your-secret-key-here/$SECRET_KEY/" "$INSTALL_DIR/backend/.env"
fi

# Configura banco de dados
log "Configurando banco de dados..."
if ! sudo -u postgres psql -lqt | cut -d \| -f 1 | grep -qw igreja_db; then
    sudo -u postgres psql -c "CREATE DATABASE igreja_db;"
    sudo -u postgres psql -c "CREATE USER igreja_user WITH PASSWORD 'igreja_password';"
    sudo -u postgres psql -c "ALTER ROLE igreja_user SET client_encoding TO 'utf8';"
    sudo -u postgres psql -c "ALTER ROLE igreja_user SET default_transaction_isolation TO 'read committed';"
    sudo -u postgres psql -c "ALTER ROLE igreja_user SET timezone TO 'America/Sao_Paulo';"
    sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE igreja_db TO igreja_user;"
fi

# Configura firewall
log "Configurando firewall..."
ufw allow 22
ufw allow 80
ufw allow 443
ufw --force enable

# Configura fail2ban
log "Configurando fail2ban..."
cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
systemctl enable fail2ban
systemctl start fail2ban

# Inicia e habilita serviços
log "Iniciando serviços..."
systemctl start postgresql
systemctl enable postgresql
systemctl start docker
systemctl enable docker
systemctl start nginx
systemctl enable nginx
systemctl start redis-server
systemctl enable redis-server

# Para serviços que podem conflitar
log "Parando serviços locais..."
systemctl stop nginx >/dev/null 2>&1
systemctl stop redis-server >/dev/null 2>&1
systemctl disable redis-server >/dev/null 2>&1
pkill -9 redis-server >/dev/null 2>&1

# Remove containers antigos
log "Removendo containers antigos..."
docker-compose down -v >/dev/null 2>&1

# Verifica e libera portas
log "Liberando portas necessárias..."
for port in 5432 5433 6379 6380; do
    if lsof -i :$port >/dev/null 2>&1; then
        log "Liberando porta $port..."
        fuser -k $port/tcp >/dev/null 2>&1
        sleep 2
        # Verifica se a porta foi realmente liberada
        if lsof -i :$port >/dev/null 2>&1; then
            log "ERRO: Não foi possível liberar a porta $port"
            log "Por favor, verifique manualmente os processos usando a porta $port"
            exit 1
        fi
    fi
done

# Função para encontrar porta disponível
find_available_port() {
    local start_port=$1
    local service=$2
    local port=$start_port

    while lsof -i :$port >/dev/null 2>&1; do
        log "Porta $port em uso para $service, tentando próxima..."
        port=$((port + 1))
    done
    echo $port
}

# Configura portas antes de iniciar containers
POSTGRES_PORT=$(find_available_port 5432 "PostgreSQL")
REDIS_PORT=$(find_available_port 6379 "Redis")

log "Usando porta $POSTGRES_PORT para PostgreSQL"
log "Usando porta $REDIS_PORT para Redis"

# Atualiza configurações de porta
log "Atualizando configurações de porta..."
sed -i "s/\"[0-9]\+:5432\"/\"$POSTGRES_PORT:5432\"/" docker-compose.yml
sed -i "s/\"[0-9]\+:5432\"/\"$POSTGRES_PORT:5432\"/" docker-compose.prod.yml
sed -i "s/\"[0-9]\+:6379\"/\"$REDIS_PORT:6379\"/" docker-compose.yml
sed -i "s/\"[0-9]\+:6379\"/\"$REDIS_PORT:6379\"/" docker-compose.prod.yml

# Atualiza variáveis de ambiente
if [ -f "$INSTALL_DIR/backend/.env" ]; then
    log "Atualizando variáveis de ambiente..."
    sed -i "s/DB_PORT=.*/DB_PORT=$POSTGRES_PORT/" "$INSTALL_DIR/backend/.env"
    sed -i "s/REDIS_PORT=.*/REDIS_PORT=$REDIS_PORT/" "$INSTALL_DIR/backend/.env"
fi

# Move para o diretório do projeto e inicia os containers
log "Iniciando containers Docker..."
cd "$INSTALL_DIR"
docker-compose down -v
docker-compose up -d --build

# Verifica se os containers estão rodando
log "Verificando status dos containers..."
sleep 10
if ! docker-compose ps | grep -q "Up"; then
    log "ERRO: Alguns containers não iniciaram corretamente"
    docker-compose logs
    exit 1
fi

log "Todos os serviços iniciados com sucesso nas novas portas:"
log "PostgreSQL: porta $POSTGRES_PORT"
log "Redis: porta $REDIS_PORT"

# Configura certificados SSL com fallback para autoassinado
log "Configurando certificados SSL..."
if ! "$SCRIPTS_DIR/ssl-setup.sh" install; then
    log "Atenção: Falha ao obter certificado SSL automaticamente"
    log "Gerando certificado autoassinado temporário..."
    mkdir -p nginx/ssl
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout nginx/ssl/integramax.app.br.key \
        -out nginx/ssl/integramax.app.br.crt \
        -subj "/CN=integramax.app.br"
    log "Certificado autoassinado gerado com sucesso"
    log "Você pode substituí-lo por um certificado válido posteriormente em nginx/ssl/"
fi

# Configura cron jobs
log "Configurando cron jobs..."
(crontab -l 2>/dev/null; echo "0 2 * * * $SCRIPTS_DIR/backup.sh") | crontab -
(crontab -l 2>/dev/null; echo "*/5 * * * * $SCRIPTS_DIR/monitor.sh all") | crontab -
(crontab -l 2>/dev/null; echo "0 3 * * * $SCRIPTS_DIR/ssl-setup.sh renew") | crontab -

echo "=================================================="
echo "Instalação concluída!"
echo ""
echo "Próximos passos:"
echo "1. Verifique e ajuste as configurações em $INSTALL_DIR/backend/.env"
echo "2. Configure seu DNS para apontar para este servidor"
echo "3. Acesse o sistema em: https://sua-igreja.integramax.app.br"
echo ""
echo "Para criar um superusuário, execute:"
echo "cd $INSTALL_DIR && docker-compose exec backend python manage.py createsuperuser"
echo ""
echo "Para verificar os logs, execute:"
echo "docker-compose logs -f"
echo ""
echo "Scripts disponíveis em $SCRIPTS_DIR:"
echo "- backup.sh: Gerencia backups do banco de dados"
echo "- monitor.sh: Monitora saúde do sistema"
echo "- deploy.sh: Gerencia deployments"
echo "- ssl-setup.sh: Gerencia certificados SSL"
echo "=================================================="
