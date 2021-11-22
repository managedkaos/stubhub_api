run:
	python algo.py

server:
	uvicorn main:app --reload

token:
	python generate_access_token.py
