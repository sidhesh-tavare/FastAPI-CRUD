from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import Seller
from app.api.schemas.sellers import SellerCreate
from argon2 import PasswordHasher

ph = PasswordHasher()

class SellerService(): 
    
    def __init__(self,session:AsyncSession):
        self.session = session
        
    async def add_seller(self,seller_data : SellerCreate)->Seller:
        seller = Seller(**seller_data.model_dump(exclude={"password"}),password_hash = ph.hash(seller_data.password))
        self.session.add(seller)
        await self.session.commit()
        await self.session.refresh(seller)
        return seller


