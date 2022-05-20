from sql_models import create_table
from sql_models.db_config import PBaseModel, BaseType
from sqlalchemy import select

from sql_models.PersonnelManagement.OrmPersonnelManagement import Users


# from sql_models.PersonnelManagement.OrmUsers import Roles, RoleUserMapping


class DocumentManagement(PBaseModel):
    __tablename__ = 'tb_Document'

    filename = BaseType.BaseColumn(BaseType.BaseString(255), nullable=False, unique=True)
    file_size = BaseType.BaseColumn(BaseType.BaseString(10), nullable=False)
    user_id = BaseType.BaseColumn(BaseType.BaseInteger, nullable=False)
    created_time = BaseType.BaseColumn(BaseType.BaseDateTime, nullable=False)
    updated_time = BaseType.BaseColumn(BaseType.BaseDateTime, nullable=True)
    department_id = BaseType.BaseColumn(BaseType.BaseString(10), nullable=False)

    @classmethod
    async def get_document_user(cls, dbs, user_id):
        _orm = select(Users).where(Users.is_delete == 0, Users.id == user_id)
        result = (await dbs.execute(_orm)).scalars().first()
        return result.name

    @classmethod
    async def get_document_user_id(cls, dbs, user_name):
        print(user_name)
        _orm = select(Users).where(Users.is_delete == 0, Users.name == user_name)
        result = (await dbs.execute(_orm)).scalars().first()
        print(result.id)
        return result.id


if __name__ == '__main__':
    create_table()
