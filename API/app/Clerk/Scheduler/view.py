import datetime
import json
import time
import hmac
import urllib
import hashlib
import base64
from apscheduler.schedulers.background import BackgroundScheduler
# from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from dingtalkchatbot.chatbot import DingtalkChatbot
from app.Clerk.Scheduler.DataValidation import Alarm, SearchJob, DisplaySearchJob, DisplayAddJob, DisplayUpdateJob
from config import MysqlConfig, globals_config
from sql_models.Clerk.OrmSchedulerHeartbeat import Heartbeat
from sqlalchemy.ext.asyncio import AsyncSession
from sql_models.db_config import db_session
from fastapi import APIRouter, Depends, HTTPException
from fastapi import Query
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from typing import List
from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from queue import Queue
from util.crypto import decrypt
# 系统管理 - 心跳功能
clerk_scheduler_router = APIRouter(
    prefix="/heartbeat/v1",
    responses={404: {"heartbeat": "Not found"}},
    tags=["heartbeat"]
)
MYSQL_URL = f"mysql+pymysql://{MysqlConfig.username}:{MysqlConfig.password}@{MysqlConfig.host}:" \
            f"{MysqlConfig.port}/{MysqlConfig.db}?charset=utf8"
# MYSQL_URL = f"mysql+pymysql://root:root@127.0.0.1:3306/{MysqlConfig.db}?charset=utf8"
# 执行器
job_stores = {'default': SQLAlchemyJobStore(url=MYSQL_URL)}
executors = {'default': ThreadPoolExecutor(20), 'processpool': ProcessPoolExecutor(5)}
job_defaults = {'coalesce': True, 'max_instances': 20}
# heartbeat_scheduler = AsyncIOScheduler(
heartbeat_scheduler = BackgroundScheduler(
    timezone="Asia/Shanghai",
    jobstores=job_stores,
    job_defaults=job_defaults,
    executors=executors
)
heartbeat_scheduler.start()
loop_detection_scheduler = BackgroundScheduler(timezone="Asia/Shanghai", job_defaults=job_defaults,
                                       SCHEDULER_API_ENABLED=True)
engine = create_engine(MYSQL_URL, encoding='utf-8')
# autocommit：是否自动提交 autoflush：是否自动刷新并加载数据库 bind：绑定数据库引擎
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# 实例化
session = Session()
# 报警队列
heartbeat_q = Queue()


@clerk_scheduler_router.get('/')
async def get_job(info: SearchJob = Depends(SearchJob)):
    """
        获取想传入计划任务的id是否存在
    param info:

        job_name: 想查找的任务名

    return:

        data: 任务存不存在的信息

    """
    if heartbeat_scheduler.get_job(info.job_name):
        return {"exist": True, "data": info.job_name + ", current id exists"}
    else:
        return {"exist": False, "data": info.job_name + ", current id does not exist"}


@clerk_scheduler_router.post('/')
async def exposed_add_job(info: Alarm, dbs: AsyncSession = Depends(db_session)):
    """
        创建告警的计划任务，传入相同任务名会自动延期
    param info:

        key: 加密的数据，里面包含：
            - job_name: 任务名
            - alarm_time: 任务最长没有心跳时间，超过这个时间则报警

    """
    try:
        data = info.key.encode('utf8')
        data = json.loads(decrypt(data))
    except ValueError:
        return {"data": "illegal data"}
    if "job_name" not in data or "interval" not in data:
        return {"data": "data field error"}
    job_name = data["job_name"]
    interval = data["interval"]
    now_time = datetime.datetime.now()

    # 获取当前任务是否存在
    # if heartbeat_scheduler.get_job(job_name):
    #     # 修改当前任务告警时间
    #     heartbeat_scheduler.reschedule_job(job_name, trigger='date', run_date=alarm_time)
    # else:
    #     # 创建告警任务
    #     heartbeat_scheduler.add_job(id=job_name, func=dingding, args=[alarm_content], trigger='date',
    #                                 run_date=alarm_time)

    try:
        filter_condition = [
            ('job_name', f'=="{job_name}"', job_name)
        ]
        data_result = await Heartbeat.get_one(dbs, *filter_condition)
        if not data_result:
            # # 当数据库中没有这条数据时新增
            # data = {
            #     "job_name": job_name,
            #     "create_time": now_time,
            #     "last_heartbeat": now_time,
            #     "heartbeat_alarm": alarm_time,
            #     "alarm": 0,
            #     "state": 0,
            # }
            # await Heartbeat.add_data(dbs, data)
            # 当数据库中没有这条数据时
            return {"data": "Unknown task, this task name is not registered"}
        else:
            # 当数据库中有这条数据时，检查是否需要检测（alarm）
            if data_result.alarm == 0:
                return {"data": "This task does not need to be run"}
            interval = data_result.interval
            job_id = data_result.id
            at = data_result.at
            data = {
                "id": job_id,
                "last_heartbeat": now_time,
                "state": 0,
                # "heartbeat_alarm": alarm_time,
            }
            await Heartbeat.update_data(dbs, data, is_delete=0)
    except Exception as ex:
        print(ex)
        at = "all"
    # 告警时间(到此时间未接到下次心跳来重置告警就报警)
    alarm_time = now_time + datetime.timedelta(seconds=(interval * 60))
    # alarm_time = now_time + datetime.timedelta(seconds=10)
    print(alarm_time)
    heartbeat_scheduler.add_job(id=job_name, func=trigger_an_alarm, args=[job_name, interval, at],
                                trigger='date', run_date=alarm_time,  # 执行时间
                                replace_existing=True,  # 有就覆盖
                                # coalesce=True  # 忽略服务器宕机时间段内的任务执行(否则就会出现服务器恢复之后一下子执行多次任务的情况)
                                )
    response_json = {"data": job_name + " timed task created successfully"}
    return response_json


def loop_detection():
    loop_li = []
    job_names = []
    # 获取队列里所有要报警的任务数据
    while not heartbeat_q.empty():
        loop_li.append(heartbeat_q.get())
    if loop_li:
        loop_di = {}  # 要发送钉钉数据的name和限制的时长
        at_di = {}  # 要发送钉钉的@人
        # 对数据摘取
        for loop in loop_li:
            # 同一时长的分入一类一起报警
            # 对名称分类
            if loop[1] in loop_di:
                loop_di[loop[1]].append(loop[0])
            else:
                loop_di[loop[1]] = [loop[0]]
            # 对需@人分类
            if loop[2]:
                if loop[1] in at_di:
                    at_di[loop[1]] = at_di[loop[1]] + "," + loop[2]
                else:
                    at_di[loop[1]] = loop[2]
            job_names.append(loop[0])

        # 发送钉钉
        for k, v in loop_di.items():
            alarm_content = "心跳故障: " + str(v) + " 在设置时间 " + str(k) + " 分钟内，未发出心跳"  # 告警内容
            stamp = str(round(time.time() * 1000))
            try:
                url_token = globals_config.urlToken  # 钉钉群机器人Webhook
                secret = globals_config.secret  # 钉钉群机器人secret
            except Exception as ex:
                print(ex)
                raise Exception("config.py folder has no url_token or secret fields")
            string_to_sign_enc = '{}\n{}'.format(stamp, secret).encode('utf-8')
            hm_code = hmac.new(secret.encode('utf-8'), string_to_sign_enc, digestmod=hashlib.sha256).digest()
            sign_me = url_token + "&timestamp=" + stamp + "&sign=" + urllib.parse.quote_plus(base64.b64encode(hm_code))
            xiao_ding = DingtalkChatbot(sign_me)  # 初始化机器人

            # 判断需@人
            if k in at_di:
                if "all" in at_di[k]:
                    xiao_ding.send_markdown(title="心跳消失", text=alarm_content, is_auto_at=True)  # @所有人
                else:
                    # 对要@的人去空格去重去空
                    at = list(set(at_di[k].replace(" ", "").split(",")))
                    while "" in at:
                        at.remove("")
                    xiao_ding.send_markdown(title="心跳消失", text=alarm_content, at_mobiles=at)  # @个人
            else:
                xiao_ding.send_markdown(title="心跳消失", text=alarm_content)

        try:
            hears = session.query(Heartbeat).filter(Heartbeat.job_name.in_(job_names)).all()
            if hears:
                for he in hears:
                    he.state = 1
                    he.heartbeat_alarm = datetime.datetime.now()
                session.commit()
                session.close()
                print({"code": "0000", "message": str(job_names) + "修改成功"})
            else:
                print({"code": "0001", "message": str(job_names) + "参数错误"})
        except ArithmeticError:
            print({"code": "0002", "message": str(job_names) + "数据库错误"})


# 定时刷新库里的campaign信息
loop_detection_scheduler.add_job(id="loop_detection", func=loop_detection, trigger="interval", seconds=5)
loop_detection_scheduler.start()


def trigger_an_alarm(job_name, interval, at):
    heartbeat_q.put([job_name, interval, at])


@clerk_scheduler_router.get('/display')
async def get_heartbeat_display(info: DisplaySearchJob = Depends(DisplaySearchJob),
                                dbs: AsyncSession = Depends(db_session)):
    """
        获取心跳功能注册列表

    :param info:

        job_name: 名称
        start_create_time: 创建时间 开始范围
        end_create_time: 创建时间 结束范围
        alarm: 是否启用:0-否；1-是
        state: 状态:0-正常；1-异常；2-离线

    :param dbs:

        数据依赖

    :return:

        对应的映射信息，包含分页
    """
    filter_condition = [
        ('job_name', f'.like(f"%{info.job_name}%")', info.job_name),
        ("create_time", f'>="{info.start_create_time}"', info.start_create_time),
        ("create_time", f'<="{info.end_create_time}"', info.end_create_time),
        ('alarm', f'=="{info.alarm}"', info.alarm),
        ('state', f'=="{info.state}"', info.state),
        ('is_delete', '==0', 0)
    ]
    print(info.page, info.page_size)
    result, count, total_page = await Heartbeat.get_all_detail_page(dbs, info.page, info.page_size, *filter_condition)
    print(count)
    response_json = {"total": count,
                     "page": info.page,
                     "page_size": info.page_size,
                     "total_page": total_page,
                     "data": result}
    return response_json


@clerk_scheduler_router.get('/display/detail')
async def get_heartbeat_display_one(heartbeat_id: Optional[int] = Query(None), dbs: AsyncSession = Depends(db_session)):
    """
        获取某个心跳功能注册列表的信息

    :param heartbeat_id:

        列表id

    :param dbs:

        数据库依赖

    :return:

        单个列表的信息
    """
    result = await Heartbeat.get_one_detail(dbs, heartbeat_id)
    if not result:
        raise HTTPException(status_code=404, detail="Get non-existent resources.")
    response_json = {"data": result}
    return response_json


@clerk_scheduler_router.post('/display')
async def add_heartbeat_display(info: DisplayAddJob, dbs: AsyncSession = Depends(db_session)):
    """
        添加心跳功能注册列表

    :param info:

        添加心跳功能注册列表携带的参数

    :param dbs:

        数据库依赖

    :return:

        数据添加后在表里的id
    """
    return {"data": await Heartbeat.add_data(dbs, info)}


@clerk_scheduler_router.delete('/display')
async def del_heartbeat_display(ids: List[int] = Query(...), dbs: AsyncSession = Depends(db_session)):
    """
        删除告警计划任务
    param info:

        ids: 要删除的id
    """
    # 获取对应卡id的所有任务
    filter_condition = [
        ('id', f'.in_(' + str(ids) + ')', ids),
        ('is_delete', '==0', 0)
    ]
    task_result = await Heartbeat.get_all(dbs, *filter_condition)

    result = await Heartbeat.delete_data(dbs, tuple(ids))
    if not result:
        raise HTTPException(status_code=404, detail="Delete non-existent resources.")
    for task in task_result:
        # 删除对应任务
        try:
            heartbeat_scheduler.remove_job(task.job_name)
        except Exception as e:
            print(e)
            print("ignore delete " + task.job_name)
    response_json = {"data": str(ids) + " successfully deleted"}
    return response_json


@clerk_scheduler_router.patch('/display')
async def update_heartbeat_display(info: DisplayUpdateJob, dbs: AsyncSession = Depends(db_session)):
    """
        修改心跳功能注册列表
    param info:

        对应的需要修改的任务字段

    param dbs:

        数据库依赖

    return:

        更新后的任务的任务信息

    """
    update_data_dict = info.dict(exclude_unset=True)
    # filter_condition = [
    #     ('task', f'=="{info.task}"', info.task)
    # ]
    # result = await TbTask.get_one(dbs, *filter_condition)
    # if result:
    #     raise HTTPException(status_code=403, detail="Duplicate Task.")
    if len(update_data_dict) > 1:
        result = await Heartbeat.update_data(dbs, update_data_dict, is_delete=0)
        if not result:
            raise HTTPException(status_code=403, detail="Task does not exist.")
    response_json = {"data": update_data_dict}
    return response_json
