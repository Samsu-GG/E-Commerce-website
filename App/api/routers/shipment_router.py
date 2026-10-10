from fastapi import APIRouter
from fastapi import  HTTPException,status
from App.Databse.models import Shipment
from App.api.dependency import ServiceDep
from App.api.schemas.shipment import ShipmentRead,ShipmentStatus,ShipmentCreate,ShipmentChange


from App.services.shipment import Shipmentservice

router= APIRouter(prefix="/shipment",tags=["shipment"])

@router.get("/",response_model=ShipmentRead)
async def get_shipment(id: int, service :ServiceDep): #the serviceDep is a object of shipmentservice which does CRUD operations
    #Session create -> function get_session() <AsuncSession> -> Shipmentservice(session) -> 
    shipment = await service.get_shipment(id)
    if id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The id is not there")
    return shipment

@router.post("/",response_model=None)
async def submit_shipment(shipment : ShipmentCreate, service :ServiceDep):
    new_shipment= await service.add(shipment)
    return {"id":new_shipment.id}


@router.patch("/",response_model=ShipmentChange)
async def shipment_patch(id : int,body : ShipmentChange, service :ServiceDep):
    shipment_update= body.model_dump(exclude_none=True)

    if not shipment_update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "No data Provided"
        )
    shipment= await service.update(id,shipment_update)
    return shipment

@router.delete("/")
async def delete_shipment(id : int, service :ServiceDep):
    await service.delete(id)
    return {f"{id} is deleted"}

