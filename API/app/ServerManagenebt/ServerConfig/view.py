# Server 视图
# 配置服务器

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sql_models.db_config import db_session
from typing import Optional, List
from sql_models.ServerManagement.ServerManagement import Server, ServerScript
from app.ServerManagenebt.ServerConfig.DataValidation import ServerSearch, AddServer, UpdateServer
from config import globals_config
import os

server_router = APIRouter(
    prefix="/Server/v1",
    responses={404: {"description": "Not found"}},
    tags=["Server"])


@server_router.delete("/")
async def delete_server(server_ids: List[int], dbs=Depends(db_session)):
    await Server.delete_data(dbs, server_ids)
    await ServerScript.delete_data_server_id(dbs, server_ids)
    return server_ids


@server_router.get('/')
async def server_search(search_info: ServerSearch = Depends(ServerSearch), dbs=Depends(db_session)):
    filter_condition = [
        ('name', f'.like(f"%{search_info.name}%")', search_info.name),
        ('ip_address', f'=={search_info.ip_address}', search_info.ip_address),
    ]
    result, count, total_page = await Server.get_all_detail_page(dbs, search_info.page, search_info.page_size,
                                                                 *filter_condition)
    response_json = {"total": count,
                     "page": search_info.page,
                     "page_size": search_info.page_size,
                     "total_page": total_page,
                     "data": result}
    return response_json


@server_router.get('/{server_id}')
async def get_server_one(server_id: int, dbs=Depends(db_session)):
    result = await Server.get_one_detail(dbs, server_id)
    if not result:
        raise HTTPException(status_code=404, detail="Get non-existent resources.")
    return result


@server_router.post('/')
async def add_server(server_info: AddServer = Depends(AddServer), file: Optional[UploadFile] = File(...),
                     dbs=Depends(db_session)):
    # 密钥和密码 必须要有一个存在
    if server_info.password and not file:
        password = server_info.password
    elif not server_info.password and file:
        key_name = file.filename
        content = await file.read()
        avatar_path = os.path.join(os.path.join(globals_config.basedir, 'app/ServerManagenebt/ServerConfig/key/'),
                                   key_name)
        with open(avatar_path, 'wb') as f:
            f.write(content)
    else:
        raise HTTPException(status_code=500, detail="Please fill in password or upload key.")

    # 构建新增数据
    data = {
        "name": server_info.name,
        "ip_address": server_info.ip_address,
        "password": server_info.password,
        "pass_key": key_name,
        "remark": server_info.remark,
    }
    server_id = await Server.add_data(dbs, data)
    data["server_id"] = server_id
    return data


@server_router.patch('/')
async def update_server(server_info: UpdateServer = Depends(UpdateServer), file: Optional[UploadFile] = File(...),
                        dbs=Depends(db_session)):
    if server_info.password and not file:
        password = server_info.password
    elif not server_info.password and file:
        key_name = file.filename
        content = await file.read()
        avatar_path = os.path.join(os.path.join(globals_config.basedir, 'app/ServerManagenebt/ServerConfig/key/'),
                                   key_name)
        with open(avatar_path, 'wb') as f:
            f.write(content)
    else:
        raise HTTPException(status_code=500, detail="Please fill in password or upload key.")

    # 构建新增数据
    update_data_dict = {
        "name": server_info.name,
        "ip_address": server_info.ip_address,
        "password": server_info.password,
        "pass_key": key_name,
        "remark": server_info.remark,
    }
    if len(update_data_dict) > 1:
        result = await Server.update_data(dbs, update_data_dict, is_delete=0)
        if not result:
            raise HTTPException(status_code=403, detail="User does not exist.")
    response_json = {"data": update_data_dict}
    return response_json
