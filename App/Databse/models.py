
from datetime import datetime
from pydantic import EmailStr
from sqlmodel import SQLModel,Field

from App.api.schemas.shipment import ShipmentStatus

class Shipment(SQLModel,table=True):
    id : int|None = Field(default=None,primary_key=True)
    content : str
    weight : float = Field(le=25)
    status : ShipmentStatus|None=Field(default=None)
    estimated_date: datetime|None=Field(default=None)

class Seller(SQLModel,table=True):
    id : int|None = Field(default=None,primary_key=True)
    name : str
    email : EmailStr
    password_hash : str