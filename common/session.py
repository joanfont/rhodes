from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import config.rhodes as config

from api import db


class SessionManager(object):

    @staticmethod
    def get_flask():
        return db.session()

    @staticmethod
    def get_standalone():
        engine = create_engine(config.DB_DSN)
        return sessionmaker(bind=engine)()
