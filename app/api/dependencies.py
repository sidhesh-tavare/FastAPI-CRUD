from typing import Annotated
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_session
from app.api.services.product import ProductService
from app.api.services.sellers import SellerService

SessionDep = Annotated[AsyncSession,Depends(get_session)]

def get_product_service(session:SessionDep):
    return ProductService(session)

ProductDep = Annotated[ProductService,Depends(get_product_service)]

def get_seller_service(session:SessionDep):
    return SellerService(session)

SellerDep = Annotated[SellerService,Depends(get_seller_service)]