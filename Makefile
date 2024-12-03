# Variables
PROJECT_NAME = Kabi
COMPOSE_FILE = devops/docker-compose.yml
SERVICES_COMPOSE_FILE = devops/docker-compose.services.yml
SERVICE_WEB = kabi-server
SERVICE_DB = db
DOCKER_EXEC_WEB = docker exec -it $(SERVICE_WEB)

# Default help target
.PHONY: help
help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  image         Build Docker images"
	@echo "  up            Start services in detached mode"
	@echo "  down          Stop services"
	@echo "  restart       Restart all services"
	@echo "  logs          View logs for the kabi-server service"
	@echo "  exec          Enter the kabi-server container shell"
	@echo "  migrate       Run Django migrations"
	@echo "  makemigrations Create new Django migrations"
	@echo "  test          Run tests using pytest"
	@echo "  superuser     Create a Django superuser"
	@echo "  clean         Clean up unused Docker resources"
	@echo "  dbshell       Access the PostgreSQL database shell"
	@echo ""

# Docker-related targets
.PHONY: image
image:
	docker-compose -f $(COMPOSE_FILE) build

dev-run:
	docker-compose -f $(COMPOSE_FILE) up

dev-run-d:
	docker-compose -f $(COMPOSE_FILE) up -d

.PHONY: up
services:
	docker-compose -f $(SERVICES_COMPOSE_FILE) up

services-d:
	docker-compose -f $(SERVICES_COMPOSE_FILE) up -d

.PHONY: down
down:
	docker-compose -f $(COMPOSE_FILE) down

.PHONY: restart
restart: down up

.PHONY: logs
logs:
	docker-compose -f $(COMPOSE_FILE) logs -f $(SERVICE_WEB)

.PHONY: exec
exec:
	$(DOCKER_EXEC_WEB) /bin/bash

# Django-related targets
.PHONY: migrate
migrate:
	docker-compose -f $(COMPOSE_FILE) run --rm $(SERVICE_WEB)  migrate

.PHONY: makemigrations
makemigrations:
	docker-compose -f $(COMPOSE_FILE) run --rm $(SERVICE_WEB)  makemigrations

.PHONY: superuser
superuser:
	docker-compose -f $(COMPOSE_FILE) run --rm $(SERVICE_WEB)  createsuperuser

.PHONY: test
test:
	docker-compose -f $(COMPOSE_FILE) run --rm $(SERVICE_WEB)  test

# Database-related targets
.PHONY: dbshell
dbshell:
	docker exec -it $(SERVICE_DB) psql -U $$POSTGRES_USER $$POSTGRES_DB

# Cleanup-related targets
.PHONY: clean
clean:
	docker system prune -f

.PHONY: clean-volumes
clean-volumes:
	docker-compose -f $(COMPOSE_FILE) down --volumes

dev-ssh:
	docker-compose -f $(COMPOSE_FILE) exec kabi-server bash

dev-attach:
	docker attach kabi-server
