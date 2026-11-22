from datetime import datetime, timezone
from enum import Enum
from sqlmodel import Field, SQLModel
from pydantic import EmailStr
import uuid 
from uuid import uuid4


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
    email : EmailStr
    password_hash : str