from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database.database import Database
from app.database.session import create_db_tables
from app.api import all_routers


db = Database()

@asynccontextmanager
async def lifespan(app:FastAPI):
    await create_db_tables()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(all_routers.router)
