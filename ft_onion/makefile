up: build
	@docker compose up -d
build:
	@docker compose build

rebuild:
	@docker compose build --no-cache

stop:
	@docker compose stop

down: stop
	@docker compose down

clear:
	@docker compose down -v

prune:
	@docker volume prune -f

.PHONY: up build rebuild stop down clear
