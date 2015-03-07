from application.services.base import BasePersistanceService
from application.lib.helper import Helper
from application.lib.validators import IntegerValidator

from application.lib.models import Subject, Group, StudentGroup, Person


class GetSubject(BasePersistanceService):

    def input(self):
        return {
            'id': IntegerValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.instance_of(x, Subject) or x is None

    def execute(self, args):
        _id = args.get('id')
        return self.session.query(Subject).get(_id)


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
            join(Person, StudentGroup.student_id == Person.id).\
            filter(Person.id == student_id).all()

        return subjects