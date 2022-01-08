from fastapi_pagination.bases import AbstractParams, RawParams

from sql_models import create_table
from sql_models.db_config import PBaseModel, BaseType
from sqlalchemy import select
from sql_models.PersonnelManagement.OrmUsers import Users
from fastapi_pagination.ext.async_sqlalchemy import paginate


class DocumentManagement(PBaseModel):
    __tablename__ = 'document_info'

    filename = BaseType.BaseColumn(BaseType.BaseString(255), nullable=False, unique=True)
    filesize = BaseType.BaseColumn(BaseType.BaseString(10), nullable=False)
    user_id = BaseType.BaseColumn(BaseType.BaseString(10), nullable=False)
    created_time = BaseType.BaseColumn(BaseType.BaseDateTime, nullable=False)
    updated_time = BaseType.BaseColumn(BaseType.BaseDateTime, nullable=True)

    @classmethod
    async def search(cls, data: dict, dbs):
        filter_parm = []
        # page_size = data.get("page_size")
        # page = data.get(("page"))

        if "filename" in data and data.get("filename"):
            filter_parm.append(cls.filename == data.get("filename"))
        if "user_name" in data and data.get("user_name"):
            pass
        if "start_time" in data and data.get("start_time") and "end_time" in data and data.get("end_time"):
            filter_parm.append(cls.created_time > data.get("start_time"))
            filter_parm.append(cls.created_time < data.get("end_time"))
        if "start_time" in data and data.get("start_time") and "end_time" not in data and not data.get("end_time"):
            filter_parm.append(cls.created_time > data.get("start_time"))
        if "end_time" in data and data.get("end_time") and "start_time" not in data and not data.get("start_time"):
            filter_parm.append(cls.created_time < data.get("end_time"))
        if "is_delete" in data and str(data.get("is_delete")):
            filter_parm.append(cls.is_delete == data.get("is_delete"))
        # _orm = await select(self).where(*filter_parm).order_by().limit(page_size).offset((page - 1) * page)
        _orm = select(cls).where(*filter_parm).order_by()
        return await paginate(dbs, _orm)


if __name__ == '__main__':
    create_table()
