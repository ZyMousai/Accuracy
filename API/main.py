import uvicorn
# import aioredis
from starlette.responses import JSONResponse
from fastapi import FastAPI, Request, status

from app.Clerk.VoluumSiteId.VoluumSpider import VoluumData
from initialize import init_app, init_middleware
from app.PersonnelManagement.Users.permissions import Permissions
from apscheduler.schedulers.background import BackgroundScheduler

app = FastAPI(title="Accuracy",
              version="1.0")

# 初始化app
init_app(app)


@app.get("/")
async def read_root():
    return {"Hello": "Accuracy"}


# # 中间件
# @app.middleware("http")
# async def add_process_time_header(request: Request, call_next):
#     # # 判断不是登录接口的链接就验证token
#     path = str(request.url.path)
#     if path == '/api/PersonnelManagement/users/v1/login' \
#             or path == '/docs' or path == '/redocs' or path == '/openapi.json' \
#             or 'heartbeat' in path \
#             or 'avatar' in path \
#             or 'download' in path:
#         return await call_next(request)
#     if request.method == "OPTIONS":
#         return await call_next(request)
#     try:
#         token = request.headers["token"]
#         payload = await Permissions.verify(token)
#         request.state.user_id = payload.get("user_id")
#         request.state.account = payload.get("account")
#         request.state.username = payload.get("name")
#         request.state.role = payload.get("role")
#         request.state.role_id = payload.get("role_id")
#         # 权限验证
#         if request.state.role_id == 1:
#             return await call_next(request)
#
#         from app.PersonnelManagement.Roles.AuthPermissions import AuthPermissions
#         auth_tag = await AuthPermissions.auth(request)
#         if not auth_tag:
#             return JSONResponse(status_code=403, content={"detail": "Authorization authentication failed."})
#         response = await call_next(request)
#     except Exception as e:
#         return JSONResponse(status_code=401, content={"detail": str(e)})
#     return response


init_middleware(app)

# # 在FastAPI创建前创建Redis连接
# @app.on_event("startup")
# async def startup_event():
#     app.state.redis = await aioredis.from_url("redis://45.63.5.115", port=6379, db=3, encoding="utf-8",
#                                               password='4242587')
#     print(f"redis连接成功--->>{app.state.redis}")
#
#
# # 在FastAPI关闭时关闭Redis连接
# @app.on_event("shutdown")
# async def shutdown_event():
#     app.state.redis.close()
#     await app.state.redis.wait_closed()

# ==================分割线==================
# # 定时任务
# ax = VoluumData()
# master_scheduler = BackgroundScheduler(timezone='Pacific/Pitcairn',
#                                        job_defaults={'coalesce': True, 'misfire_grace_time': 60 * 60 * 2},
#                                        SCHEDULER_API_ENABLED=True)
# # 定时刷新库里的campaign信息
# master_scheduler.add_job(ax.add_campaign, "interval", seconds=600)
# master_scheduler.start()


if __name__ == '__main__':
    uvicorn.run('main:app', host="0.0.0.0", port=8000, reload=True)
