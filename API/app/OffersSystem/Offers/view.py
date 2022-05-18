# offers联盟管理
from fastapi import APIRouter

offers_router = APIRouter(
    prefix="/Offers/v1",
    responses={404: {"description": "Not found"}},
    tags=["Offers"])


@offers_router.get('/')
async def hi():
    return 'ok'
