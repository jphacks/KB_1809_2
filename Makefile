SHELL   := /bin/bash

NAME    := plannap

SRCS    := $(shell find ./src -type f \( -name '*.css' -o -name '*.py' -o -name '*.html' -o -name '*.js' \) -print)
DOCKERFILE := Dockerfile
DB_USER := develop
DB_PASSWORD := password
DB_ROOT_PASSWORD := root
DB_NAME := dev_db
DB_PORT := 3306
DEV_DB_CONTAINER := $(NAME)-db-dev
DB_IMAGE := studioaquatan/mysql-utf8mb4
DB_IMAGE_VERSION := latest
ARGS := "-h"

deps:
	$(eval VENV := $(shell ls -a | grep .venv))
	$(eval PULLED_IMAGE := $(shell docker images | grep $(DB_IMAGE)))
	@if ! test -n "$(VENV)"; then \
		echo "Can't find '.venv' in current dir."; \
		pipenv install; \
	else \
		echo "Virtualenv has already been prepared."; \
	fi
	@if ! test -n "$(PULLED_IMAGE)"; then \
		docker pull $(DB_IMAGE):$(DB_IMAGE_VERSION);\
	else \
		echo "'$(DB_IMAGE):$(DB_IMAGE_VERSION)' has already been pulled."; \
	fi

image: $(SRCS) $(DOCKERFILE)
	$(eval VERSION := $(shell git describe --tags || echo "v0.0.0"))
	$(eval REVISION:= $(shell git rev-parse --short HEAD || echo "None"))
	docker build . -t studioaquatan/plannap-api:latest


rundb:
	$(eval RUNNING := $(shell docker ps -q -f name=$(DEV_DB_CONTAINER)))
	$(eval STOPPING := $(shell docker ps -aq -f name=$(DEV_DB_CONTAINER)))
	@echo "Run MySQL server named '$(DEV_DB_CONTAINER)' using docker"
	@echo "Username: $(DB_USER)"
	@echo "Password: $(DB_PASSWORD)"
	@echo "Database: $(DB_NAME)"
	@echo "Port: $(DB_PORT)"
	@echo "You can connect this DB on '127.0.0.1:$(DB_PORT)'"
	@if test -n "$(RUNNING)" || test -n "$(STOPPING)"; then \
		docker start $(DEV_DB_CONTAINER) > /dev/null;\
	else \
		docker run -d --name $(DEV_DB_CONTAINER) \
			-e MYSQL_ROOT_PASSWORD=$(DB_ROOT_PASSWORD) \
			-e MYSQL_USER=$(DB_USER) \
			-e MYSQL_PASSWORD=$(DB_PASSWORD) \
			-e MYSQL_DATABASE=$(DB_NAME) \
			-p $(DB_PORT):$(DB_PORT) \
			$(DB_IMAGE):$(DB_IMAGE_VERSION) > /dev/null; \
	fi

stopdb:
	docker stop $(DEV_DB_CONTAINER) > /dev/null

rmdb: stopdb
	docker rm $(DEV_DB_CONTAINER) > /dev/null

cleandb:
	@echo "Delete database..."
	@cd env_files/data && ls -a | grep -v -E "^\.|^\.\.|^\.git-keep" | xargs rm -rf && cd ../../
	@echo "Done"

qa-start:
	docker-compose up -d

qa-stop:
	docker-compose stop

qa-manage:
	docker-compose exec webapp pipenv run python manage.py $(ARGS)

qa-clean: qa-stop
	docker-compose rm

.PHONY: deps image rundb stopdb cleandb qa-start qa-stop qa-manage qa-clean ;
