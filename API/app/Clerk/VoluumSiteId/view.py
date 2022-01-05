# VoluumSiteId 视图
from fastapi import APIRouter

voluum_router = APIRouter(
    prefix="/voluum/v1",
    responses={404: {"description": "Not found"}}, )


@voluum_router.get("/123")
async def read_root():
    return {"Hello": "World"}
