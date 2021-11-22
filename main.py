from datetime import datetime
from uuid import UUID
from typing import Union, List, Dict
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from botocore.exceptions import ClientError
import boto3
import requests
import os

STUBHUB_TOKEN = os.getenv("STUBHUB_TOKEN")
STUBHUB_EVENTS_URL = os.getenv("STUBHUB_EVENTS_URL")
DYNAMODB_TABLE = os.getenv("DYNAMODB_TABLE")
DYNAMODB_URL = os.getenv("DYNAMODB_URL")
REGION_NAME = os.getenv("REGION_NAME")

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


app = FastAPI()


@app.get("/")
async def hello():
    return {"detail": "hello"}


@app.get("/event/{eventId}")
async def get_event(eventId):
    database = boto3.resource('dynamodb', region_name=REGION_NAME, endpoint_url=DYNAMODB_URL)
    table = database.Table(DYNAMODB_TABLE)

    try:
        response = table.get_item(Key={'id': int(eventId)})
    except ClientError as e:
        message = "Client error. {}. region_name={}; table_name={}".format(e.response['Error']['Message'], REGION_NAME, DYNAMODB_TABLE)
        print(message)
        raise HTTPException(status_code=404, detail=message)
    else:
        if 'Item' in response:
            print(response['Item'])
            return response['Item']
        else:
            raise HTTPException(status_code=404, detail="Item with ID={} not found.".format(eventId))


@app.post("/event/{eventId}")
async def post_event(eventId):
    try:
        headers = {'Authorization': 'Bearer {}'.format(STUBHUB_TOKEN)}
        params = {'id': eventId}
        response = requests.request("GET", STUBHUB_EVENTS_URL, params=params, headers=headers)
        print(response.text)
    except requests.exceptions.RequestException as e:
        message = "Failed to connect to StubHub API. {}".format(e)
        print(message)
        raise HTTPException(status_code=500, detail=message)
    else:
        if "fault" in response.json():
            message = "Stubhub API fault. {}".format(response.json()['fault']['faultstring'])
            print(message)
            raise HTTPException(status_code=500, detail=message)
        if "error" in response.json():
            message = "StubHub API error. {}".format(response.json()['error']['message'])
            print(message)
            raise HTTPException(status_code=404, detail=message)
        else:
            item = response.json()['events'][0]
            print(item['ticketInfo'])

    try:
        database = boto3.resource('dynamodb', region_name=REGION_NAME)
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
        message = "DynamoDB client error. {}".format(e.response['Error']['Message'])
        print(message)
        raise HTTPException(status_code=400, detail=message)
    else:
        print(response)
        return response['ResponseMetadata']
