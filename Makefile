THIS_FILE := $(lastword $(MAKEFILE_LIST))
.PHONY: help build up stop restart  destroy log shell manage makemigrations migrate test

help:
	make -pRrq  -f $(THIS_FILE) : 2>/dev/null |	awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'

build:
	docker-compose -f docker-compose.yaml build $(c)
up:
	docker-compose -f docker-compose.yaml up -d $(c)
stop:
	docker-compose -f docker-compose.yaml stop $(c)
restart:
	docker-compose -f docker-compose.yaml stop $(c)
	docker-compose -f docker-compose.yaml up -d $(c)
destroy:
	docker-compose -f docker-compose.yaml down -v $(c)
log:
	docker-compose -f docker-compose.yaml logs --tail=100 -f messanger-app
shell:
	docker-compose -f docker-compose.yaml exec messanger-app /bin/bash
manage:
	docker-compose -f docker-compose.yaml exec messanger-app python manage.py $(c)
makemigrations:
	docker-compose -f docker-compose.yaml exec messanger-app python manage.py makemigrations
migrate:
	docker-compose -f docker-compose.yaml exec messanger-app python manage.py migrate
test:
	docker-compose -f docker-compose.yaml exec messanger-app python manage.py test
