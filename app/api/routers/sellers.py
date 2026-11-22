from typing import Annotated
from fastapi import APIRouter, Depends , HTTPException , status
from ..schemas.sellers import SellerCreate,SellerRead,SellerResponse
from app.api.dependencies import SellerDep 
from app.database.models import Seller
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix='/sellers',tags=['sellers'])

@router.post("/signup",response_model=SellerResponse)
async def register_seller(seller:SellerCreate,service:SellerDep)->Seller:
    return await service.add_seller(seller)

@router.post("/login")
async def login_seller(request_form :Annotated[OAuth2PasswordRequestForm, Depends()],service:SellerDep):
    token = await service.login_seller(request_form.username,request_form.password)
    return {
        "access_token" : token,
        "type" : "jwt"
    }