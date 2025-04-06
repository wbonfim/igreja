FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    netcat-openbsd \
    curl \
    gcc \
    python3-dev \
    musl-dev \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    dos2unix \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir Pillow gunicorn

# Copiar o código
COPY . .

# Converter quebras de linha para Unix e dar permissão ao script
RUN dos2unix /app/scripts/entrypoint.sh && \
    chmod +x /app/scripts/entrypoint.sh

# Criar diretórios necessários
RUN mkdir -p /app/media/igrejas/logos \
    /app/media/igrejas/backgrounds \
    /app/media/igrejas/videos \
    /app/staticfiles \
    && chmod -R 755 /app/media \
    && chmod -R 755 /app/staticfiles

EXPOSE 8000

CMD ["/bin/sh", "/app/scripts/entrypoint.sh"]
