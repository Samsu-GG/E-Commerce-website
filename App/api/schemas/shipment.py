from datetime import datetime
from pydantic import BaseModel ,Field
from enum import Enum
import App.Databse.models 

class ShipmentStatus(str, Enum):
    placed= "placed"
    in_transit= "in_transit"
    out_for_delivary= "out_for_delivary"
    deliverd = "deliverd"

class BaseShipment(BaseModel):
    content :str=Field(description="The marketing of the product")
    weight : float = Field(description="The weight of the product in KG",le=25,ge=1)
    
class ShipmentRead(BaseShipment) :
    estimated_date: datetime
    status :ShipmentStatus 

class ShipmentCreate(BaseShipment) :
    pass

class ShipmentChange(BaseModel):
    content :str | None=Field(default=None)
    weight : float|None=Field(default=None)
    status : ShipmentStatus
    estimated_date: datetime |None=Field(default=None)  







