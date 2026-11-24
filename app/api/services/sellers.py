from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import Seller,SellerRead
from app.api.schemas.sellers import SellerCreate,SellerResponse
from argon2 import PasswordHasher
from sqlalchemy import select
from  fastapi import HTTPException,status
import jwt
from datetime import datetime,timezone,timedelta
from app.config import loginsettings
from argon2.exceptions import InvalidHashError, VerifyMismatchError
from app.database.redis_db import redis_db
from uuid import UUID,uuid4
from sqlmodel import col
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

ph = PasswordHasher()

class SellerService(): 
    
    def __init__(self,session:AsyncSession):
        self.session = session
        
    async def add_seller(self,seller_data : SellerCreate)->SellerResponse:
        seller = Seller(
        **seller_data.model_dump(exclude={"password", "email"}),email=seller_data.email.strip().lower(),password_hash=ph.hash(seller_data.password),)
        self.session.add(seller)
        try:
            await self.session.commit()
        except IntegrityError as e:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Email already registered",
            )
        await self.session.refresh(seller)
        return SellerResponse.model_validate(seller)

    
    async def login_seller(self,email,password)->str:# returns JWT access token 
        # Validate the User 
        result = await self.session.execute(select(Seller).where(Seller.email == email))
        seller = result.scalar_one_or_none()
        
        if seller is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email or password is not correct",
            )
        # generate access token to return frm the function for this we use jwt
        try:
            ph.verify(seller.password_hash, password)
        except (VerifyMismatchError, InvalidHashError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email or password is not correct",
            )

        token = jwt.encode(
            payload={
                "user": {
                    "id" : str(seller.id), #to typecase json doesn ot store datatype as uuid so 
                    
                },
                "exp": datetime.now(timezone.utc) + timedelta(days=1),
                "jti" : str(uuid4())
            },
            algorithm=loginsettings.algorithm,
            key=loginsettings.get_signature,
        )
        return token
    
    async def get_seller_details(self, seller_id: UUID) -> Seller | None:
        stmt = select(Seller).where(col(Seller.id) == seller_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
            

        
        