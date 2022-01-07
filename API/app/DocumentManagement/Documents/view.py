# Documents 视图
from fastapi import APIRouter, Depends
from sqlalchemy import select
from typing import Union, Optional
from sql_models.db_config import db_session
from sql_models.DocumentManagement.OrmDocumentManagement import DocumentManagement
from sqlalchemy.ext.asyncio import AsyncSession

documents_router = APIRouter(
    prefix="/documents/v1",
    responses={404: {"description": "Not found"}}, )


@documents_router.get('/{fileid}')
async def get_demo(fileid: int, dbs: AsyncSession = Depends(db_session)):
    return await DocumentManagement.get_one_detail(dbs, fileid)


# @documents_router.get('/search')
# async def get_demo(filename: str, start_time: str, end_time: str, user_name: str,
#                    dbs: AsyncSession = Depends(db_session)):
#     _orm = select(DocumentManagement).where(DocumentManagement.filename == filename)
#     result: DocumentManagement = (await dbs.execute(_orm)).scalars().first()
#     return result
