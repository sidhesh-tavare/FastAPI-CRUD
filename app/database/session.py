from sqlmodel import SQLModel, create_engine, Session
from .models import ProductCategory, Product
from sqlalchemy.ext.asyncio import AsyncSession,create_async_engine,async_sessionmaker
from sqlalchemy.orm import sessionmaker
from .models import Product
from app.config import settings
from typing import Annotated 
from fastapi import Depends

#1 create db engine asynchronously 
engine = create_async_engine(
    settings.POSTGRES_URL,
    echo=True
)

#craete session factory asynchronously 
async_session = async_sessionmaker(bind=engine,class_=AsyncSession,expire_on_commit=False)

#2create tables asyncronously 
async def create_db_tables():
    async with engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.create_all)

async def get_session():
    async with async_session() as session:
        yield session

SessionDep = Annotated[AsyncSession,Depends(get_session)]