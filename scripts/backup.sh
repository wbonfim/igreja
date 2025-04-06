#!/bin/bash

# Configurações
BACKUP_DIR="/var/www/igreja/backups"
KEEP_DAYS=30
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="backup_${DATE}.sql.gz"

# Função para exibir mensagens
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

# Função para fazer backup
do_backup() {
    log "Iniciando backup do banco de dados..."

    # Cria diretório de backup se não existir
    mkdir -p "$BACKUP_DIR"

    # Realiza o backup
    docker-compose exec -T db pg_dump -U "$DB_USER" "$DB_NAME" | gzip > "$BACKUP_DIR/$BACKUP_FILE"

    if [ $? -eq 0 ]; then
        log "Backup realizado com sucesso: $BACKUP_FILE"
        # Remove backups antigos
        find "$BACKUP_DIR" -type f -name "backup_*.sql.gz" -mtime +$KEEP_DAYS -delete
        log "Backups mais antigos que $KEEP_DAYS dias foram removidos"
    else
        log "ERRO: Falha ao realizar backup"
        exit 1
    fi
}

# Função para restaurar backup
restore_backup() {
    if [ -z "$1" ]; then
        log "ERRO: Arquivo de backup não especificado"
        log "Uso: $0 restore <arquivo_backup>"
        exit 1
    fi

    RESTORE_FILE="$1"

    if [ ! -f "$RESTORE_FILE" ]; then
        log "ERRO: Arquivo de backup não encontrado: $RESTORE_FILE"
        exit 1
    }

    log "Iniciando restauração do backup: $RESTORE_FILE"

    # Para os serviços
    docker-compose stop backend

    # Restaura o backup
    gunzip -c "$RESTORE_FILE" | docker-compose exec -T db psql -U "$DB_USER" "$DB_NAME"

    if [ $? -eq 0 ]; then
        log "Backup restaurado com sucesso"
        # Reinicia os serviços
        docker-compose start backend
    else
        log "ERRO: Falha ao restaurar backup"
        # Reinicia os serviços mesmo em caso de erro
        docker-compose start backend
        exit 1
    fi
}

# Função para listar backups
list_backups() {
    log "Backups disponíveis:"
    ls -lh "$BACKUP_DIR"/*.sql.gz 2>/dev/null || echo "Nenhum backup encontrado"
}

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
    backup)
        do_backup
        ;;
    restore)
        restore_backup "$2"
        ;;
    list)
        list_backups
        ;;
    *)
        echo "Uso: $0 {backup|restore|list}"
        echo "  backup             - Realiza backup do banco de dados"
        echo "  restore <arquivo>  - Restaura backup específico"
        echo "  list              - Lista backups disponíveis"
        exit 1
        ;;
esac

exit 0
