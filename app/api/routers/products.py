from fastapi import APIRouter ,status,HTTPException
from app.api.schemas.products import ProductCreate,ProductUpdate
from app.database.models import ProductUpdate,ProductCreate,ProductResponse
from app.api.dependencies import ProductDep,SellerDep,CurrentSellerDep
from typing import Any
import uuid 
from uuid import uuid4
# from datetime import datetime,timezone

router = APIRouter(prefix="/products",tags=['products'])

@router.get("/health")
async def health_check():
    return {"message":"working"}

@router.get("/")
async def get_product(id: uuid.UUID,service:ProductDep,seller:CurrentSellerDep):
    product = await service.get_product(id)
    if product is None :
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Given id doesn't exist!")
    return product


@router.post("/")
async def create_product(data: ProductCreate , service :ProductDep,seller:CurrentSellerDep) -> ProductResponse:
    # product_data = data.model_copy(update={"seller_id" : seller.id})
    product = await service.add_product(data,seller.id)
    return ProductResponse.model_validate(product,from_attributes=True)

@router.patch("/")
async def update_product(id: uuid.UUID, body: ProductUpdate,service :ProductDep,seller:CurrentSellerDep):
    update_data = body.model_dump(exclude_none=True)
    if update_data is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No data to update")

    product = await service.update_product(id,body,current_seller_id = seller.id)
    if product:
        return product

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {id} not found",
        )


@router.delete("/")
async def delete_product(id: uuid.UUID ,service :ProductDep,seller:CurrentSellerDep) -> dict[str, Any]:
    res = await service.delete_product(id)
    if res is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,detail="Product with given id not found"
        )
    return {"message":f"deleted product id {id}"}

@router.get("/all")
async def get_all_products(service:ProductDep , seller:CurrentSellerDep)->dict[uuid.UUID, ProductResponse]:
    products = await service.get_all_products()
    if products : return {
        p.id: ProductResponse.model_validate(p, from_attributes=True)
        for p in products}
    raise HTTPException(
        status_code=status.HTTP_204_NO_CONTENT,
        detail = "No products available to display"
    )

@router.get("/{seller_id}")  
async def get_seller_products(service:ProductDep,seller_id : uuid.UUID)-> dict[uuid.UUID,ProductResponse]:
    products = await service.get_seller_products(seller_id)
    return {
        p.id: ProductResponse.model_validate(p, from_attributes=True)
        for p in products
    }
    

    

