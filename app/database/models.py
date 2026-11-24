from datetime import datetime, timezone
from enum import Enum
from sqlmodel import Field, Relationship, SQLModel
from pydantic import EmailStr
import uuid 
from uuid import uuid4
from typing import List 


class ProductCategory(str, Enum):
    ELECTRONICS = "electronics"
    CLOTHING = "clothing"
    HOME = "home"
    ACCESSORIES = "accessories"
    PERIPHERALS = "peripherals"
    FOODS = "foods"


class Product(SQLModel, table=True):
    __tablename__ = "products"

    id: uuid.UUID = Field(default_factory=uuid4,primary_key=True)
    name: str
    price: float = Field(gt=0, le=10_000)
    stock: int = Field(ge=0)
    category: ProductCategory
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    seller_id : uuid.UUID = Field(foreign_key="sellers.id")
    
    seller : "Seller" = Relationship(back_populates="listed_products",sa_relationship_kwargs={"lazy":"selectin"})
    # sa_relationship_kwargs={"lazy":"selectin"}) only load when query not when server starts

class ProductUpdate(SQLModel):
    name: str | None = None
    price: float | None = Field(default=None, gt=0, le=10_000)
    stock: int | None = Field(default=None, ge=0)
    category: ProductCategory | None = None

class ProductCreate(SQLModel):
    # What the client sends. No id or created_at: the server sets those.
    name: str
    price: float = Field(gt=0, le=10_000)
    stock: int = Field(ge=0)
    category: ProductCategory
    
class Seller(SQLModel,table=True):
    __tablename__ = "sellers"
    id : uuid.UUID = Field(default_factory=uuid4,primary_key=True)
    name : str = Field(max_length=30)
    email : EmailStr  = Field(unique=True, index=True, max_length=255)
    password_hash : str
    
    listed_products : List[Product] = Relationship(back_populates="seller",sa_relationship_kwargs={"lazy":"selectin"})
    
class ProductResponse(SQLModel):
    id: uuid.UUID
    name: str
    price: float
    stock: int
    category: ProductCategory
    created_at: datetime
    seller_id: uuid.UUID
    
class SellerRead(SQLModel):
    id : uuid.UUID
    name : str
    email : EmailStr

