UNAME_S := $(shell uname -s)

CURRENT_USER := $(shell whoami)
UID := $(shell id -u $(CURRENT_USER))
GID := $(shell id -g $(CURRENT_USER))

ifeq ($(UNAME_S),Darwin)
    GID := 1000
endif

.PHONY: all
all: help

.PHONY: help
help:
	@echo "Comandos disponíveis:"
	@echo "  make run          - Inicia os containers"
	@echo "  make build        - Faz build dos containers"
	@echo "  make console      - Acessa o bash do container app"
	@echo "  make hard-rebuild - Rebuild completo (remove volumes)"

.PHONY: run
run:
	@docker compose -f docker-compose.yml up

.PHONY: build
build:
	@docker compose -f docker-compose.yml build --build-arg GID=${GID} --build-arg UID=${UID}

.PHONY: console
console:
	@docker compose -f docker-compose.yml exec app bash

.PHONY: hard-rebuild
hard-rebuild:
	@docker compose -f docker-compose.yml down --volumes --remove-orphans
	@docker compose -f docker-compose.yml build --no-cache --build-arg GID=${GID} --build-arg UID=${UID}
	@docker compose -f docker-compose.yml up
