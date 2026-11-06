from uuid import UUID
from App.Databse import session
from App.Databse.models import Seller
from App.Databse.redis import is_jti_blacklisted
from App.core.security import OAuth2_scheme
from App.services.seller import SellerService
from App.Databse.session import get_session
from App.services.shipment import Shipmentservice
from typing import Annotated
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from App.utils import decode_access_token


# Create a AsyncSession which depends on the get_session function which is connted to the postgres database

SessionDep= Annotated[AsyncSession,Depends(get_session)]

# get a session of the connted to the postgres database and pass it to the Shipmentservice class 
# to create a new session of the Shipmentservice class which is used to perform CRUD operations on the Shipment model
def get_shipment_service(session : SessionDep) :
    return Shipmentservice(session)

# Access Token

async def get_access_token(token : Annotated[str, Depends(OAuth2_scheme)])-> dict:
    data = decode_access_token(token)
    
    if data is None:
            raise HTTPException(status_code=401,detail="Invalid Token")
    if await is_jti_blacklisted(data["jti"]):
            raise HTTPException(status_code=401,detail="The account is logout")

    return data

# logged in seller
async def get_logged_in_seller(token_data: Annotated[dict,Depends(get_access_token)], session : SessionDep):
    seller = await session.get(Seller,UUID(token_data["user"]["id"]))
    if seller is None:
        raise HTTPException(status_code=404,detail="Seller not found")
    return seller

      

def get_seller_service(session : SessionDep):
    return SellerService(session)

# connect the router to the Shipmentservice class which is used to perform CRUD operations on the Shipment model
ServiceDep = Annotated[Shipmentservice, Depends(get_shipment_service)]
SellerServiceDep = Annotated[SellerService, Depends(get_seller_service)]
SellerDep = Annotated[Seller, Depends(get_logged_in_seller)]
