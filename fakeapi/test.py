from botocore.exceptions import ClientError, EndpointConnectionError
import boto3
import os

os.environ['AWS_ACCESS_KEY_ID'] = '1234567890'
os.environ['AWS_SECRET_ACCESS_KEY'] = '1234567890'

database = boto3.resource('dynamodb', region_name='us-west-1', endpoint_url='http://dynamodb:8000')
table = database.Table('foo')

response = table.scan()
events = response['Items']

while 'LastEvaluatedKey' in response:
    response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
    events.extend(response['Items'])
