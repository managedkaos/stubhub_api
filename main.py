from datetime import datetime
from uuid import UUID
from typing import Union, List, Dict
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from botocore.exceptions import ClientError
import boto3
import json


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


@app.get("/event/{eventId}")
async def read_event(eventId):
    database = boto3.resource('dynamodb', region_name='us-west-1')
    table = database.Table('stubhub-events-development')
    try:
        response = table.get_item(Key={'id': eventId})
    except ClientError as e:
        message = "Client error. {}".format(e.response['Error']['Message'])
        print(message)
        raise HTTPException(status_code=404, detail=message)
    else:
        if 'Item' in response:
            print(response['Item'])
            return response['Item']
        else:
            raise HTTPException(status_code=404, detail="Item with ID={} not found.".format(eventId))


@app.post("/event/")
async def create_event(event: Event):
    item = json.loads(event.json())
    database = boto3.resource('dynamodb', region_name='us-west-1')
    table = database.Table('stubhub-events-development')
    try:
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
            "venue": item['venue'],
            "timezone":  item['timezone'],
            "currencyCode":  item['currencyCode'],
            "ticketInfo": item['ticketInfo'],
            "performers": item['performers'],
            "ancestors": item['ancestors'],
            "categoriesCollection": item['categoriesCollection']
            })
    except ClientError as e:
        message = "Client error. {}".format(e.response['Error']['Message'])
        print(message)
        raise HTTPException(status_code=400, detail=message)
    else:
        print(response)
        return response
