import datetime
import uuid

from sqlalchemy import select, func
from sql_models import create_table
from sql_models.db_config import BaseType, PBaseModel
from sqlalchemy import or_


class TrackAlliance(PBaseModel):
    __tablename__ = 'track_alliance'

    name = BaseType.BaseColumn(BaseType.BaseString(588), nullable=False)
    url = BaseType.BaseColumn(BaseType.BaseString(588), nullable=False)
    alliance_uuid = BaseType.BaseColumn(BaseType.BaseString(588), nullable=False, default=uuid.uuid1)
    created_time = BaseType.BaseColumn(BaseType.BaseDateTime, nullable=False, default=datetime.datetime.now)

    @classmethod
    async def get_all_detail_page_track(cls, dbs, page, page_size, **kwargs):
        """获取所有数据-分页-关联查询"""
        # 构建查询条件
        filter_condition = list()
        name_or_url = kwargs.get("name_or_url")
        track_url = kwargs.get("track_url")
        if name_or_url:
            filter_condition.append(cls.name.like(f"%{name_or_url}%"))
            filter_condition.append(cls.url.like(f"%{name_or_url}%"))

        if track_url:
            filter_condition.append(TrackUrl.track_url.like(f"%{track_url}%"))

        # 查询数据
        _orm = select(cls.id, cls.name, cls.url, TrackUrl.id, TrackUrl.track_url).outerjoin(TrackUrl,
                                                                                            TrackUrl.alliance_id == cls.alliance_uuid).where(
            or_(*filter_condition)).order_by().limit(page_size).offset((page - 1) * page_size)
        print(_orm)
        result = (await dbs.execute(_orm)).all()

        # 处理分页
        # count = len(result)
        # count = await TrackAlliance.get_data_count_or(dbs, *filter_condition)

        _orm = select(cls.id, cls.name, cls.url, TrackUrl.id, TrackUrl.track_url).outerjoin(TrackUrl,
                                                                                             TrackUrl.alliance_id == cls.alliance_uuid).where(
            or_(*filter_condition))
        count = (await dbs.execute(_orm)).scalar()
        # return total

        print(count)
        remainder = count % page_size
        if remainder == 0:
            total_page = int(count // page_size)
        else:
            total_page = int(count // page_size) + 1
        return result, count, total_page


class TrackUrl(PBaseModel):
    __tablename__ = 'track_url'

    track_url = BaseType.BaseColumn(BaseType.BaseString(588), nullable=False)
    alliance_id = BaseType.BaseColumn(BaseType.BaseString(588), nullable=False)  # 链接的是alliance_uuid
    created_time = BaseType.BaseColumn(BaseType.BaseDateTime, nullable=False, default=datetime.datetime.now)


if __name__ == '__main__':
    create_table()
