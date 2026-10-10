from App.services.seller import SellerService
from App.Databse.session import get_session
from App.services.shipment import Shipmentservice
from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


# Create a AsyncSession which depends on the get_session function which is connted to the postgres database

SessionDep= Annotated[AsyncSession,Depends(get_session)]

# get a session of the connted to the postgres database and pass it to the Shipmentservice class 
# to create a new session of the Shipmentservice class which is used to perform CRUD operations on the Shipment model
def get_shipment_service(session : SessionDep) :
    return Shipmentservice(session)


def get_seller_service(session : SessionDep):
    return SellerService(session)

# connect the router to the Shipmentservice class which is used to perform CRUD operations on the Shipment model
ServiceDep = Annotated[Shipmentservice, Depends(get_shipment_service)]
SellerServiceDep = Annotated[SellerService, Depends(get_seller_service)]
