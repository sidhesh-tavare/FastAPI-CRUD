from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import Product,ProductCreate,ProductUpdate

class ProductService:

    def __init__(self,session:AsyncSession):
        self.session = session

    async def get_product(self,id:int)->Product|None:
        return await self.session.get(Product,id)

    async def add_product(self,data : ProductCreate)->Product:
        new_product = Product.model_validate(data)
        self.session.add(new_product)
        await self.session.commit()
        await self.session.refresh(new_product)
        return new_product.model_dump()

    async def update_product(self,id: int, body: ProductUpdate):
        update_data = body.model_dump(exclude_none=True)
        product = await self.session.get(Product,id)
        if product is None: return None
        product.sqlmodel_update(update_data)
        await self.session.commit()
        await self.session.refresh(product)
        return product

    async def delete_product(self,id: int) -> bool | None:
        product = await self.session.get(Product,id)
        if product is None: return None
        await self.session.delete(product)
        await self.session.commit()
        return True