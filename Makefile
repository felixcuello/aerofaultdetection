all: build up

build: build
	docker compose build --no-cache

shell:
	docker compose exec aero_app bash

attempt_1:
	docker-compose run --entrypoint python3 aero_app scripts/attempt_1_isolation_forest.py data/D214102-2023.csv

testshell:
	docker compose run -p 80:80 aero_app bash

up:
	docker compose up

down:
	docker compose down

# ------------------------------------------------------------------
#  RUN TESTS
# ------------------------------------------------------------------
test:
	docker compose run aero_app pytest

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
	docker compose exec -T aero_db psql -U aero_admin aero_db < ./sql/create_aero_sensor.sql
	docker compose exec -T aero_db psql -U aero_admin aero_db < ./sql/create_aero_sample.sql

db_drop:
	docker compose exec -T aero_db psql -U aero_admin aero_db < ./sql/drop_tables.sql

db_destroy: down
	rm -rf aero_db

# -- This command initiates the docker agent in MacOS
macos_docker_up:
	open -a Docker
