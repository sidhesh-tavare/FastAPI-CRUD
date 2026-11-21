from fastapi import APIRouter
from app.api.routers import products,sellers

router = APIRouter()
router.include_router(sellers.router)
router.include_router(products.router)