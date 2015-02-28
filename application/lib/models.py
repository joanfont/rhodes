from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

dsn = 'mysql://root:@localhost/rhodes'
db = create_engine(dsn)

Base = declarative_base()

class SessionWrapper(object):

  @staticmethod
  def get_session():
    session = sessionmaker(bind = db)
    return session()

class Message(Base):
  
  __tablename__ = 'message'

  id = Column(Integer, primary_key = True)
  message = Column(String(140))

  def __unicode__(self):
    return '<Message id={id}>'.format(id = self.id)