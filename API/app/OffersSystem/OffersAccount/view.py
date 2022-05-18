# offers账号管理
from fastapi import APIRouter

offers_account_router = APIRouter(
    prefix="/OffersAccount/v1",
    responses={404: {"description": "Not found"}},
    tags=["OffersAccount"])


@offers_account_router.get('/')
async def hi():
    return 'ok'
