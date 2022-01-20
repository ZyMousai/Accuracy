# Documents 视图
from fastapi import APIRouter, Depends, Query, File, UploadFile
from typing import Optional, List
from sql_models.db_config import db_session
from datetime import datetime
from sql_models.DocumentManagement.OrmDocumentManagement import DocumentManagement
from app.DocumentManagement.schemas import SearchDocumentManagement
from sqlalchemy.ext.asyncio import AsyncSession
from config import globals_config
import os

documents_router = APIRouter(
    prefix="/documents/v1",
    responses={404: {"description": "Not found"}}, )


@documents_router.get('/')
async def get_docs_page(query: SearchDocumentManagement = Depends(SearchDocumentManagement),
                        dbs: AsyncSession = Depends(db_session)):
    """
    默认获取文档页当前第一页数据
    """
    filter_condition = [
        ("filename", f'.like(f"%{query.filename}%")', query.filename),
        # ("filename",f'.like(f"%{query.filename}%")',query.filename),
        ("created_time", f'>"{query.start_time}"', query.start_time),
        ("created_time", f'<"{query.end_time}"', query.end_time),
        ("is_delete", '==0', 0),
    ]

    result, count, total_page = await DocumentManagement.get_all_detail_page(dbs, query.page, query.page_size,
                                                                             *filter_condition)
    response_json = {"total": count,
                     "page": query.page,
                     "page_size": query.page_size,
                     "total_page": total_page,
                     "data": result}
    return response_json


@documents_router.get('/{fileid}')
async def get_doc_one(file_id: int, dbs: AsyncSession = Depends(db_session)):
    """
    根据file的id来获取对应数据
    """
    return await DocumentManagement.get_one_detail(dbs, file_id)


# @documents_router.get('/search')
# async def get_demo(filename: str, start_time: str, end_time: str, user_name: str,
#                    dbs: AsyncSession = Depends(db_session)):
#     _orm = select(DocumentManagement).where(DocumentManagement.filename == filename)
#     result: DocumentManagement = (await dbs.execute(_orm)).scalars().first()
#     return result


@documents_router.delete('/')
async def delete_doc(ids: List[int] = Query(...),
                     is_logic_del: int = Query(ge=0, le=1, default=0),
                     dbs: AsyncSession = Depends(db_session, use_cache=True)):
    """
    逻辑删除和真实删除
    """
    if is_logic_del:
        return await DocumentManagement.delete_data_logic(dbs, ids)
    else:
        for doc_id in ids:
            doc_info = await DocumentManagement.get_one_detail(dbs, doc_id)
            filename = doc_info.filename
            os.remove(os.path.join(globals_config.DocumentStoragePath, filename))
        return await DocumentManagement.delete_data(dbs, ids)


@documents_router.post('/upload')
async def upload_doc(user_id: int, files: List[UploadFile] = File(...), dbs: AsyncSession = Depends(db_session)):
    """
    文件上传
    """
    for idx, f in enumerate(files):
        filename = f.filename
        content = await f.read()
        file_size = str(float('%.2f' % (len(content) / 1024 / 1024))) + "M"
        created_time = datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
        doc_model = DocumentManagement(filename=filename, file_size=file_size, user_id=user_id,
                                       created_time=created_time)
        dbs.add(doc_model)
        await dbs.flush()
        with open(os.path.join(globals_config.DocumentStoragePath, f.filename), "wb") as w:
            w.write(content)
    await dbs.commit()


# @documents_router.post('/')
# async def update_doc(ids: Optional[List[int]] = Query(...),
#                      is_logicdel: int = Query(ge=0, le=1, default=0),
#                      dbs: AsyncSession = Depends(db_session)):
#     if is_logicdel:
#         return await DocumentManagement.delete_data_logic(dbs, ids)
#     else:
#         return await DocumentManagement.delete_data(dbs, ids)
