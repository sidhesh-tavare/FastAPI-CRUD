from typing import Annotated
from fastapi import HTTPException,status,Depends
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import Seller
from app.database.session import get_session
from app.api.services.product import ProductService
from app.api.services.sellers import SellerService
from app.core.security import oauth2_scheme
from app.utils import decode_access_token
from app.database.redis_db import check_blacklisted,blacklist_jti

SessionDep = Annotated[AsyncSession,Depends(get_session)]

def get_product_service(session:SessionDep):
    return ProductService(session)

def get_seller_service(session:SessionDep):
    return SellerService(session)

async def get_access_token(token: Annotated[str,Depends(oauth2_scheme)],)-> dict:
    data = decode_access_token(token)
  
    if data is None or await check_blacklisted(jti = data['jti']):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid access token"
        )
    return data

async def get_current_seller(
        token_data : Annotated[dict,Depends(get_access_token)],
        session: SessionDep
):
    return await session.get(Seller,token_data["user"]["id"])
    
ProductDep = Annotated[ProductService,Depends(get_product_service)]
SellerDep = Annotated[SellerService,Depends(get_seller_service)]
CurrentSellerDep = Annotated[Seller,Depends(get_current_seller)]