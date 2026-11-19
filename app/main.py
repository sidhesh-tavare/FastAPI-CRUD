from typing import Annotated,Any,Optional
from fastapi import FastAPI, HTTPException, status 
from contextlib import asynccontextmanager
from app.schemas.models import ProductCreate,ProductRead,ProductUpdate
from app.database.database import Database
from app.database.models import Product,ProductCategory,ProductUpdate,ProductCreate
from app.database.session import SessionDep,create_db_tables
db = Database()


@asynccontextmanager
async def lifespan(app:FastAPI):
    await create_db_tables()
    yield
    
app = FastAPI(lifespan=lifespan)




# We return a plain dict, so the schema goes in response_model=
# (it validates the output AND hides keys that are not in the schema)
@app.get("/products")
async def get_product(id: int,session:SessionDep):
    product = await session.get(Product,id)
    if product is None :
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Given id doesn't exist!")
    return product


@app.post("/products")
async def create_product(data: ProductCreate , session : SessionDep) -> dict[str, Any]:
    new_product = Product.model_validate(data)
    session.add(new_product)
    await session.commit()
    await session.refresh(new_product)
    return new_product.model_dump()


@app.patch("/products")
async def update_product(id: int, body: ProductUpdate,session : SessionDep):
    update_data = body.model_dump(exclude_none=True)

    if update_data is None : 
        raise HTTPException(status.HTTP_404_NOT_FOUND,"NO data to update")

    product = await session.get(Product,id)
    if product:
        product.sqlmodel_update(update_data)
        await session.commit()
        await session.refresh(product)
        return product


    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {id} not found",
        )

@app.delete("/products")
async def delete_product(id: int,session : SessionDep) -> dict[str, str]:
    product = await session.get(Product,id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,detail="Product with given id not found"
        )
    await session.delete(product)
    await session.commit()
    return {"detail" : f"Deleted the product with id : {id}"}