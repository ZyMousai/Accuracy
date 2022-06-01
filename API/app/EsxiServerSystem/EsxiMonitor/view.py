from starlette.responses import StreamingResponse
from config import globals_config
from sql_models.Clerk.OrmSchedulerHeartbeat import Machine
from fastapi import APIRouter, Depends, HTTPException, Query
import paramiko
import os
from app.EsxiServerSystem.EsxiMonitor.spider import EsxiSpider
from sql_models.db_config import db_session

esxi_sys_router = APIRouter(
    prefix="/EsxiSystem/v1",
    responses={404: {"description": "Not found"}},
    tags=["EsxiSystem"])


@esxi_sys_router.get('/all')
async def get_machine_all(dbs=Depends(db_session)):
    result = await Machine.get_all(dbs, *[("is_delete", '==0', 0)])
    response_json = {"data": result}
    return response_json


@esxi_sys_router.get('/restart')
async def vm_restart(hostname: str, vmid: int, dbs=Depends(db_session)):
    result = await esxi_restart(vmid, hostname)
    response_json = {"data": result, "status_code": 200}
    return response_json


# 虚拟机重启
async def esxi_restart(vmid, hostname, username="dingzj", pwd="Ff!4242587"):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hostname, port=22, username=username, password=pwd)
    cmd_shutdown = "vim-cmd vmsvc/power.reset " + str(vmid) + " && echo " + vmid + " success"
    stdin, stdout, stderr = ssh.exec_command(cmd_shutdown)
    cmd_result = stdout.read()
    print(cmd_result)
    ssh.close()
    return cmd_result


@esxi_sys_router.get('/')
async def get_host_img_all(hostname: str, dbs=Depends(db_session)):
    es = EsxiSpider(hostname)
    es.spider_esxi_monitor_img()
    machine_code_list = es.get_esxi_machine()
    response_json = {"data": machine_code_list}
    return response_json


@esxi_sys_router.get('/esxiimg/{esxi_img_name}')
async def get_avatar(esxi_img_name: str = Query(...)):
    esxiimg_file = os.path.join(globals_config.basedir, 'app/EsxiServerSystem/EsxiImg', esxi_img_name)
    if not os.path.exists(esxiimg_file):
        raise HTTPException(status_code=404, detail="image not found !")

    file_like = open(esxiimg_file, mode="rb")
    return StreamingResponse(file_like, media_type="image/jpg")
