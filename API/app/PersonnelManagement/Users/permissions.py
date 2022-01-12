from jose import jwt, JWTError
from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = "ed970259a19edf1edf1010199c7002d183bd15bc1aec612481b29bac1cb83d8137"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


async def create_jwt_token(data: dict, expire_delta: Optional[timedelta] = None):
    """
    生成token
    :param data:
    :param expire_delta:
    :return:
    """
    # 如果传入了过期时间, 那么就用该时间, 否则使用默认的时间
    expire = datetime.utcnow() + expire_delta if expire_delta else datetime.utcnow() + timedelta(seconds=30)
    # expire = datetime.utcnow() + expire_delta if expire_delta else datetime.utcnow() + timedelta(hours=24)
    # 需要加密的数据data必须为一个字典类型, 在数据中添加过期时间键值对, 键exp的名称是固定写法
    data.update({'exp': expire})
    # 进行jwt加密
    token = jwt.encode(claims=data, key=SECRET_KEY, algorithm="HS256")
    return token


async def verify(token: str):
    """
    验证token
    :param token:
    :return:
    """
    # 验证token
    try:
        # 解密token, 返回被加密的字典
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=["HS256"])
        # print(f'payload: {payload}')
        # 从字典中获取数据
        user_id = payload.get('user_id')
        account = payload.get('account')
        name = payload.get('name')
        # 若没有user_id等数据, 则返回认证异常
        if not user_id or not account or not name:
            await credentials_exception()
    except JWTError as e:
        print(f'认证异常: {e}')
        # 当解密不出来时，给出指令到redis中检测
        return True


async def credentials_exception():
    """
    凭证异常
    :return:
    """
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="认证失败",
        # 根据OAuth2规范, 认证失败需要在响应头中添加如下键值对
        headers={'WWW-Authenticate': "Bearer"}
    )
