from typing import Any 
from fastapi import FastAPI , HTTPException , status
from fastapi.concurrency import asynccontextmanager
from app.schemas.models import ProductUpdate,ProductCreate,ProductRead
from rich import print 
from rich.panel import Panel

@asynccontextmanager
async def lifespan(app:FastAPI):
    print(Panel("Server started Running",border_style = "green"))
    yield 
    print(Panel("Server Ennded ...",border_style = "red"))

app = FastAPI(lifespan=lifespan)

@app.get("/product")
def get_product()->int:
    return 0

