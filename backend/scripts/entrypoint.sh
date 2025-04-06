#!/bin/sh

set -e

# Função para esperar o PostgreSQL
wait_for_postgres() {
    echo "Aguardando PostgreSQL..."
    while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
        sleep 0.1
    done
    echo "PostgreSQL iniciado"
}

# Função para esperar o Redis
wait_for_redis() {
    echo "Aguardando Redis..."
    while ! nc -z $REDIS_HOST $REDIS_PORT; do
        sleep 0.1
    done
    echo "Redis iniciado"
}

# Criar diretórios necessários
mkdir -p /app/media/igrejas/logos
mkdir -p /app/media/igrejas/backgrounds
mkdir -p /app/media/igrejas/videos
mkdir -p /app/staticfiles

# Definir permissões
chmod -R 755 /app/media
chmod -R 755 /app/staticfiles

# Esperar serviços
wait_for_postgres
wait_for_redis

# Aplicar migrações
python manage.py migrate

# Criar dados iniciais
python manage.py criar_usuario_padrao
python manage.py criar_templates_padrao
python manage.py criar_igreja_padrao

# Coletar arquivos estáticos
python manage.py collectstatic --noinput

# Iniciar Gunicorn
exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --worker-class gthread \
    --threads 4 \
    --timeout 300 \
    --reload
