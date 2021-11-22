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
REGION_NAME = os.getenv("REGION_NAME")

class Simple(BaseModel):
    id: Union[UUID, int, str]
    name: str


class Venue(BaseModel):
    id: Union[UUID, int, str]
    name: str
    city: str
    state: str
    postalCode: str
    country: str
    venueConfigId: Union[UUID, int, str]
    venueConfigName: str
    latitude: str
    longitude: str


class Ticketinfo(BaseModel):
    minPrice: Union[str, int]
    minListPrice: Union[str, int]
    maxListPrice: Union[str, int]
    totalTickets: int
    totalListings: int


class EventId(BaseModel):
    id: Union[UUID, int, str]


class Event(BaseModel):
    id: Union[UUID, int, str]
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
    database = boto3.resource('dynamodb', region_name=REGION_NAME)
    table = database.Table(DYNAMODB_TABLE)

    try:
        response = table.get_item(Key={'id': eventId})
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
        message="Failed to connect to StubHub API. {}".format(e)
        print(message)
        raise HTTPException(status_code=500, detail=message)
    else:
        if "fault" in response.json():
            message="Stubhub API fault. {}".format(response.json()['fault']['faultstring'])
            print(message)
            raise HTTPException(status_code=500, detail=message)
        if "error" in response.json():
            message="StubHub API error. {}".format(response.json()['error']['message'])
            print(message)
            raise HTTPException(status_code=404, detail=message)
        else:
            item = response.json()['events'][0]

    try:
        database = boto3.resource('dynamodb', region_name=REGION_NAME)
        table = database.Table(DYNAMODB_TABLE)
        response = table.put_item(Item={
            "id": str(item['id']),
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
            #"venue": item['venue'],
            "timezone":  item['timezone'],
            "currencyCode":  item['currencyCode'],
            #"ticketInfo": item['ticketInfo'],
            "performers": item['performers'],
            "ancestors": item['ancestors'],
            "categoriesCollection": item['categoriesCollection']
            })
    except ClientError as e:
        message = "DynamoDB client error. {}".format(e.response['Error']['Message'])
        print(message)
        raise HTTPException(status_code=400, detail=message)
    else:
        print(response)
        return response['ResponseMetadata']
