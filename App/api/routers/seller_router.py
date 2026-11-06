from typing_extensions import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from App.Databse.models import Seller
from App.Databse.redis import add_jti_to_blacklist
from App.api.dependency import SellerDep, SellerServiceDep, SessionDep, get_access_token
from App.core.security import OAuth2_scheme
from App.utils import decode_access_token
from ..schemas.seller import SellerCreate, SellerRead
router = APIRouter(prefix="/seller",tags=["seller"])

@router.post("/register", response_model=SellerRead)
async def register_seller(credential: SellerCreate,service : SellerServiceDep):
    return await service.regestration(credential)
    
@router.post("/signin")
async def login_seller(request_form: Annotated[OAuth2PasswordRequestForm,Depends()], service : SellerServiceDep):

    token =  await service.sign_in(request_form.username,request_form.password)
    return {"access_token": token, "token_type": "jwt"}

@router.get("/logout")
async def logout_seller(token_data: Annotated[dict,Depends(get_access_token)]):
   await add_jti_to_blacklist(token_data["jti"])
   return { "message": "Successfully logged out" }


@router.get("/dashcard")
async def dashboard(seller: SellerDep):
    return seller

