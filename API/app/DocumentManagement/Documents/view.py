# Documents 视图
from fastapi import APIRouter

documents_router = APIRouter(
    prefix="/documents/v1",
    responses={404: {"description": "Not found"}}, )


@documents_router.get("/123")
async def read_root():
    return {"Hello": "World"}
