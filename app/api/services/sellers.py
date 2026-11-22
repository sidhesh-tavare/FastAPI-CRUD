from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import Seller
from app.api.schemas.sellers import SellerCreate,SellerResponse
from argon2 import PasswordHasher
from sqlalchemy import select
from  fastapi import HTTPException,status
import jwt
from datetime import datetime,timezone,timedelta
from app.config import loginsettings
from argon2.exceptions import InvalidHashError, VerifyMismatchError

ph = PasswordHasher()

class SellerService(): 
    
    def __init__(self,session:AsyncSession):
        self.session = session
        
    async def add_seller(self,seller_data : SellerCreate)->SellerResponse:
        seller = Seller(**seller_data.model_dump(exclude={"password"}),password_hash = ph.hash(seller_data.password))
        self.session.add(seller)
        await self.session.commit()
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
                    "name": seller.name,
                    "email": seller.email,
                },
                "exp": datetime.now(timezone.utc) + timedelta(days=1),
            },
            algorithm=loginsettings.algorithm,
            key=loginsettings.get_signature,
        )
        return token

        
        
token = jwt.encode(
            payload = {
                "user" : {
                    "name" : "Sidhesh",
                    "email": "sidhesh@gmail.com"
                 },
                "exp": datetime.now(timezone.utc)+timedelta(days=1)
            },
            algorithm=loginsettings.algorithm,
            key = loginsettings.get_signature
        )
print(token)

