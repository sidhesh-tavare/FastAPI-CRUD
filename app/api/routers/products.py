from fastapi import APIRouter ,status,HTTPException
from app.api.schemas.products import ProductCreate,ProductUpdate
from app.database.models import ProductUpdate,ProductCreate
from app.api.dependencies import ProductDep,SellerDep
from typing import Any
# from datetime import datetime,timezone

router = APIRouter(prefix="/products",tags=['products'])

@router.get("/health")
async def health_check():
    return {"message":"working"}

@router.get("/")
async def get_product(id: int,service:ProductDep):
    product = await service.get_product(id)
    if product is None :
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Given id doesn't exist!")
    return product


@router.post("/")
async def create_product(data: ProductCreate , service :ProductDep) -> dict[str, Any]:
    return await service.add_product(data)

@router.patch("/")
async def update_product(id: int, body: ProductUpdate,service :ProductDep):
    update_data = body.model_dump(exclude_none=True)
    if update_data is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No data to update")

    product = await service.update_product(id,body)
    if product:
        return product

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {id} not found",
        )


@router.delete("/")
async def delete_product(id: int ,service :ProductDep) -> dict[str, Any]:
    res = await service.delete_product(id)
    if res is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,detail="Product with given id not found"
        )
    return {"message":f"deleted product id {id}"}

