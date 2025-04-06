#!/bin/bash

# Verifica se o certbot está instalado
if ! command -v certbot &> /dev/null; then
    echo "Instalando certbot..."
    apt-get update
    apt-get install -y certbot
fi

# Diretório para os certificados
CERT_DIR="/etc/nginx/ssl/live/igreja"

# Cria o diretório se não existir
mkdir -p $CERT_DIR

# Gera o certificado
echo "Gerando certificado SSL..."
certbot certonly --standalone \
    --agree-tos \
    --non-interactive \
    --email admin@example.com \
    -d 173.249.46.169 \
    --cert-name igreja

# Copia os certificados para o diretório do nginx
echo "Copiando certificados..."
cp /etc/letsencrypt/live/igreja/fullchain.pem $CERT_DIR/
cp /etc/letsencrypt/live/igreja/privkey.pem $CERT_DIR/

# Ajusta as permissões
chmod 755 $CERT_DIR
chmod 644 $CERT_DIR/fullchain.pem
chmod 644 $CERT_DIR/privkey.pem

echo "Configuração SSL concluída!"
