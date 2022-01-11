# Recycle 视图
from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sql_models.DocumentManagement.OrmDocumentManagement import DocumentManagement
from sql_models.db_config import db_session

from app.DocumentManagement.schemas import SearchDocumentManagement

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


@recycle_router.get('/')
async def get_recycle_page(query: SearchDocumentManagement = Depends(SearchDocumentManagement),
                           dbs: AsyncSession = Depends(db_session)):
    """
    默认获取回收站第一页内容，默认显示10条
    """
    filter_condition = [
        ("filename", f'.like(f"%{query.filename}%")', query.filename),
        # ("filename",f'.like(f"%{query.filename}%")',query.filename),
        ("created_time", f'>"{query.start_time}"', query.start_time),
        ("created_time", f'<"{query.end_time}"', query.end_time),
        ("is_delete", '==1', 1),
    ]

    result, count, total_page = await DocumentManagement.get_all_detail_page(dbs, query.page, query.page_size,
                                                                             *filter_condition)
    response_json = {"total": count,
                     "page": query.page,
                     "page_size": query.page_size,
                     "total_page": total_page,
                     "data": result}
    return response_json


@recycle_router.get('/recover')
async def get_recycle_page(file_id: int, dbs: AsyncSession = Depends(db_session)):
    """
    恢复功能
    """
    file = await DocumentManagement.get_one_detail(dbs, file_id)
    file.is_delete = 0
    await dbs.flush()
    await dbs.commit()
