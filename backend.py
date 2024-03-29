from mangum import Mangum
from datetime import datetime
from typing import Union, List, Dict
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from botocore.exceptions import ClientError, EndpointConnectionError


import pyrebase
import boto3
import requests
import os

# stage = os.environ.get('OPERATION_MODE', "development")
# openapi_prefix = f"/{stage}" if stage else "/"

STUBHUB_TOKEN = os.getenv("STUBHUB_TOKEN")
STUBHUB_EVENTS_URL = os.getenv("STUBHUB_EVENTS_URL")
DYNAMODB_TABLE = os.getenv("DYNAMODB_TABLE")
DYNAMODB_URL = os.getenv("DYNAMODB_URL")
REGION_NAME = os.getenv("REGION_NAME")
OPERATION_MODE = os.getenv("OPERATION_MODE")

class Simple(BaseModel):
    id: int
    name: str


class Venue(BaseModel):
    id: int
    name: str
    city: str
    state: str
    postalCode: str
    country: str
    venueConfigId: int
    venueConfigName: str
    latitude: str
    longitude: str


class Ticketinfo(BaseModel):
    minPrice: Union[int, str]
    minListPrice: Union[int, str]
    maxListPrice: Union[int, str]
    totalTickets: int
    totalListings: int


class EventId(BaseModel):
    id: int


class Event(BaseModel):
    id: int
    status: str
    locale: str
    name: str
    description: str
    webURI: str
    eventDateLocal: datetime
    eventDateUTC: datetime
    createdDate: datetime
    lastUpdatedDate: datetime
    hideEventDate: bool
    hideEventTime: bool
    venue: Venue
    timezone: str
    currencyCode: str
    ticketInfo: Ticketinfo
    performers: List[Simple]
    ancestors: Dict[str, List[Simple]]
    categoriesCollection: Dict[str, List[Simple]]


app = FastAPI(title="backend") #, openapi_prefix=openapi_prefix)


@app.get("/")
async def hello():
    print("{\"detail\": \"hello\"}")
    return {"detail": "hello"}

@app.get("/events")
async def get_events():
    database = boto3.resource('dynamodb', region_name=REGION_NAME, endpoint_url=DYNAMODB_URL)
    table = database.Table(DYNAMODB_TABLE)

    try:
        print("Getting all events")
        response = table.scan()
    except ClientError as e:
        message = "DyanmoDB client error. {}. region_name={}; table_name={}".format(e.response['Error']['Message'], REGION_NAME, DYNAMODB_TABLE)
        print(message)
        raise HTTPException(status_code=500, detail=message)
    except EndpointConnectionError as e:
        message = "DynamoDB client error. {}. region_name={}; table_name={}".format(e, REGION_NAME, DYNAMODB_TABLE)
        print(message)
        raise HTTPException(status_code=500, detail=message)
    else:
        events = response['Items']

        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            events.extend(response['Items'])

        return {"total": len(events), "events": events}


@app.get("/event/{eventId}")
async def get_event(eventId):
    print("Getting event {}".format(eventId))
    database = boto3.resource('dynamodb', region_name=REGION_NAME, endpoint_url=DYNAMODB_URL)
    table = database.Table(DYNAMODB_TABLE)

    try:
        print("Reading event data from {}/{}".format(DYNAMODB_URL, DYNAMODB_TABLE))
        response = table.get_item(Key={'id': int(eventId)})
    except ClientError as e:
        message = "DyanmoDB client error. {}. region_name={}; table_name={}".format(e.response['Error']['Message'], REGION_NAME, DYNAMODB_TABLE)
        print(message)
        raise HTTPException(status_code=500, detail=message)
    except EndpointConnectionError as e:
        message = "DynamoDB client error. {}. region_name={}; table_name={}".format(e, REGION_NAME, DYNAMODB_TABLE)
        print(message)
        raise HTTPException(status_code=500, detail=message)
    else:
        if 'Item' in response:
            print(response['Item'])
            return response['Item']
        else:
            raise HTTPException(status_code=404, detail="Item with ID={} not found.".format(eventId))


@app.post("/event/{eventId}")
async def post_event(eventId):
    print("Creating event {}".format(eventId))
    try:
        print("Requesting event data from {}".format(STUBHUB_EVENTS_URL))
        headers = {'Authorization': 'Bearer {}'.format(STUBHUB_TOKEN)}
        params = {'id': int(eventId)}
        response = requests.request("GET", STUBHUB_EVENTS_URL, params=params, headers=headers)
    except requests.exceptions.RequestException as e:
        message = "Failed to connect to StubHub API. {}".format(e)
        print(message)
        raise HTTPException(status_code=500, detail=message)
    else:
        if "fault" in response.json():
            message = "Stubhub API fault. {}".format(response.text)
            print(message)
            raise HTTPException(status_code=500, detail=message)
        if "error" in response.json():
            message = "StubHub API error. {}".format(response.text)
            print(message)
            raise HTTPException(status_code=500, detail=message)
        else:
            # data generated by json-server
            if OPERATION_MODE == "local":
                print(response.json())
                try:
                    item = response.json()[0]
                except IndexError as e:
                    message = "Error. {}".format(e)
                    raise HTTPException(status_code=500, detail=e)


            # data generated by https://app.json-generator.com/ljsdksoT2-Ls
            elif OPERATION_MODE == "development":
                item = response.json()[0]['events'][0]
                item['id'] = int(eventId)

            # data generated by the real StubHub API
            else:
                item = response.json()['events'][0]

    try:
        print("Writing event data to {}/{}".format(DYNAMODB_URL, DYNAMODB_TABLE))
        database = boto3.resource('dynamodb', region_name=REGION_NAME, endpoint_url=DYNAMODB_URL)
        table = database.Table(DYNAMODB_TABLE)
        response = table.put_item(Item={
            "id": item['id'],
            "status": item['status'],
            "locale": item['locale'],
            "name": item['name'],
            "description": item['description'],
            "webURI": item['webURI'],
            "eventDateLocal": item['eventDateLocal'],
            "eventDateUTC":  item['eventDateUTC'],
            "createdDate":  item['createdDate'],
            "lastUpdatedDate":  item['lastUpdatedDate'],
            "hideEventDate":  item['hideEventDate'],
            "hideEventTime":  item['hideEventTime'],
            "venue": {
                "id": item['venue']['id'],
                "name": item['venue']['name'],
                "city": item['venue']['city'],
                "state": item['venue']['state'],
                "postalCode": item['venue']['postalCode'],
                "country": item['venue']['country'],
                "venueConfigId": item['venue']['venueConfigId'],
                "venueConfigName": item['venue']['venueConfigName'],
                "latitude": str(item['venue']['latitude']),
                "longitude": str(item['venue']['longitude'])},
            "timezone":  item['timezone'],
            "currencyCode":  item['currencyCode'],
            "ticketInfo": {
                "minPrice": str(item['ticketInfo']['minPrice']),
                "minListPrice": str(item['ticketInfo']['minListPrice']),
                "maxListPrice": str(item['ticketInfo']['maxListPrice']),
                "totalTickets": str(item['ticketInfo']['totalTickets']),
                "totalListings": str(item['ticketInfo']['totalListings'])},
            "performers": item['performers'],
            "ancestors": item['ancestors'],
            "categoriesCollection": item['categoriesCollection'],
            "ingestionDate": str(datetime.utcnow().isoformat())
            })
    except ClientError as e:
        message = "DyanmoDB client error. {}. region_name={}; table_name={}".format(e.response['Error']['Message'], REGION_NAME, DYNAMODB_TABLE)
        print(message)
        raise HTTPException(status_code=500, detail=message)
    except EndpointConnectionError as e:
        message = "DynamoDB client error. {}. region_name={}; table_name={}".format(e, REGION_NAME, DYNAMODB_TABLE)
        print(message)
        raise HTTPException(status_code=500, detail=message)
    else:
        print(response)
        return response['ResponseMetadata']


@app.delete("/event/{eventId}")
async def delete_event(eventId):
    print("Deleting event {}".format(eventId))
    database = boto3.resource('dynamodb', region_name=REGION_NAME, endpoint_url=DYNAMODB_URL)
    table = database.Table(DYNAMODB_TABLE)

    # Read to see if the item is there
    try:
        print("Reading event data from {}/{}".format(DYNAMODB_URL, DYNAMODB_TABLE))
        response = table.get_item(Key={'id': int(eventId)})
    except ClientError as e:
        message = "DyanmoDB client error. {}. region_name={}; table_name={}".format(e.response['Error']['Message'], REGION_NAME, DYNAMODB_TABLE)
        print(message)
        raise HTTPException(status_code=500, detail=message)
    except EndpointConnectionError as e:
        message = "DynamoDB client error. {}. region_name={}; table_name={}".format(e, REGION_NAME, DYNAMODB_TABLE)
        print(message)
        raise HTTPException(status_code=500, detail=message)
    else:
        if 'Item' in response:
            try:
                print("Deleting event data from {}/{}".format(DYNAMODB_URL, DYNAMODB_TABLE))
                response = table.delete_item(Key={'id': int(eventId)})
            except ClientError as e:
                message = "DyanmoDB client error. {}. region_name={}; table_name={}".format(e.response['Error']['Message'], REGION_NAME, DYNAMODB_TABLE)
                print(message)
                raise HTTPException(status_code=500, detail=message)
            except EndpointConnectionError as e:
                message = "DynamoDB client error. {}. region_name={}; table_name={}".format(e, REGION_NAME, DYNAMODB_TABLE)
                print(message)
                raise HTTPException(status_code=500, detail=message)
            else:
                print(response)
                return {"id": eventId, "detail": "The target item has been deleted", "response": response['ResponseMetadata']}
        else:
            return {"id": eventId, "detail": "The target item was not found. But that's OK since you wanted to delete it anyway....right?", "response": response['ResponseMetadata']}


@app.post("/login")
async def login():
    return {"detail": "Logging in!"}


@app.post("/logout")
async def logout():
    return {"detail": "Logging out!"}



handler = Mangum(app)
