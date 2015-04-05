from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import config

from api import db


class SessionManager(object):

    def __init__(self):
        self.sessions = {
            'flask': self.flask,
            'standalone': self.standalone
        }

    def get(self, item):
        session = self.sessions.get(item)
        return session()

    @staticmethod
    def flask():
        return db.session

    @staticmethod
    def standalone():
        engine = create_engine(config.DB_DSN)
        return sessionmaker(bind=engine)


manager = SessionManager()