# Users 视图
from fastapi import APIRouter, Depends

from sqlalchemy import select


from sql_models.PersonnelManagement.OrmUsers import User
from sqlalchemy.ext.asyncio import AsyncSession

from sql_models.db_config import db_session

users_router = APIRouter(
    prefix="/users/v1",
    responses={404: {"description": "Not found"}}, )


@users_router.get('/demo/{user_name}')
async def get_demo(user_name: str, dbs: AsyncSession = Depends(db_session)):
    _orm = select(User).where(User.name == user_name)
    result: User = (await dbs.execute(_orm)).scalars().first()
    return result


@users_router.get('/demo1/{id}')
async def get_demo1(id: int, dbs: AsyncSession = Depends(db_session)):
    return await dbs.get(User, id)
