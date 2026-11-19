from fastapi import APIRouter ,status,HTTPException
from app.schemas.models import ProductCreate,ProductRead,ProductUpdate
from app.database.database import Database
from app.database.models import Product,ProductUpdate,ProductCreate
from app.database.session import SessionDep
from typing import Any
from datetime import datetime,timezone

router = APIRouter(prefix="/products",tags=['products'])

@router.get("/health")
async def health_check():
    return {"message":"working"}

@router.get("/")
async def get_product(id: int,session:SessionDep):
    product = await session.get(Product,id)
    if product is None :
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Given id doesn't exist!")
    return product


@router.post("/")
async def create_product(data: ProductCreate , session : SessionDep) -> dict[str, Any]:
    new_product = Product.model_validate(data)
    session.add(new_product)
    await session.commit()
    await session.refresh(new_product)
    return new_product.model_dump()


@router.patch("/")
async def update_product(id: int, body: ProductUpdate,session : SessionDep):
    update_data = body.model_dump(exclude_none=True)
    

    if update_data is None : 
        raise HTTPException(status.HTTP_404_NOT_FOUND,"No data to update")

    product = await session.get(Product,id)
    if product:
        # if update time etc logic
        # update_data["created_at"] = datetime.now(timezone.utc)
        product.sqlmodel_update(update_data)
        await session.commit()
        await session.refresh(product)
        return product


    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {id} not found",
        )

@router.delete("/")
async def delete_product(id: int,session : SessionDep) -> dict[str, str]:
    product = await session.get(Product,id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,detail="Product with given id not found"
        )
    await session.delete(product)
    await session.commit()
    return {"detail" : f"Deleted the product with id : {id}"}

