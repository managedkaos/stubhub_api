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
		--endpoint-url http://localhost:7500 || echo "All good! table is likely already there."

events:
	cheat post-to-local-api-with-path-variables | bash

token:
	python generate_access_token.py

algo:
	python algo.py
