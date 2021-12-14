all:
	honcho start
	docker stop dynamodb

start-dynamodb:
	docker run --detach --rm -p 7500:8000 --name dynamodb amazon/dynamodb-local -jar DynamoDBLocal.jar -inMemory -sharedDb

stop-dynamodb:
	docker stop dynamodb

table:
	aws dynamodb create-table \
		--cli-input-json file://dynamodb-table-config.json \
		--endpoint-url http://localhost:8000 || echo "All good! table is likely already there."

events:
	cheat post-to-local-api-with-path-variables | bash

token:
	python generate_access_token.py

algo:
	python algo.py

build:
	@docker build --tag=backend --build-arg TARGET=backend .
	@docker build --tag=frontend --build-arg TARGET=frontend .

logs:
	@docker compose logs

detach: down
	@docker compose up --detach -e STUBHUB_TOKEN=$(STUBHUB_TOKEN)

up: down
	@docker compose up -e STUBHUB_TOKEN=$(STUBHUB_TOKEN)

down:
	@docker compose down --rmi local

init:
	./init-local-environment.sh
