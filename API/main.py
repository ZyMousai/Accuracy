import uvicorn
from fastapi import FastAPI

from initialize import init_app
import aioredis
from fastapi import Request
from fastapi.security import OAuth2PasswordBearer
from app.PersonnelManagement.Users.permissions import verify, credentials_exception, create_jwt_token
from fastapi import HTTPException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

app = FastAPI(title="Accuracy",
              description='海岸跃动新项目API接口文档',
              version="1.0")

# 初始化app
init_app(app)


@app.get("/")
async def read_root():
    return {"Hello": "Accuracy"}


# 中间件
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    # 判断不是登录接口的链接就验证token
    # print(request.url.path)
    if request.url.path != '/api/PersonnelManagement/users/v1/login':
        # 获取headers里的token
        token = request.headers.get("authorization")
        if "Bearer " in token:
            token = token.replace("Bearer ", "")
        # 判断token是否有效，无效时进入redis中再检测一次
        if await verify(token):
            # 判断redis中是否存在此token
            data = await request.app.state.redis.get(token)
            if data:
                # 存在则获取到redis里此token对应的data颁发新token
                new_token = await create_jwt_token(data)
                await request.app.state.redis.set(key=new_token, value=data, seconds=24 * 60 * 60 * 3)
                # 删除老token
                await request.app.state.redis.delete(token)
                return HTTPException(status_code=200, detail=new_token)

            else:
                # 不存在则报错
                await credentials_exception()
    # 通行，运行原方法
    response = await call_next(request)
    return response


# 在FastAPI创建前创建Redis连接
@app.on_event("startup")
async def startup_event():
    app.state.redis = await aioredis.from_url("redis://127.0.0.1", port=6379, db=3, encoding="utf-8")
    print(f"redis连接成功--->>{app.state.redis}")


# 在FastAPI关闭时关闭Redis连接
@app.on_event("shutdown")
async def shutdown_event():
    app.state.redis.close()
    await app.state.redis.wait_closed()


if __name__ == '__main__':
    uvicorn.run('main:app', host="0.0.0.0", port=8000, reload=True)
