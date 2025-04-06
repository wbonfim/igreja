#!/bin/bash

# Configurações
DEPLOY_DIR="/var/www/igreja"
BACKUP_DIR="$DEPLOY_DIR/backups"
LOG_DIR="$DEPLOY_DIR/logs"
BRANCH="main"
REPO_URL="[seu-repositorio-git]"

# Função para exibir mensagens
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_DIR/deploy.log"
}

# Função para verificar erro
check_error() {
    if [ $? -ne 0 ]; then
        log "ERRO: $1"
        exit 1
    fi
}

# Função para fazer backup antes do deploy
pre_deploy_backup() {
    log "Realizando backup antes do deploy..."

    # Cria diretório de backup se não existir
    mkdir -p "$BACKUP_DIR"

    # Nome do arquivo de backup
    BACKUP_FILE="$BACKUP_DIR/pre_deploy_$(date +%Y%m%d_%H%M%S).sql.gz"

    # Realiza o backup
    docker-compose exec -T db pg_dump -U "$DB_USER" "$DB_NAME" | gzip > "$BACKUP_FILE"
    check_error "Falha ao realizar backup"

    log "Backup realizado com sucesso: $BACKUP_FILE"
}

# Função para atualizar código
update_code() {
    log "Atualizando código..."

    # Verifica se é uma instalação nova ou atualização
    if [ -d "$DEPLOY_DIR/.git" ]; then
        # Atualização
        cd "$DEPLOY_DIR"
        git fetch origin
        git reset --hard "origin/$BRANCH"
        check_error "Falha ao atualizar código"
    else
        # Instalação nova
        git clone -b "$BRANCH" "$REPO_URL" "$DEPLOY_DIR"
        check_error "Falha ao clonar repositório"
    fi

    log "Código atualizado com sucesso"
}

# Função para atualizar dependências
update_dependencies() {
    log "Atualizando dependências..."

    # Reconstrói os containers com as novas dependências
    docker-compose -f docker-compose.prod.yml build
    check_error "Falha ao construir containers"

    log "Dependências atualizadas com sucesso"
}

# Função para aplicar migrações
apply_migrations() {
    log "Aplicando migrações..."

    docker-compose -f docker-compose.prod.yml exec -T backend python manage.py migrate --noinput
    check_error "Falha ao aplicar migrações"

    log "Migrações aplicadas com sucesso"
}

# Função para coletar arquivos estáticos
collect_static() {
    log "Coletando arquivos estáticos..."

    docker-compose -f docker-compose.prod.yml exec -T backend python manage.py collectstatic --noinput
    check_error "Falha ao coletar arquivos estáticos"

    log "Arquivos estáticos coletados com sucesso"
}

# Função para reiniciar serviços
restart_services() {
    log "Reiniciando serviços..."

    docker-compose -f docker-compose.prod.yml down
    docker-compose -f docker-compose.prod.yml up -d
    check_error "Falha ao reiniciar serviços"

    log "Serviços reiniciados com sucesso"
}

# Função para verificar saúde do sistema
check_health() {
    log "Verificando saúde do sistema..."

    # Aguarda o sistema iniciar
    sleep 10

    # Verifica se os serviços estão rodando
    docker-compose -f docker-compose.prod.yml ps | grep -q "Exit"
    if [ $? -eq 0 ]; then
        log "ERRO: Alguns serviços não estão rodando"
        exit 1
    fi

    # Verifica se a API está respondendo
    curl -f http://localhost:8000/health/
    check_error "API não está respondendo"

    log "Sistema está saudável"
}

# Função para reverter deploy em caso de erro
rollback() {
    log "ERRO: Iniciando rollback..."

    # Restaura backup
    BACKUP_FILE=$(ls -t "$BACKUP_DIR"/pre_deploy_*.sql.gz | head -n1)
    if [ -f "$BACKUP_FILE" ]; then
        log "Restaurando backup: $BACKUP_FILE"
        gunzip -c "$BACKUP_FILE" | docker-compose exec -T db psql -U "$DB_USER" "$DB_NAME"
    fi

    # Reinicia serviços
    docker-compose -f docker-compose.prod.yml down
    docker-compose -f docker-compose.prod.yml up -d

    log "Rollback concluído"
    exit 1
}

# Cria diretórios necessários
mkdir -p "$LOG_DIR"

# Verifica se as variáveis de ambiente necessárias estão definidas
if [ -z "$DB_USER" ] || [ -z "$DB_NAME" ]; then
    if [ -f .env ]; then
        export $(cat .env | grep -v '^#' | xargs)
    else
        log "ERRO: Arquivo .env não encontrado"
        exit 1
    fi
fi

# Menu principal
case "$1" in
    full)
        pre_deploy_backup
        update_code
        update_dependencies
        apply_migrations
        collect_static
        restart_services
        check_health
        ;;
    update-code)
        update_code
        restart_services
        check_health
        ;;
    update-deps)
        update_dependencies
        restart_services
        check_health
        ;;
    migrate)
        apply_migrations
        ;;
    static)
        collect_static
        ;;
    restart)
        restart_services
        check_health
        ;;
    rollback)
        rollback
        ;;
    *)
        echo "Uso: $0 {full|update-code|update-deps|migrate|static|restart|rollback}"
        echo "  full        - Deploy completo"
        echo "  update-code - Atualiza apenas o código"
        echo "  update-deps - Atualiza dependências"
        echo "  migrate     - Aplica migrações"
        echo "  static      - Coleta arquivos estáticos"
        echo "  restart     - Reinicia serviços"
        echo "  rollback    - Reverte última implantação"
        exit 1
        ;;
esac

log "Deploy concluído com sucesso!"
exit 0
