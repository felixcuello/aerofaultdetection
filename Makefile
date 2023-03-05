all: build up

build: build up

shell:
	docker compose exec aero_app bash

testshell:
	docker compose run -p 80:80 aero_app bash

up:
	docker compose up

down:
	docker compose down

# ------------------------------------------------------------------
#  DATABASE COMMANDS
# ------------------------------------------------------------------
psql:
	docker compose exec aero_db psql -U aero_admin aero_db

db_up:
	@mkdir -p aero_db
	docker compose up -d aero_db

db_shell:
	docker compose exec aero_db bash

db_create:
	docker compose exec -T aero_db psql -U aero_admin aero_db < ./sql/create_scada.sql

db_delete:
	docker compose exec -T aero_db psql -U aero_admin aero_db < ./sql/drop_scada.sql

db_drop: down
	rm -rf aero_db
