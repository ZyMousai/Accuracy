from jose import jwt, JWTError
from datetime import datetime, timedelta
from typing import Optional

SECRET_KEY = "ed970259a19edf1edf1010199c7002d183bd15bc1aec612481b29bac1cb83d8137"
token_time = 1


class Permissions(object):

    @staticmethod
    async def create_jwt_token(data: dict, expire_delta: Optional[timedelta] = None):
        """
        生成token
        :param data:
        :param expire_delta:
        :return:
        """
        # 如果传入了过期时间, 那么就用该时间, 否则使用默认的时间
        expire = datetime.utcnow() + expire_delta if expire_delta else datetime.utcnow() + timedelta(days=token_time)
        # 需要加密的数据data必须为一个字典类型, 在数据中添加过期时间键值对, 键exp的名称是固定写法
        data.update({'exp': expire})
        # 进行jwt加密
        token = jwt.encode(claims=data, key=SECRET_KEY, algorithm="HS256")
        return token

    @classmethod
    async def verify(cls, token: str):
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

        except JWTError:
            raise JWTError("Invalid token")
        else:
            if not user_id or not account or not name:
                raise JWTError("Invalid token")

        return user_id, account, name

        # 当解密不出来时，给出指令到redis中检测

    @classmethod
    async def verify_token_redis(cls):
        pass
