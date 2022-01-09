from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, registry
from sqlalchemy import Integer, Column, String, Boolean, Date, DateTime
from sqlalchemy import select, func, delete

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


class PBaseModel(Base):
    __abstract__ = True
    id = BaseType.BaseColumn(BaseType.BaseInteger, primary_key=True)
    is_delete = BaseType.BaseColumn(BaseType.BaseBoolean, nullable=False, default=False)  # 逻辑删除

    @classmethod
    async def get_one_detail(cls, dbs, data_id):
        """
        以数据id为条件获取一条数据
        :param dbs:
        :param data_id:
        :return:
        """
        return await dbs.get(cls, data_id)

    @classmethod
    async def get_all_detail_page(cls, dbs, page, page_size):
        """获取所有数据-分页"""
        # 处理分页
        count = await cls.get_data_count(dbs)
        remainder = count % page_size
        if remainder == 0:
            total_page = int(count // page_size)
        else:
            total_page = int(count // page_size) + 1

        # 查询数据
        _orm = select(cls).where(cls.is_delete == 0).order_by().limit(page_size).offset((page - 1) * page)
        result = (await dbs.execute(_orm)).scalars().all()
        return result, count, total_page

    @classmethod
    async def get_all_detail(cls, dbs):
        """获取所有数据"""
        _orm = select(cls).where(cls.is_delete == 0)
        result = (await dbs.execute(_orm)).scalars().all()
        return result

    @classmethod
    async def get_data_count(cls, dbs):
        """获取数据量"""
        _orm = select(func.count()).where(cls.is_delete == 0)
        total = (await dbs.execute(_orm)).scalar()
        return total

    @classmethod
    async def delete_data_logic(cls, dbs, ids):
        """逻辑删除"""
        _orm = select(cls).where(cls.id.in_(ids))
        result = (await dbs.execute(_orm)).scalars().all()

        if result:
            for r in result:
                r.is_delete = 1

            await dbs.flush()
            await dbs.commit()

        return result

    @classmethod
    async def delete_data(cls, dbs, ids):
        """真实删除"""
        _orm = delete(cls).where(cls.id.in_(ids))
        (await dbs.execute(_orm))

        await dbs.flush()
        await dbs.commit()

    @classmethod
    async def add_data(cls, dbs, info):
        """添加单挑数据"""
        data = cls(**info.dict())
        dbs.add(data)
        await dbs.flush()
        uid = data.id
        await dbs.commit()
        return uid

    @classmethod
    async def update_data(cls, dbs, info):
        _orm = select(cls).where(cls.is_delete == 0, cls.id == info['id'])
        result = (await dbs.execute(_orm)).scalars().first()

        if result:
            for k, v in info.items():
                exec(f'result.{k}=v')
            await dbs.flush()
            await dbs.commit()
        else:
            info = 0
        return info
