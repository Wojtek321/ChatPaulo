run:
	docker compose -f ./docker/docker-compose.yml up -d

down:
	docker compose -f ./docker/docker-compose.yml down --remove-orphans

build:
	docker compose -f ./docker/docker-compose.yml build

launch:
	if docker exec -i postgress psql -U postgres -c "SELECT 1 FROM pg_database WHERE datname = 'restaurant_db'" | grep -q 1; then \
		echo "Database already exists."; \
	else \
		echo "Creating database..."; \
		docker exec -i postgress psql -U postgres -c "CREATE DATABASE restaurant_db"; \
		echo "Loading database dump..."; \
		docker exec -i postgress psql -U postgres -d restaurant_db < ./postgres_db/dump.sql; \
		echo "Loading data into vector database..."; \
		python ./qdrant_db/load_data.py; \
		echo "Launch process completed successfully."; \
	fi
