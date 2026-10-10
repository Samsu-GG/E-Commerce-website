from typing_extensions import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from App.api.dependency import SellerServiceDep
from ..schemas.seller import SellerCreate, SellerRead
router = APIRouter(prefix="/seller",tags=["seller"])

@router.post("/register", response_model=SellerRead)
async def register_seller(credential: SellerCreate,service : SellerServiceDep):
    return await service.regestration(credential)
    
@router.post("/signin")
async def login_seller(request_form: Annotated[OAuth2PasswordRequestForm,Depends()], service : SellerServiceDep):

    token =  await service.sign_in(request_form.username,request_form.password)
    return {"access_token": token, "token_type": "jwt"}