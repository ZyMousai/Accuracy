# Documents 视图
import os
from datetime import datetime
from typing import Optional, List, Any

from fastapi import APIRouter, Depends, Query, File, UploadFile, Path, HTTPException
from starlette.responses import FileResponse,StreamingResponse
from sql_models.db_config import db_session
from sql_models.DocumentManagement.OrmDocumentManagement import DocumentManagement
from app.DocumentManagement.schemas import *
from sqlalchemy.ext.asyncio import AsyncSession
from config import globals_config

documents_router = APIRouter(
    prefix="/documents/v1",
    responses={404: {"description": "Not found"}},
    tags=["DocumentManagement"])


@documents_router.get("/download/{file_name}")
async def download_file(file_name: Any):
    """
        下载文件

    param file_name:

        下载的文件名
    return:

        返回文件流，直接下载，下载后的文件名与显示的文件名一样。
    """
    final_file = os.path.join(globals_config.DocumentStoragePath, file_name)

    def iterfile():
        # 通过使用 with 块，确保在生成器函数完成后关闭类文件对象
        with open(final_file, "rb") as file_like:
            # yield from 告诉函数迭代名为 file_like 的东西
            # 对于迭代的每个部分，yield 的内容作为来自这个生成器函数
            yield from file_like

    return StreamingResponse(iterfile())


@documents_router.get('/')
async def get_docs_page(query: SearchDocumentManagement = Depends(SearchDocumentManagement),
                        dbs: AsyncSession = Depends(db_session)):
    """
        默认获取文档页当前第一页数据,也可根据条件获取所有文档信息

    param query:

        对应文档搜索的参数

    param dbs:

        数据库依赖

    return:

        返回分页信息，重新渲染后的文档的参数

    """
    # 站点域名和端口配置
    filter_condition = [
        ("filename", f'.like(f"%{query.filename}%")', query.filename),
        # ("filename",f'.like(f"%{query.filename}%")',query.filename),
        ("created_time", f'>="{query.start_time}"', query.start_time),
        ("created_time", f'<="{query.end_time}"', query.end_time),
        ("is_delete", '==0', 0),
        ("department_id", f'=={query.department_id}', query.department_id),
    ]

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
            "is_delete": False,
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


@documents_router.get('/{file_id}')
async def get_doc_one(file_id: int = Path(..., description='文件id', ge=1), dbs: AsyncSession = Depends(db_session)):
    """
        默认获取文档页当前第一页数据

    param query:

        对应文档搜索的参数

    param dbs:

        数据库依赖

    return:

        返回分页信息，重新渲染后的文档的参数

    """
    result = await DocumentManagement.get_one_detail(dbs, file_id)
    if not result:
        raise HTTPException(status_code=404, detail="Get non-existent resources.")
    response_json = {"data": result}
    return response_json


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

    param ids:

        需要删除的文档id

    param is_logic_del:

        逻辑删除的参数，1就是逻辑删除，0就是真实删除

    param dbs:

        数据库依赖

    return:

        删除的文档的id
    """
    if is_logic_del:
        # 更新逻辑删除的时间

        for doc_id in ids:
            update_data_dict = {
                "id": doc_id,
                "updated_time": datetime.now()
            }
            await DocumentManagement.update_data(dbs, update_data_dict, is_delete=0)

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
async def upload_doc(user_id: int, department_id: int, files: List[UploadFile] = File(...),
                     dbs: AsyncSession = Depends(db_session)):
    """
        文件上传

    param user_id:

        上传人的id

    param department_id:

        上传人的部门id

    param files:

        上传的文件

    param dbs:

        数据库依赖

    return:

        上传的文件名
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

        size = len(content) / 1024
        if size > 1024:
            file_size = str(float('%.2f' % (len(content) / 1024 / 1024))) + "M"
        else:
            file_size = str(float('%.2f' % (len(content) / 1024))) + "KB"

        created_time = datetime.strptime(datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d')
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
async def update_doc(info: UpdateDocumentManagement,
                     dbs: AsyncSession = Depends(db_session)):
    """
        修改文档的信息

    param info:

        文件修改信息参数

    param dbs:

        数据库依赖

    return:

        更新文档后文档的内容参数
    """
    update_data_dict = info.dict(exclude_unset=True)
    if len(update_data_dict) > 1:
        result = await DocumentManagement.update_data(dbs, update_data_dict, is_delete=0)
        if not result:
            raise HTTPException(status_code=403, detail="card does not exist.")
    response_json = {"data": update_data_dict}
    return response_json
