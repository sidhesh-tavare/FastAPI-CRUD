from datetime import datetime, timezone
from enum import Enum
from sqlmodel import Field, SQLModel


class ProductCategory(str, Enum):
    ELECTRONICS = "electronics"
    CLOTHING = "clothing"
    HOME = "home"
    ACCESSORIES = "accessories"
    PERIPHERALS = "peripherals"
    FOODS = "foods"


class Product(SQLModel, table=True):
    __tablename__ = "products"

    id: int | None = Field(default=None, primary_key=True)
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
    __tablename__ = "products"

    id: int | None = Field(default=None, primary_key=True)
    name: str
    price: float = Field(gt=0, le=10_000)
    stock: int = Field(ge=0)
    category: ProductCategory
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))