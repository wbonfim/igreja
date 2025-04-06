.PHONY: help install run test lint format migrate makemigrations shell createsuperuser collectstatic clean

help:
	@echo "Comandos disponíveis:"
	@echo "  install        - Instala as dependências do projeto"
	@echo "  run           - Inicia o servidor de desenvolvimento"
	@echo "  test          - Executa os testes"
	@echo "  lint          - Executa verificação de código"
	@echo "  format        - Formata o código"
	@echo "  migrate       - Aplica as migrações"
	@echo "  makemigrations- Cria novas migrações"
	@echo "  shell         - Inicia o shell do Django"
	@echo "  createsuperuser- Cria um superusuário"
	@echo "  collectstatic - Coleta arquivos estáticos"
	@echo "  clean         - Remove arquivos temporários"

install:
	pip install -r requirements.txt

run:
	python manage.py runserver 0.0.0.0:8000

test:
	pytest

lint:
	flake8 .
	black . --check
	isort . --check-only

format:
	black .
	isort .

migrate:
	python manage.py migrate

makemigrations:
	python manage.py makemigrations

shell:
	python manage.py shell

createsuperuser:
	python manage.py createsuperuser

collectstatic:
	python manage.py collectstatic --noinput

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "*.egg" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type d -name ".tox" -exec rm -rf {} +
	find . -type d -name "dist" -exec rm -rf {} +
	find . -type d -name "build" -exec rm -rf {} +

docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

docker-shell:
	docker-compose exec backend bash

docker-test:
	docker-compose exec backend pytest

docker-migrate:
	docker-compose exec backend python manage.py migrate

docker-makemigrations:
	docker-compose exec backend python manage.py makemigrations

docker-createsuperuser:
	docker-compose exec backend python manage.py createsuperuser

docker-collectstatic:
	docker-compose exec backend python manage.py collectstatic --noinput

docker-clean:
	docker-compose down -v
	docker system prune -f
