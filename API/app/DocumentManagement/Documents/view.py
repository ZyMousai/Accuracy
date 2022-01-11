# Documents 视图
from fastapi import APIRouter, Depends, Query, File, UploadFile
from fastapi_pagination import Page, add_pagination
from typing import Union, Optional, List
from sql_models.db_config import db_session
from datetime import datetime
from sql_models.DocumentManagement.OrmDocumentManagement import DocumentManagement
from app.DocumentManagement.schemas import DocumentManagementModel
from sqlalchemy.ext.asyncio import AsyncSession
from config import GlobalsConfig
import os

documents_router = APIRouter(
    prefix="/documents/v1",
    responses={404: {"description": "Not found"}}, )


async def query_parm(filename: Optional[str] = None, start_time: Optional[str] = None, end_time: Optional[str] = None,
                     user_name: Optional[str] = None):
    return {"filename": filename, "start_time": start_time, "end_time": end_time,
            "user_name": user_name}


@documents_router.get('/', response_model=Page[DocumentManagementModel])
async def get_docs_page(query: dict = Depends(query_parm), dbs: AsyncSession = Depends(db_session)):
    return await DocumentManagement.search(query, dbs)


@documents_router.get('/{fileid}')
async def get_doc_one(fileid: int, dbs: AsyncSession = Depends(db_session)):
    return await DocumentManagement.get_one_detail(dbs, fileid)


# @documents_router.get('/search')
# async def get_demo(filename: str, start_time: str, end_time: str, user_name: str,
#                    dbs: AsyncSession = Depends(db_session)):
#     _orm = select(DocumentManagement).where(DocumentManagement.filename == filename)
#     result: DocumentManagement = (await dbs.execute(_orm)).scalars().first()
#     return result

@documents_router.delete('/')
async def delete_doc(ids: Optional[List[int]] = Query(...),
                     is_logicdel: int = Query(ge=0, le=1, default=0),
                     dbs: AsyncSession = Depends(db_session)):
    if is_logicdel:
        return await DocumentManagement.delete_data_logic(dbs, ids)
    else:
        for doc_id in ids:
            doc_info = await DocumentManagement.get_one_detail(dbs, doc_id)
            filename = doc_info.filename
            os.remove(os.path.join(GlobalsConfig.DocumentStoragePath, filename))
        return await DocumentManagement.delete_data(dbs, ids)


@documents_router.post('/upload')
async def upload_doc(user_id: int, files: List[UploadFile] = File(...), dbs: AsyncSession = Depends(db_session)):
    '''
    :param files:
    :param dbs:
    :return:
    '''
    for idx, f in enumerate(files):
        filename = f.filename
        content = await f.read()
        filesize = str(float('%.2f' % (len(content) / 1024 / 1024))) + "M"
        created_time = datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
        doc_model = DocumentManagement(filename=filename, filesize=filesize, user_id=user_id, created_time=created_time)
        dbs.add(doc_model)
        await dbs.flush()
        with open(os.path.join(GlobalsConfig.DocumentStoragePath, f.filename), "wb") as w:
            w.write(content)
    await dbs.commit()


@documents_router.post('/')
async def update_doc(ids: Optional[List[int]] = Query(...),
                     is_logicdel: int = Query(ge=0, le=1, default=0),
                     dbs: AsyncSession = Depends(db_session)):
    if is_logicdel:
        return await DocumentManagement.delete_data_logic(dbs, ids)
    else:
        return await DocumentManagement.delete_data(dbs, ids)


# 加载分页类
add_pagination(documents_router)
