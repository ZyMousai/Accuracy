from sqlalchemy import Integer, Column, String

from sql_models import create_table
from sql_models.db_config import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(30))


if __name__ == '__main__':
    create_table()
