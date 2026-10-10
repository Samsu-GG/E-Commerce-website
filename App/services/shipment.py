from datetime import datetime, timedelta

from App.Databse.models import Shipment
from App.api.schemas.shipment import ShipmentChange, ShipmentCreate, ShipmentStatus
from sqlalchemy.ext.asyncio import AsyncSession

class Shipmentservice:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_shipment(self,id:int):
         return await self.session.get(Shipment,id)

    async def add(self, shipment_create: ShipmentCreate) -> Shipment:
        new_shipment= Shipment(
                **shipment_create.model_dump(),
                status=ShipmentStatus.placed,
                estimated_date = datetime.now() + timedelta(days=3)
            )
        self.session.add(new_shipment)
        await self.session.commit()
        await self.session.refresh(new_shipment)

        return new_shipment

    async def update(self,id,update)->Shipment :
        update_Shipment = await self.session.get(Shipment,id) 
        update_Shipment.sqlmodel_update(
                update
            )
        await self.session.commit()
        await self.session.refresh(update_Shipment)
        return update_Shipment

    async def delete(self,id:int) ->None:
        await self.session.delete(self.get_shipment(id))
        await self.session.commit()