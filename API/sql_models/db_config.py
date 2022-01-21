from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, registry
from sqlalchemy import Integer, Column, String, Boolean, Date, DateTime, Float
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
    """session生成器 作为fastapi的Depends选项"""
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
    BaseFloat = Float


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
    async def get_one(cls, dbs, *args):
        """以一些特定属性来获取一条数据"""
        filter_condition = list()
        for x in args:
            if x[2] is not None:
                filter_condition.append(eval(f'cls.{x[0]}{x[1]}'))
        _orm = select(cls).where(*filter_condition)
        result = (await dbs.execute(_orm)).scalars().first()

        return result

    @classmethod
    async def get_all_detail_page(cls, dbs, page, page_size, *args):
        """获取所有数据-分页"""
        # 构建查询条件
        filter_condition = list()
        for x in args:
            if x[2] is not None:
                filter_condition.append(eval(f'cls.{x[0]}{x[1]}'))
        # 处理分页
        count = await cls.get_data_count(dbs, *filter_condition)
        remainder = count % page_size
        if remainder == 0:
            total_page = int(count // page_size)
        else:
            total_page = int(count // page_size) + 1

        # 查询数据
        _orm = select(cls).where(*filter_condition).order_by().limit(page_size).offset((page - 1) * page_size)
        result = (await dbs.execute(_orm)).scalars().all()
        return result, count, total_page

    @classmethod
    async def get_all(cls, dbs, *args):
        """获取有此关键词的所有数据"""
        # 构建查询条件
        filter_condition = list()
        for x in args:
            if x[2] is not None:
                filter_condition.append(eval(f'cls.{x[0]}{x[1]}'))

        # 查询数据
        _orm = select(cls).where(*filter_condition)
        result = (await dbs.execute(_orm)).scalars().all()
        return result

    @classmethod
    async def get_data_count(cls, dbs, *args):
        """获取数据量"""
        _orm = select(func.count()).where(*args)
        total = (await dbs.execute(_orm)).scalar()
        return total

    @classmethod
    async def delete_data_logic(cls, dbs, ids, auto_commit=True):
        """逻辑删除"""
        _orm = select(cls).where(cls.id.in_(ids))
        result = (await dbs.execute(_orm)).scalars().all()

        if result:
            for r in result:
                r.is_delete = 1

            await dbs.flush()
            if auto_commit:
                await dbs.commit()

        return result

    @classmethod
    async def delete_data(cls, dbs, ids, auto_commit=True):
        """真实删除"""
        _orm = delete(cls).where(cls.id.in_(ids))
        (await dbs.execute(_orm))

        await dbs.flush()
        if auto_commit:
            await dbs.commit()

        return ids

    @classmethod
    async def filter_delete_data(cls, dbs, *args, auto_commit=True):
        """通过条件真实删除"""

        filter_condition = list()
        for x in args:
            if x[2] is not None:
                filter_condition.append(eval(f'cls.{x[0]}{x[1]}'))
        _orm = delete(cls).where(*filter_condition)
        await dbs.execute(_orm)

        await dbs.flush()
        if auto_commit:
            await dbs.commit()

    @classmethod
    async def add_data(cls, dbs, info, auto_commit=True):
        """添加单条数据"""
        if not isinstance(info, dict):
            info = info.dict()
        data = cls(**info)
        dbs.add(data)
        await dbs.flush()
        uid = data.id
        if auto_commit:
            await dbs.commit()
        return uid

    @classmethod
    async def add_data_many(cls, dbs, info_list):
        """添加多条数据"""
        uid_list = []
        for info in info_list:
            uid = await cls.add_data(dbs, info, auto_commit=False)
            uid_list.append(uid)
        await dbs.commit()
        return uid_list

    @classmethod
    async def update_data(cls, dbs, info, is_delete):
        """更新数据"""
        _orm = select(cls).where(cls.is_delete == is_delete, cls.id == info['id'])
        result = (await dbs.execute(_orm)).scalars().first()

        if result:
            for k, v in info.items():
                exec(f'result.{k}=v')
            await dbs.flush()
            await dbs.commit()
        else:
            info = 0
        return info

    @classmethod
    async def filter_add_data_many(cls, dbs, id1, id1_value, id2, ids, auto_commit=True):
        """
        添加关联信息
        id1 一对多 id2
        :param dbs:
        :param id1: 主关联id
        :param id1_value: 主关联id得value
        :param id2: 副关联id
        :param ids: 副关联id得value
        :param auto_commit:
        :return:
        """
        # 先查询出有没有相关数据
        add_list = [{f"{id1}": id1_value, f"{id2}": x} for x in ids]
        add_menu_id_list = []
        exist_list = []

        # 组建查询条件
        filter_condition = [eval(f"cls.{id1} == {id1_value}"), eval(f"cls.{id2}.in_({ids})"), cls.is_delete == 0]
        _orm = select(cls).where(*filter_condition)

        # 把所有查询出来得数据id做为一个list
        exist_data = (await dbs.execute(_orm)).scalars().all()
        exist_data_id = [eval(f"o.{id2}") for o in exist_data]

        # 判断id2是否在已存在得id-list里
        # 只会插入不存在的数据
        for info in add_list:
            if info.get(id2) not in exist_data_id:
                await cls.add_data(dbs, info, auto_commit=False)
                add_menu_id_list.append(info.get(id2))
            else:
                exist_list.append(info.get(id2))
        if auto_commit:
            await dbs.commit()
        return add_menu_id_list, exist_data_id
