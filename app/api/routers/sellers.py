from fastapi import APIRouter
from ..schemas.sellers import SellerCreate,SellerRead
from app.api.dependencies import SellerDep
from app.database.models import Seller

router = APIRouter(prefix='/sellers',tags=['sellers'])

@router.post("/signup")
async def register_seller(seller:SellerCreate,service:SellerDep)->Seller:
    return await service.add_seller(seller)