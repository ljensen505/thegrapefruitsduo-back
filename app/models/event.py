from datetime import datetime

from fastapi import UploadFile
from pydantic import BaseModel


class NewEvent(BaseModel):
    name: str
    location: str
    description: str
    time: datetime
    poster: UploadFile


class InsertionEvent(NewEvent):
    poster: str  # cloudinary id


class Event(InsertionEvent):
    id: int


EVENT_TABLE = "events"
