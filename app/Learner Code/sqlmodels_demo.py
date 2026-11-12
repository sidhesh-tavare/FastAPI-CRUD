from sqlmodel import SQLModel , Field 
from typing import Any , Optional
from enum import Enum
from datetime import datetime

class ProductCategory(str,Enum):
    ELECTRONICS = 'electronics'
    CLOTHING = 'clothing'
    HOME = 'home'
    ACCESSORIES = 'accessories'
    PERIPHERALS = 'peripherals'

class Product(SQLModel,table=True):
    __tablename__ = "products"
    id : int | None = Field(default=None,primary_key=True)
    name : str = Field(max_length=100)
    price : float = Field(gt=0)
    stock : int = Field(ge=0)
    category : ProductCategory
    created_at : datetime = Field(default_factory=datetime.now)





