from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, registry
from sqlalchemy import Integer, Column, String, Boolean, Date, DateTime

async_session_local = None


def create_eng(config):
    async_eng = create_async_engine(config.MYSQL_URL)
    global async_session_local
    # 创建session元类
    async_session_local = sessionmaker(
        class_=AsyncSession,
        autocommit=False,
        autoflush=False,
        bind=async_eng
    )


async def db_session() -> AsyncSession:
    '''session生成器 作为fastapi的Depends选项'''
    async with async_session_local() as session:
        yield session


# mapper_registry.metadata即为MetaData单例
mapper_registry = registry()
Base = mapper_registry.generate_base()


class BaseType(object):
    BaseInteger = Integer
    BaseString = String
    BaseColumn = Column
    BaseBoolean = Boolean
    BaseDate = Date
    BaseDateTime = DateTime
