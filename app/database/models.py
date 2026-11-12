from datetime import datetime, timezone
from enum import Enum
from sqlmodel import Field, SQLModel


class ProductCategory(str, Enum):
    ELECTRONICS = "electronics"
    CLOTHING = "clothing"
    HOME = "home"
    ACCESSORIES = "accessories"
    PERIPHERALS = "peripherals"


class Product(SQLModel, table=True):
    __tablename__ = "products"

    id: int | None = Field(default=None, primary_key=True)
    name: str
    price: float = Field(gt=0, le=10_000)
    stock: int = Field(ge=0)
    category: ProductCategory
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ProductUpdate(SQLModel):
    name: str
    price: float = Field(gt=0, le=10_000)
    stock: int = Field(ge=0)
    category: ProductCategory
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

