from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import INTEGER as Integer

db = SQLAlchemy()

class Base(object):

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    __table_args__ = {'mysql_engine': 'InnoDB'}

    ID = db.Column(Integer(unsigned=True), primary_key=True, nullable=False, autoincrement=True)

Base = declarative_base(cls = Base)