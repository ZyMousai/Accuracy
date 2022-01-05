# Roles 视图
from fastapi import APIRouter

roles_router = APIRouter(
    prefix="/roles/v1",
    responses={404: {"description": "Not found"}}, )


@roles_router.get("/123")
async def read_root():
    return {"Hello": "World"}
