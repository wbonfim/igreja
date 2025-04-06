#!/bin/bash

# Configurações
LOG_DIR="/var/www/igreja/logs"
ALERT_EMAIL="admin@example.com"
DISK_THRESHOLD=80
MEMORY_THRESHOLD=80
CPU_THRESHOLD=80

# Função para exibir mensagens
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_DIR/monitor.log"
}

# Função para enviar alertas
send_alert() {
    local subject="$1"
    local message="$2"
    echo "$message" | mail -s "$subject" "$ALERT_EMAIL"
    log "Alerta enviado: $subject"
}

# Função para verificar serviços Docker
check_docker_services() {
    log "Verificando serviços Docker..."

    services=("backend" "db" "redis" "nginx")
    for service in "${services[@]}"; do
        status=$(docker-compose ps "$service" | grep "Up")
        if [ -z "$status" ]; then
            send_alert "Serviço $service parado" "O serviço $service não está em execução."
            log "ALERTA: Serviço $service não está em execução"

            # Tenta reiniciar o serviço
            log "Tentando reiniciar $service..."
            docker-compose restart "$service"
        else
            log "Serviço $service está rodando"
        fi
    done
}

# Função para verificar uso de disco
check_disk_usage() {
    log "Verificando uso de disco..."

    usage=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')
    if [ "$usage" -gt "$DISK_THRESHOLD" ]; then
        send_alert "Disco com uso elevado" "Uso de disco: $usage%"
        log "ALERTA: Uso de disco elevado ($usage%)"
    else
        log "Uso de disco: $usage%"
    fi
}

# Função para verificar uso de memória
check_memory_usage() {
    log "Verificando uso de memória..."

    usage=$(free | awk '/Mem:/ {print int($3/$2 * 100)}')
    if [ "$usage" -gt "$MEMORY_THRESHOLD" ]; then
        send_alert "Memória com uso elevado" "Uso de memória: $usage%"
        log "ALERTA: Uso de memória elevado ($usage%)"
    else
        log "Uso de memória: $usage%"
    fi
}

# Função para verificar uso de CPU
check_cpu_usage() {
    log "Verificando uso de CPU..."

    usage=$(top -bn1 | grep "Cpu(s)" | awk '{print int($2)}')
    if [ "$usage" -gt "$CPU_THRESHOLD" ]; then
        send_alert "CPU com uso elevado" "Uso de CPU: $usage%"
        log "ALERTA: Uso de CPU elevado ($usage%)"
    else
        log "Uso de CPU: $usage%"
    fi
}

# Função para verificar logs de erro
check_error_logs() {
    log "Verificando logs de erro..."

    # Verifica logs do Django
    django_errors=$(tail -n 1000 "$LOG_DIR/django.log" | grep -i "error")
    if [ ! -z "$django_errors" ]; then
        send_alert "Erros encontrados nos logs Django" "$django_errors"
        log "ALERTA: Erros encontrados nos logs Django"
    fi

    # Verifica logs do Nginx
    nginx_errors=$(tail -n 1000 "/var/log/nginx/error.log" | grep -i "error")
    if [ ! -z "$nginx_errors" ]; then
        send_alert "Erros encontrados nos logs Nginx" "$nginx_errors"
        log "ALERTA: Erros encontrados nos logs Nginx"
    fi
}

# Função para limpar logs antigos
clean_old_logs() {
    log "Limpando logs antigos..."

    # Remove logs mais antigos que 30 dias
    find "$LOG_DIR" -type f -name "*.log" -mtime +30 -delete
    find "/var/log/nginx" -type f -name "*.log" -mtime +30 -delete

    log "Logs antigos removidos"
}

# Função para verificar backups
check_backups() {
    log "Verificando backups..."

    latest_backup=$(ls -t /var/www/igreja/backups/*.sql.gz 2>/dev/null | head -n1)
    if [ -z "$latest_backup" ]; then
        send_alert "Backup não encontrado" "Nenhum backup encontrado no sistema"
        log "ALERTA: Nenhum backup encontrado"
    else
        backup_age=$(( ( $(date +%s) - $(date -r "$latest_backup" +%s) ) / 86400 ))
        if [ "$backup_age" -gt 1 ]; then
            send_alert "Backup desatualizado" "Último backup tem $backup_age dias"
            log "ALERTA: Backup desatualizado ($backup_age dias)"
        else
            log "Backup está atualizado"
        fi
    fi
}

# Função para verificar certificados SSL
check_ssl_certificates() {
    log "Verificando certificados SSL..."

    cert_file="/etc/nginx/ssl/integramax.app.br.crt"
    if [ -f "$cert_file" ]; then
        expiry_date=$(openssl x509 -enddate -noout -in "$cert_file" | cut -d= -f2)
        expiry_epoch=$(date -d "$expiry_date" +%s)
        current_epoch=$(date +%s)
        days_left=$(( ($expiry_epoch - $current_epoch) / 86400 ))

        if [ "$days_left" -lt 30 ]; then
            send_alert "Certificado SSL próximo do vencimento" "Certificado SSL irá expirar em $days_left dias"
            log "ALERTA: Certificado SSL irá expirar em $days_left dias"
        else
            log "Certificado SSL válido por mais $days_left dias"
        fi
    else
        send_alert "Certificado SSL não encontrado" "Arquivo de certificado não existe"
        log "ALERTA: Certificado SSL não encontrado"
    fi
}

# Cria diretório de logs se não existir
mkdir -p "$LOG_DIR"

# Menu principal
case "$1" in
    all)
        check_docker_services
        check_disk_usage
        check_memory_usage
        check_cpu_usage
        check_error_logs
        check_backups
        check_ssl_certificates
        clean_old_logs
        ;;
    docker)
        check_docker_services
        ;;
    disk)
        check_disk_usage
        ;;
    memory)
        check_memory_usage
        ;;
    cpu)
        check_cpu_usage
        ;;
    logs)
        check_error_logs
        ;;
    backup)
        check_backups
        ;;
    ssl)
        check_ssl_certificates
        ;;
    clean)
        clean_old_logs
        ;;
    *)
        echo "Uso: $0 {all|docker|disk|memory|cpu|logs|backup|ssl|clean}"
        echo "  all    - Executa todas as verificações"
        echo "  docker - Verifica serviços Docker"
        echo "  disk   - Verifica uso de disco"
        echo "  memory - Verifica uso de memória"
        echo "  cpu    - Verifica uso de CPU"
        echo "  logs   - Verifica logs de erro"
        echo "  backup - Verifica backups"
        echo "  ssl    - Verifica certificados SSL"
        echo "  clean  - Limpa logs antigos"
        exit 1
        ;;
esac

exit 0
