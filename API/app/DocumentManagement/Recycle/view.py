# Recycle 视图
from fastapi import APIRouter

recycle_router = APIRouter(
    prefix="/recycle/v1",
    responses={404: {"description": "Not found"}}, )


@recycle_router.get("/123")
async def read_root():
    return {"Hello": "World"}
