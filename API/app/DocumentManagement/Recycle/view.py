# Recycle 视图
from typing import Optional

from fastapi import APIRouter, Depends
from fastapi_pagination import Page, add_pagination
from sqlalchemy.ext.asyncio import AsyncSession
from sql_models.DocumentManagement.OrmDocumentManagement import DocumentManagement
from sql_models.db_config import db_session

from app.DocumentManagement.schemas import DocumentManagementModel

recycle_router = APIRouter(
    prefix="/recycle/v1",
    responses={404: {"description": "Not found"}}, )


async def query_parm(filename: Optional[str] = None, start_time: Optional[str] = None, end_time: Optional[str] = None,
                     user_name: Optional[str] = None):
    return {"filename": filename, "start_time": start_time, "end_time": end_time,
            "user_name": user_name}


@recycle_router.get("/123")
async def read_root():
    return {"Hello": "World"}


# @documents_router.get('/search')
# async def get_demo(filename: str, start_time: str, end_time: str, user_name: str,
#                    dbs: AsyncSession = Depends(db_session)):
#     _orm = select(DocumentManagement).where(DocumentManagement.filename == filename)
#     result: DocumentManagement = (await dbs.execute(_orm)).scalars().first()
#     return result


@recycle_router.get('/', response_model=Page[DocumentManagementModel])
async def get_recycle_page(query: dict = Depends(query_parm), dbs: AsyncSession = Depends(db_session)):
    """
    默认获取回收站第一页内容，默认显示50条
    """
    query['is_delete'] = 1
    return await DocumentManagement.search(query, dbs)


@recycle_router.get('/recover', response_model=Page[DocumentManagementModel])
async def get_recycle_page(file_id: int, dbs: AsyncSession = Depends(db_session)):
    """
    恢复功能
    """
    file = await DocumentManagement.get_one_detail(dbs, file_id)
    file.is_delete = 0
    await dbs.flush()
    await dbs.commit()


# 加载分页类
add_pagination(recycle_router)
