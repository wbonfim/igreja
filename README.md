# Sistema de Gestão de Igrejas

Sistema multi-igreja para gestão completa de igrejas, incluindo gestão de membros, financeiro e páginas personalizadas.

## 🚀 Características

- Sistema multi-igreja com subdomínios personalizados
- 5 níveis de acesso (Visitante, Membro, Líder, Pastor, Administrador)
- Gestão completa de membros
- Controle financeiro
- Templates personalizáveis para página inicial
- Sistema de filiais
- Rastreamento de visitas entre igrejas

## 📋 Pré-requisitos

- Ubuntu 22.04
- Docker e Docker Compose
- Git

## 🔧 Instalação

1. Clone o repositório:
```bash
git clone [url-do-repositorio]
cd igreja
```

2. Execute o script de instalação:
```bash
chmod +x scripts/instalar.sh
sudo ./scripts/instalar.sh
```

3. Configure as variáveis de ambiente:
```bash
cd backend
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

## 🛠️ Desenvolvimento

### Configuração do Ambiente de Desenvolvimento

1. Instale as extensões recomendadas do VS Code:
   - Abra o VS Code
   - Vá para a aba de extensões
   - Digite `@recommended` na busca
   - Instale todas as extensões recomendadas

2. Instale os hooks do pre-commit:
```bash
cd backend
pre-commit install
```

### Comandos Úteis

Você pode usar o Makefile ou as tarefas do VS Code para executar comandos comuns:

#### Usando Makefile:
```bash
# Iniciar o projeto
make docker-up

# Executar testes
make docker-test

# Aplicar migrações
make docker-migrate

# Criar superusuário
make docker-createsuperuser

# Formatar código
make format

# Verificar código
make lint
```

#### Usando VS Code:
- Pressione `Ctrl+Shift+P`
- Digite "Tasks: Run Task"
- Escolha a tarefa desejada

### Debugging

O projeto está configurado para debugging no VS Code:

1. Inicie o servidor com o debugger:
   - Pressione F5 ou use o menu de Debug
   - Escolha "Django: Docker"

2. Para debuggar testes:
   - Abra o arquivo de teste
   - Use "Python: Debug Tests"

## 📦 Estrutura do Projeto

```
igreja/
├── backend/
│   ├── apps/
│   │   ├── autenticacao/
│   │   ├── igrejas/
│   │   ├── membros/
│   │   └── financeiro/
│   ├── config/
│   └── scripts/
├── nginx/
│   └── conf.d/
└── docker-compose.yml
```

## 🔍 Testes

```bash
# Executar todos os testes
make docker-test

# Executar testes com cobertura
make docker-test-cov
```

## 📝 Convenções de Código

- Usamos Black para formatação
- Isort para ordenação de imports
- Flake8 para linting
- MyPy para verificação de tipos
- Pre-commit hooks para garantir qualidade do código

## 🚀 Deployment

### Configuração Inicial

1. Configure seu DNS para apontar *.integramax.app.br para o IP do servidor

2. Instalação automatizada:
```bash
sudo ./scripts/instalar.sh
```

3. Configuração SSL automatizada:
```bash
sudo ./scripts/ssl-setup.sh install
```

### Opções de Deploy

**Deploy manual:**
```bash
docker-compose -f docker-compose.prod.yml up -d
```

**Deploy automatizado (recomendado):**
```bash
sudo ./scripts/deploy.sh full
```

**Atualizações parciais:**
```bash
# Apenas atualizar código
sudo ./scripts/deploy.sh update-code

# Apenas atualizar dependências
sudo ./scripts/deploy.sh update-deps

# Apenas aplicar migrações
sudo ./scripts/deploy.sh migrate
```

### Monitoramento

O sistema inclui monitoramento automático com:
```bash
# Verificar status do sistema
sudo ./scripts/monitor.sh all

# Verificar certificados SSL
sudo ./scripts/monitor.sh ssl

# Verificar backups
sudo ./scripts/monitor.sh backup
```

### Backup e Restauração

**Backup manual:**
```bash
sudo ./scripts/backup.sh backup
```

**Restauração:**
```bash
sudo ./scripts/backup.sh restore [arquivo_backup]
```

**Backup automático:**
Os backups são realizados automaticamente todos os dias às 2:00 AM

## 📚 Módulos

### Autenticação
- Sistema de login
- Gerenciamento de níveis de acesso
- Recuperação de senha

### Igrejas
- Cadastro de igrejas
- Gestão de filiais
- Templates personalizáveis
- Configurações específicas por igreja

### Membros
- Cadastro completo de membros
- Histórico de visitas
- Ministérios
- Carteirinha de membro
- Relatórios

### Financeiro
- Controle de entradas e saídas
- Categorias financeiras
- Relatórios mensais e anuais
- Dashboard financeiro
- Contas bancárias

## 🔒 Segurança

- Isolamento de dados por igreja
- SSL/TLS para todas as conexões
- Autenticação JWT
- Logs de atividades
- Backup automático

## 🔄 Gerenciamento do Sistema

### Scripts Disponíveis

| Script | Descrição | Comandos |
|--------|-----------|----------|
| `instalar.sh` | Instalação completa do sistema | `sudo ./scripts/instalar.sh` |
| `deploy.sh` | Gerenciamento de deployments | `full`, `update-code`, `update-deps`, `migrate`, `static`, `restart`, `rollback` |
| `backup.sh` | Backup e restauração | `backup`, `restore`, `list` |
| `monitor.sh` | Monitoramento do sistema | `all`, `docker`, `disk`, `memory`, `cpu`, `logs`, `backup`, `ssl`, `clean` |
| `ssl-setup.sh` | Gerenciamento de certificados SSL | `install`, `renew`, `force-renew`, `check`, `test` |

### Configuração Automatizada

O sistema inclui:

- Renovação automática de certificados SSL
- Monitoramento contínuo de recursos
- Backup diário automático
- Notificações por email em caso de problemas

## 📄 Licença

Este projeto está licenciado sob [tipo de licença].

## ✨ Contribuição

1. Fork o projeto
2. Crie sua branch de feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 🤝 Suporte

Para suporte, entre em contato através de [email/contato].
