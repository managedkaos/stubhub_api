server:
	honcho start

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
