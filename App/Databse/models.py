from datetime import datetime
from pydantic import EmailStr
from sqlmodel import Column, Relationship, SQLModel,Field
from uuid import uuid4, UUID
from sqlalchemy.dialects import postgresql

from App.api.schemas.shipment import ShipmentStatus

class Shipment(SQLModel,table=True):
    id : UUID = Field(sa_column=Column(postgresql.UUID, default= uuid4,primary_key=True))
    content : str
    weight : float = Field(le=25)
    status : ShipmentStatus|None=Field(default=None)
    estimated_date: datetime|None=Field(default=None)
    seller_id : UUID = Field(foreign_key="seller.id")
    seller: "Seller" = Relationship(back_populates="shipments",
                                     sa_relationship_kwargs={"lazy": "selectin"})

class Seller(SQLModel,table=True):
    id : UUID = Field(sa_column=Column(postgresql.UUID, default= uuid4,primary_key=True))
    name : str
    email : EmailStr
    password_hash : str

    shipments : list[Shipment] = Relationship(back_populates="seller",
    sa_relationship_kwargs={"lazy": "selectin"})