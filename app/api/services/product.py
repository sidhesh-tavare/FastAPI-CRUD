from sqlmodel import col ,select
from collections.abc import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import Product,ProductCreate,ProductUpdate
from uuid import uuid4 
import uuid
from typing import Any 
from fastapi import status,HTTPException

class ProductService:

    def __init__(self,session:AsyncSession):
        self.session = session

    async def get_product(self,id:uuid.UUID)->Product|None:
        return await self.session.get(Product,id)

    async def add_product(self,data : ProductCreate,seller_id : uuid.UUID)->dict[str,Any]:
        new_product = Product(**data.model_dump(),seller_id= seller_id)
        self.session.add(new_product)
        await self.session.commit()
        await self.session.refresh(new_product)
        return new_product.model_dump()

    async def update_product(self,id: uuid.UUID, body: ProductUpdate , current_seller_id : uuid.UUID):
        update_data = body.model_dump(exclude_none=True)
        product = await self.session.get(Product,id)
        if product is None: return None
        original_seller_id = product.seller_id
        if original_seller_id != current_seller_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Current Seller is not authorised to edit this product {product.id}"
            )
        product.sqlmodel_update(update_data)
        await self.session.commit()
        await self.session.refresh(product)
        return product

    async def delete_product(self,id: uuid.UUID) -> bool | None:
        product = await self.session.get(Product,id)
        if product is None: return None
        await self.session.delete(product)
        await self.session.commit()
        return True
    
    async def get_all_products(self)->Sequence[Product]:
        product = select(Product)
        result = await self.session.scalars(product)
        return result.all()
    
    async def get_seller_products(self, seller_id: uuid.UUID) -> list[Product]:
        stmt = select(Product).where(col(Product.seller_id) == seller_id)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
    
    
            