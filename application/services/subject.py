from application.services.base import BasePersistanceService
from common.helper import Helper
from common.exceptions import SubjectNotFoundError
from application.lib.validators import IntegerValidator

from application.lib.models import Subject, Group, StudentGroup, User


class GetSubject(BasePersistanceService):

    def input(self):
        return {
            'id': IntegerValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.instance_of(x, Subject) or x is None

    def execute(self, args):
        _id = args.get('id')
        subject = self.session.query(Subject).get(_id)

        if not subject:
            raise SubjectNotFoundError()

        return subject


class GetStudentSubjects(BasePersistanceService):

    def input(self):
        return {
            'student_id': IntegerValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.array_of(x, Subject) or x is []

    def execute(self, args):
        student_id = args.get('student_id')
        subjects = self.session.query(Subject).\
            join(Group, Subject.id == Group.subject_id).\
            join(StudentGroup, Group.id == StudentGroup.group_id).\
            join(User, StudentGroup.student_id == User.id).\
            filter(User.id == student_id).all()

        return subjects