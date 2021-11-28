backend:  uvicorn backend:app --reload --port=8000
frontend: uvicorn frontend:app --reload --port=9000
dynamodb: docker run --rm -p 7500:8000 --name dynamodb amazon/dynamodb-local -jar DynamoDBLocal.jar -inMemory -sharedDb
