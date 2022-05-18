# offers联盟管理
from fastapi import APIRouter

offers_union_router = APIRouter(
    prefix="/OffersUnion/v1",
    responses={404: {"description": "Not found"}},
    tags=["OffersUnion"])


@offers_union_router.get('/')
async def hi():
    return 'ok'
