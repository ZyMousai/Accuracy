import uvicorn
# import aioredis
from starlette.responses import JSONResponse
from fastapi import FastAPI, Request
from initialize import init_app
from app.PersonnelManagement.Users.permissions import Permissions
from sql_models.db_config import async_session_local

app = FastAPI(title="Accuracy",
              version="1.0")

# 初始化app
init_app(app)


@app.get("/")
async def read_root():
    return {"Hello": "Accuracy"}


# 中间件
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    # 请求校验
    # path = str(request.url.path)
    # if path == '/api/PersonnelManagement/users/v1/login' \
    #         or path == '/docs' or path == '/redocs' or path == '/openapi.json':
    #     pass
    # else:
    #     try:
    #         # 验证token
    #         token = request.headers.get('Authorization')
    #         assert token, "Can't get Authorization."
    #         payload = await Permissions.verify(token)
    #         request.state.user_id = payload.get("user_id")
    #         request.state.account =  payload.get("account")
    #         request.state.username =  payload.get("username")
    #         request.state.role_id =  payload.get("role_id")
    #         request.state.role =  payload.get("role")
    #         # todo 鉴权
    #     except Exception as e:
    #         return JSONResponse(status_code=401, content={"detail": str(e)})

    response = await call_next(request)
    return response


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


if __name__ == '__main__':
    uvicorn.run('main:app', host="0.0.0.0", port=8000, reload=True)
