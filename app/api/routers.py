from fastapi import APIRouter

from .endpoints.order import router as order_router
from .endpoints.product import router as product_router

main_router = APIRouter()
main_router.include_router(
    product_router, prefix='/products', tags=['Products'])
main_router.include_router(
    order_router, prefix='/orders', tags=['Orders'])
