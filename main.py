from datetime import datetime
from uuid import UUID
from typing import Union, Optional, List, Dict
from fastapi import FastAPI
from pydantic import BaseModel

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
    latitude: float
    longitude: float

class Ticketinfo(BaseModel):
    minPrice: Union[float, int]
    minListPrice: Union[float, int]
    maxListPrice: Union[float, int]
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
    return {"detail": "Read event {}".format(eventId)}

@app.post("/event/")
async def create_event(event: Event):
    return event

