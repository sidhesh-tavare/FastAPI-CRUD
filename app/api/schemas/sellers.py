import random
from enum import Enum
from pydantic import BaseModel, Field , EmailStr

class BaseSeller(BaseModel): 
    name : str = Field(max_length=30)
    email : EmailStr
    
class SellerCreate(BaseSeller):
    password : str 
    
class SellerRead(BaseSeller):
    pass
    
