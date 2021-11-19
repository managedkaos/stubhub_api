import os
import base64
import json
import requests
from dotenv import load_dotenv

load_dotenv()

url = os.getenv('CLIENT_CREDENTIALS_URL')
consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')

basic_authorization_token = base64.b64encode(
        bytes(
            consumer_key + ':' + consumer_secret,
            encoding="raw_unicode_escape")
        )

data = json.dumps({
    "username": username,
    "password": password
    })

headers = {
        'Authorization': 'Basic ' + basic_authorization_token.decode('UTF-8'),
        'Content-Type': 'application/json',
        }

response = requests.request("POST", url, headers=headers, data=data)
response = json.loads(response.text)

print(json.dumps({
    "basic_authorization_token": basic_authorization_token.decode('UTF-8'),
    "access_token": response['access_token']
    }))
