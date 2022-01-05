# Departments 视图
from fastapi import APIRouter

departments_router = APIRouter(
    prefix="/departments/v1",
    responses={404: {"description": "Not found"}}, )


@departments_router.get("/123")
async def read_root():
    return {"Hello": "World"}
