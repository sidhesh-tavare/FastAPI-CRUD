from typing import Annotated,Any,Optional
from fastapi import FastAPI, HTTPException, status
from contextlib import asynccontextmanager
from fastapi.params import Depends
from sqlmodel import Session
from app.schemas.models import *
from app.database.database import Database
from app.database.models import Product,ProductCategory,ProductUpdate
from app.database.session import get_session
db = Database()

app = FastAPI()
SessionDep = Annotated[Session,Depends(get_session)]

# We return a plain dict, so the schema goes in response_model=
# (it validates the output AND hides keys that are not in the schema)
@app.get("/products")
def get_product(id: int,session:SessionDep):
    product = session.get(Product,id)
    if product is None :
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Given id doesn't exist!")
    return product


@app.post("/products")
def create_product(data: Product , session : SessionDep) -> dict[str, Any]:
    new_product = Product(**data.model_dump())
    session.add(new_product)
    session.commit()
    session.refresh(new_product)
    return new_product.model_dump()


@app.patch("/products")
def update_product(id: int, body: ProductUpdate,session : SessionDep):
    update_data = body.model_dump(exclude_none=True)

    if update_data is None : 
        raise HTTPException(status.HTTP_404_NOT_FOUND,"NO data to update")

    product = session.get(Product,id)
    if product:
        product.sqlmodel_update(update_data)
        session.commit()
        session.refresh(product)
        return product


    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {id} not found",
        )

@app.delete("/products")
def delete_product(id: int,session : SessionDep) -> dict[str, str]:
    product = session.get(Product,id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,detail="Product with given id not found"
        )
    session.delete(product)
    session.commit()
    return {"detail" : f"Deleted the product with id : {id}"}