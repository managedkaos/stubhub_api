import os
import boto3
import hmac
import hashlib
import base64

from dotenv import load_dotenv, find_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")

load_dotenv(find_dotenv())

COGNITO_USER_POOL_ID = os.getenv('COGNITO_USER_POOL_ID')
COGNITO_CLIENT_ID = os.getenv('COGNITO_CLIENT_ID')
COGNITO_CLIENT_SECRET = os.getenv('COGNITO_CLIENT_SECRET')
REGION_NAME = os.getenv('REGION_NAME')

username = "edward.example@example.com"
password = "ThispasswordisAmazingfor2021!"

client = boto3.client("cognito-idp")

response = client.list_users(
    UserPoolId=COGNITO_USER_POOL_ID,
    AttributesToGet=['email'],
    Limit=10,
)

print(response)

message = username + COGNITO_CLIENT_ID
dig = hmac.new(bytearray(COGNITO_CLIENT_SECRET, "utf-8"), msg=message.encode('UTF-8'),
               digestmod=hashlib.sha256).digest()
secret_hash = base64.b64encode(dig).decode()

response = client.admin_initiate_auth(
    AuthFlow='USER_SRP_AUTH',
    UserPoolId=COGNITO_USER_POOL_ID,
    AuthParameters={
        'USERNAME': username,
        'PASSWORD': password,
        'SECRET_HASH': secret_hash
    },
    ClientId=COGNITO_CLIENT_ID
)
