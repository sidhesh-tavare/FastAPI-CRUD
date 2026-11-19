from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database.database import Database
from app.database.session import create_db_tables
from app.routers import products


db = Database()
@asynccontextmanager
async def lifespan(app:FastAPI):
    await create_db_tables()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(products.router)
