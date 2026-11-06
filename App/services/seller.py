from datetime import datetime, timedelta
from fastapi import HTTPException
import jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from App.api.schemas.seller import SellerCreate, SellerRead
from App.Databse.models import Seller
from App.config import security_settings
from App.utils import generate_access_token
# remobe the deprecated warning for bcrypt hashing algorithm {deprecated="auto"}
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class SellerService:
    def __init__(self,session: AsyncSession):
        self.session =  session

    async def regestration(self, credentials : SellerCreate) -> SellerRead:
        seller = Seller(
            **credentials.model_dump(exclude=["password"]),

            password_hash=password_context.hash(credentials.password)
        )

        self.session.add(seller)
        await self.session.commit()
        await self.session.refresh(seller)
        return seller

    async def sign_in(self,email,password) -> str:
        seller = await self.session.execute(select(Seller).where(Seller.email==email))
        #result.one()
        result = seller.scalar()

        if result is None:
            raise HTTPException(status_code=404,detail="Seller not found")

        if not password_context.verify(password,result.password_hash):
            raise HTTPException(status_code=401,detail="Invalid password")

        jwt_token = generate_access_token(data={
            "user": {
                "name" : result.name,
                "id" : str(result.id)
            }
        })

        return jwt_token
