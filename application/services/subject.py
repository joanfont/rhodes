from application.services.base import BasePersistanceService
from application.lib.helper import Helper

from application.lib.models import Subject


class GetSubjects(BasePersistanceService):

    def input(self):
        return {}

    def output(self):
        return lambda x: Helper.array_of(x, Subject) or x is []

    def execute(self, args):
        return self.session.query(Subject).all()

