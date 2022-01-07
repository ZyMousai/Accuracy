from sqlalchemy import Column, Integer, VARCHAR, BOOLEAN, DATETIME, func

from sql_models import create_table
from sql_models.db_config import PBaseModel, BaseType


class DocumentManagement(PBaseModel):
    __tablename__ = 'document_info'

    filename = BaseType.BaseColumn(BaseType.BaseString(255), nullable=False, unique=True)
    filesize = BaseType.BaseColumn(BaseType.BaseString(10), nullable=False)
    user_id = BaseType.BaseColumn(BaseType.BaseString(10), nullable=False)
    created_time = BaseType.BaseColumn(BaseType.BaseDateTime, nullable=False)
    updated_time = BaseType.BaseColumn(BaseType.BaseDateTime, nullable=True)


if __name__ == '__main__':
    create_table()
