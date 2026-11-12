# Module 6 - Complete app with Pydantic schemas
# Run (from the m06 folder):  fastapi dev app/main.py
from fastapi import FastAPI, HTTPException, status

from app.schemas.models import *
from app.database.database import Database
db = Database()

app = FastAPI()

# We return a plain dict, so the schema goes in response_model=
# (it validates the output AND hides keys that are not in the schema)
@app.get("/products")
def get_product(id: int):
    product = db.get_product(product_id=id)
    if product is None :
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Given id doesn't exist!")
    return product


@app.post("/products")
def create_product(product: ProductCreate) -> dict[str, int]:
    new_id = db.create_product(product=product)
    return {"id": new_id}


@app.patch("/products")
def update_product(id: int, body: ProductUpdate):
    res = db.update_product(product_id=id,new_product=body)
    if res is not None: return res 
    raise HTTPException(status.HTTP_404_NOT_FOUND,"Given id does not exist")


@app.delete("/products")
def delete_product(id: int) -> dict[str, str]:
    res = db.delete_product(product_id=id)
    if not res: raise HTTPException(status.HTTP_404_NOT_FOUND,"Item does not exist")
    return res