# Recycle 视图
import os
from typing import Optional, List, Union
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from config import globals_config
from sql_models.DocumentManagement.OrmDocumentManagement import DocumentManagement
from sql_models.db_config import db_session

from app.DocumentManagement.schemas import SearchDocumentManagement

recycle_router = APIRouter(
    prefix="/recycle/v1",
    responses={404: {"description": "Not found"}},
    tags=["Recycle"])


async def query_parm(filename: Optional[str] = None, start_time: Optional[str] = None, end_time: Optional[str] = None,
                     user_name: Optional[str] = None):
    return {"filename": filename, "start_time": start_time, "end_time": end_time,
            "user_name": user_name}


# @recycle_router.get("/123")
# async def read_root():
#     return {"Hello": "World"}


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
    user_id = None
    if query.user_name:
        user_id = await DocumentManagement.get_document_user_id(dbs,query.user_name)
    filter_condition = [
        ("user_id", f'.like(f"%{user_id}%")', user_id),
        ("created_time", f'>="{query.start_time}"', query.start_time),
        ("created_time", f'<="{query.end_time}"', query.end_time),
        ("is_delete", '==1', 1),
        ("department_id", f'=={query.department_id}', query.department_id)
    ]
    first_result = await DocumentManagement.get_all(dbs, *filter_condition)
    # 要清除的文件
    clear_list = []
    for res in first_result:
        # 超过14天的回收站文件直接清除
        remain_hours = str((datetime.now() - res.updated_time)).split(":")[0]
        # noinspection PyBroadException
        try:
            if int(remain_hours) >= 336:
                clear_list.append(res.id)
        except Exception as e:
            if "days" in remain_hours:
                clear_list.append(res.id)
    await DocumentManagement.delete_data(dbs, clear_list)
    result, count, total_page = await DocumentManagement.get_all_detail_page(dbs, query.page, query.page_size,
                                                                             *filter_condition)
    # 对文档数据进行重新归纳赋值
    new_result = []
    for res in result:
        uploader_name = await DocumentManagement.get_document_user(dbs, res.user_id)
        new_res = {
            "filename": res.filename,
            "id": res.id,
            "user_id": res.user_id,
            "is_delete": res.is_delete,
            "created_time": res.created_time.strftime("%Y-%m-%d"),
            "file_size": res.file_size,
            "updated_time": res.updated_time,
            "department_id": res.department_id,
            "uploader_name": uploader_name,
        }
        new_result.append(new_res)
    response_json = {"total": count,
                     "page": query.page,
                     "page_size": query.page_size,
                     "total_page": total_page,
                     "data": new_result,
                     }
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


@recycle_router.delete('/')
async def delete_doc(ids: List[int] = Query(...),
                     dbs: AsyncSession = Depends(db_session)):
    """
    真实删除
    """
    for doc_id in ids:
        doc_info = await DocumentManagement.get_one_detail(dbs, doc_id)
        filename = doc_info.filename
        try:
            os.remove(os.path.join(globals_config.DocumentStoragePath, filename))
        except Exception as e:
            print('可能是文件未同步导致的删除失败')
    return await DocumentManagement.delete_data(dbs, ids)
