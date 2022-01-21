import datetime

from sql_models import create_table
from sql_models.db_config import PBaseModel, BaseType
from sqlalchemy import select


# from sql_models.PersonnelManagement.OrmUsers import Roles, RoleUserMapping


class DocumentManagement(PBaseModel):
    __tablename__ = 'tb_Document'

    filename = BaseType.BaseColumn(BaseType.BaseString(255), nullable=False, unique=True)
    file_size = BaseType.BaseColumn(BaseType.BaseString(10), nullable=False)
    user_id = BaseType.BaseColumn(BaseType.BaseInteger, nullable=False)
    created_time = BaseType.BaseColumn(BaseType.BaseDateTime, nullable=False)
    updated_time = BaseType.BaseColumn(BaseType.BaseDateTime, default=datetime.datetime.now(), nullable=True)
    department_id = BaseType.BaseColumn(BaseType.BaseString(10), nullable=False)


if __name__ == '__main__':
    create_table()
