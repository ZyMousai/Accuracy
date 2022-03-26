import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from dingtalkchatbot.chatbot import DingtalkChatbot
import time, hmac, urllib, hashlib, base64
from app.Clerk.Scheduler.DataValidation import Alarm, DelAlarm, SearchJob
from fastapi import APIRouter, Depends
from config import globals_config

clerk_scheduler_router = APIRouter(
    prefix="/heartbeat/v1",
    responses={404: {"heartbeat": "Not found"}},
    tags=["heartbeat"]
)

heartbeat_scheduler = BackgroundScheduler(SCHEDULER_API_ENABLED=True)
heartbeat_scheduler.start()


@clerk_scheduler_router.get('/')
async def get_job(info: SearchJob = Depends(SearchJob)):
    """
        获取想传入计划任务的id是否存在
    param info:

        job_id: 想查找的任务名

    return:

        data: 任务存不存在的信息

    """
    if heartbeat_scheduler.get_job(info.job_id):
        return {"exist": True, "data": info.job_id + ", current id exists"}
    else:
        return {"exist": False, "data": info.job_id + ", current id does not exist"}


@clerk_scheduler_router.post('/')
async def exposed_add_job(info: Alarm):
    """
        创建告警的计划任务，传入相同任务名会自动延期
    param info:

        job_id: 任务名
        alarm_time: 任务最长没有心跳时间，超过这个时间则报警


    """
    job_id = info.job_id
    now_time = datetime.datetime.now()
    alarm_time = now_time + datetime.timedelta(seconds=info.alarm_time)  # 告警时间(到此时间未接到下次心跳来重置告警就报警)
    # 获取当前任务是否存在
    if heartbeat_scheduler.get_job(job_id):
        # 重新赋予当前任务告警时间
        heartbeat_scheduler.reschedule_job(job_id, trigger='date', run_date=alarm_time)
    else:
        # 创建告警任务
        alarm_content = "心跳故障: " + job_id + " 在设置时间" + str(info.alarm_time) + "秒内，未发出心跳"  # 告警内容
        heartbeat_scheduler.add_job(id=job_id, func=dingding, args=[alarm_content], trigger='date', run_date=alarm_time)
    response_json = {"data": job_id + " timed task created successfully"}
    return response_json


@clerk_scheduler_router.delete('/')
async def del_job(info: DelAlarm):
    """
        删除告警计划任务
    param info:

        job_id: 要删除的任务名
    """
    heartbeat_scheduler.remove_job(info.job_id)
    response_json = {"data": info.job_id + " successfully deleted"}
    return response_json


def dingding(alarm_content):
    timestamp = str(round(time.time() * 1000))
    try:
        urlToken = globals_config.urlToken  # 钉钉群机器人Webhook
        secret = globals_config.secret  # 钉钉群机器人secret
    except:
        raise Exception("config.py folder has no urlToken or secret fields")
    string_to_sign_enc = '{}\n{}'.format(timestamp, secret).encode('utf-8')
    hmac_code = hmac.new(secret.encode('utf-8'), string_to_sign_enc, digestmod=hashlib.sha256).digest()
    SignMessage = urlToken + "&timestamp=" + timestamp + "&sign=" + urllib.parse.quote_plus(base64.b64encode(hmac_code))
    xiaoDing = DingtalkChatbot(SignMessage)  # 初始化机器人
    xiaoDing.send_markdown(title="心跳消失", text=alarm_content)
