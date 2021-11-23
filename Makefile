run:
	python algo.py

server:
	honcho start

table:
	aws dynamodb create-table \
		--cli-input-json file://dynamodb-table-config.json \
		--endpoint-url http://localhost:7500

token:
	python generate_access_token.py
