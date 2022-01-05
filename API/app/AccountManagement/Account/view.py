# Account 视图
from fastapi import APIRouter

account_router = APIRouter(
    prefix="/account/v1",
    responses={404: {"description": "Not found"}}, )


@account_router.get("/123")
async def read_root():
    return {"Hello": "World"}
