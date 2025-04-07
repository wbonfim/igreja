# Minister360 - Sistema de Gerenciamento para Igrejas

Sistema web completo para administração de igrejas, desenvolvido com Django seguindo as melhores práticas de desenvolvimento.

## 🚀 Principais Funcionalidades

- Cadastro e gestão de membros
- Controle financeiro completo
- Organização de eventos e atividades
- Geração de relatórios e painéis
- Suporte a múltiplas igrejas com separação de dados

## 🛠️ Tecnologias Utilizadas

- Python 3.10+
- Django 4.2+
- PostgreSQL
- Docker e Docker Compose
- Nginx
- Redis

## 📋 Requisitos do Sistema

- Python 3.10 ou versão superior
- Docker e Docker Compose instalados
- Git para controle de versão

## 🔧 Configuração do Ambiente de Desenvolvimento

1. Clone o repositório:
```bash
git clone https://github.com/wbonfim/Minister360.git
cd Minister360
```

2. Crie e ative o ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

5. Execute as migrações do banco de dados:
```bash
python manage.py migrate
```

6. Crie um usuário administrador:
```bash
python manage.py createsuperuser
```

7. Inicie o servidor de desenvolvimento:
```bash
python manage.py runserver
```

## 🐳 Execução com Docker

1. Construa e inicie os containers:
```bash
docker-compose up -d --build
```

2. Aplique as migrações no banco de dados:
```bash
docker-compose exec web python manage.py migrate
```

3. Crie um usuário administrador:
```bash
docker-compose exec web python manage.py createsuperuser
```

## 📦 Organização do Projeto

```
Minister360/
├── backend/              # Aplicação principal
│   ├── apps/             # Módulos do sistema
│   │   ├── autenticacao/ # Controle de acesso
│   │   ├── membros/      # Gestão de membros
│   │   ├── financeiro/   # Controle financeiro
│   │   └── igrejas/      # Cadastro de igrejas
│   ├── config/           # Configurações do Django
│   └── manage.py         # Script de administração
├── nginx/                # Configurações do servidor web
├── docker-compose.yml    # Orquestração de containers
└── requirements.txt      # Dependências do projeto
```

## 🚀 Implantação em Produção

Para implantar em um servidor Ubuntu:

1. Execute o script de configuração:
```bash
./scripts/setup.sh
```

2. Realize o deploy da aplicação:
```bash
./scripts/deploy.sh
```

## 📄 Termos de Uso

Este projeto utiliza a licença MIT - consulte o arquivo [LICENSE.md](LICENSE.md) para mais informações

## ✨ Como Contribuir

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/NovaFuncionalidade`)
3. Faça commit das suas alterações (`git commit -m 'Adiciona nova funcionalidade'`)
4. Envie para o repositório remoto (`git push origin feature/NovaFuncionalidade`)
5. Abra um Pull Request
