from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

dsn = 'mysql://root:@localhost/rhodes'
db = create_engine(dsn)

Base = declarative_base()


class SessionWrapper(object):
    def __init__(self):
        self.session = sessionmaker(bind=db)()

    def add(self, obj):
        self.session.add(obj)

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

    def query(self, cls):
        return self.session.query(cls)


class DictMixin(object):
    def to_dict(self):
        raise NotImplementedError()


class Message(DictMixin, Base):
    __tablename__ = 'message'

    id = Column(Integer, primary_key=True)
    message = Column(String(140))

    def __str__(self):
        return '<Message id={id}>'.format(id=self.id)

    def to_dict(self):
        return {'id': self.id, 'message': self.message}