from application.services.base import BasePersistanceService
from application.lib.validators import IntegerValidator
from application.lib.helper import Helper
from application.lib.models import Group


class GroupNotFoundError(Exception):
    pass


class GetGroup(BasePersistanceService):

    def input(self):
        return {
            'id': IntegerValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.instance_of(x, Group)

    def execute(self, args):
        _id = args.get('id')
        group = self.session.query(Group).get(_id)

        if not group:
            raise GroupNotFoundError()

        return group


class GetSubjectGroups(BasePersistanceService):

    def input(self):
        return {
            'subject_id': IntegerValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.array_of(x, Group) or x is None

    def execute(self, args):
        subject_id = args.get('subject_id')
        groups = self.session.query(Group).filter(Group.subject_id == subject_id).all()
        return groups
