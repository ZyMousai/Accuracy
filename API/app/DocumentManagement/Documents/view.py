# Documents 视图
from fastapi import APIRouter, Depends, Query, File, UploadFile, Path, HTTPException
from typing import Optional, List
from sql_models.db_config import db_session
from datetime import datetime
from sql_models.DocumentManagement.OrmDocumentManagement import DocumentManagement
from app.DocumentManagement.schemas import *
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
        ("department_id", f'=={query.department_id}', query.department_id),
    ]

    result, count, total_page = await DocumentManagement.get_all_detail_page(dbs, query.page, query.page_size,
                                                                             *filter_condition)
    for i in result:
        i.created_time = i.created_time.strftime("%Y-%m-%d")
    response_json = {"total": count,
                     "page": query.page,
                     "page_size": query.page_size,
                     "total_page": total_page,
                     "data": result}
    return response_json


@documents_router.get('/{fileid}')
async def get_doc_one(file_id: int = Path(..., description='文件id', ge=1), dbs: AsyncSession = Depends(db_session)):
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
async def delete_doc(ids: Optional[List[int]] = Query(...),
                     is_logic_del: int = Query(ge=0, le=1, default=0),
                     dbs: AsyncSession = Depends(db_session)):
    """
    逻辑删除和真实删除
    """
    if is_logic_del:
        return await DocumentManagement.delete_data_logic(dbs, ids)
    else:
        for doc_id in ids:
            doc_info = await DocumentManagement.get_one_detail(dbs, doc_id)
            filename = doc_info.filename
            try:
                os.remove(os.path.join(globals_config.DocumentStoragePath, filename))
            except:
                print('可能是文件未同步导致的删除失败')
        return await DocumentManagement.delete_data(dbs, ids)


@documents_router.post('/upload')
async def upload_doc(user_id: int, department_id: str, files: List[UploadFile] = File(...),
                     dbs: AsyncSession = Depends(db_session)):
    """
    文件上传
    """
    for idx, f in enumerate(files):
        filename = f.filename
        filter_condition = [
            ('filename', f'=="{filename}"', filename)
        ]
        result = await DocumentManagement.get_one(dbs, *filter_condition)
        if result:
            raise HTTPException(status_code=403, detail="Duplicate filename.")
        content = await f.read()
        file_size = str(float('%.2f' % (len(content) / 1024 / 1024))) + "M"
        created_time = datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
        doc_model = DocumentManagement(filename=filename, file_size=file_size, user_id=user_id,
                                       department_id=department_id,
                                       created_time=created_time)
        dbs.add(doc_model)
        await dbs.flush()
        with open(os.path.join(globals_config.DocumentStoragePath, f.filename), "wb") as w:
            w.write(content)
    await dbs.commit()
    return {'file_name': [file.filename for file in files]}


@documents_router.patch('/')
async def update_doc(info: UpdateDocumentManagement = Depends(UpdateDocumentManagement),
                     dbs: AsyncSession = Depends(db_session)):
    """
    修改文档部门id
    :param info:
    :param dbs:
    :return:
    """
    update_data_dict = info.dict(exclude_unset=True)
    if len(update_data_dict) > 1:
        result = await DocumentManagement.update_data(dbs, update_data_dict, is_delete=0)
        if not result:
            raise HTTPException(status_code=403, detail="card does not exist.")
    response_json = {"data": update_data_dict}
    return response_json
