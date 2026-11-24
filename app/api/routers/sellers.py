from typing import Annotated
from fastapi import APIRouter, Depends , HTTPException , status
from redis import Redis,RedisError
from ..schemas.sellers import SellerCreate,SellerResponse
from app.api.dependencies import SellerDep , get_access_token , decode_access_token
from app.database.models import Seller
from fastapi.security import OAuth2PasswordRequestForm
from app.database.redis_db import blacklist_jti
from uuid import UUID
from app.api.services.sellers import SellerService

router = APIRouter(prefix='/sellers',tags=['sellers'])

@router.post("/signup")
async def register_seller(seller:SellerCreate,service:SellerDep)->SellerResponse:
    return await service.add_seller(seller)

@router.post("/login")
async def login_seller(request_form :Annotated[OAuth2PasswordRequestForm, Depends()],service:SellerDep):
    token = await service.login_seller(request_form.username,request_form.password)
    data = decode_access_token(token)
    return {
        "access_token" : token,
        "type" : "jwt",
        "jwt_decoded" : data
    }

@router.get("/logout")
async def logout_seller(token_data : Annotated[dict,Depends(get_access_token)]):
    jti = token_data['jti']
    try:
        await blacklist_jti(jti=jti)
    except RedisError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail = "Could not log out right now. Please check again"
        )
    return {"detail" : "LoggedOut Successfully"}

@router.get("/{seller_id}")
async def get_seller_details(seller_id : UUID,service:SellerDep)->SellerResponse:
    seller = await service.get_seller_details(seller_id=seller_id)
    if seller is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Seller not found",
        )
    return SellerResponse.model_validate(seller, from_attributes=True)

