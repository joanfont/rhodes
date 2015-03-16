from application.services.base import BasePersistanceService, BaseService
from application.services.user import GetUser
from common.helper import Helper
from common.exceptions import SubjectNotFoundError
from application.lib.validators import IntegerValidator

from application.lib.models import Subject, Group, StudentGroup, User, TeacherSubject, UserType


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


class GetTeacherSubjects(BasePersistanceService):

    def input(self):
        return {
            'teacher_id': IntegerValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.array_of(x, Subject) or x is []

    def execute(self, args):
        teacher_id = args.get('teacher_id')
        subjects = self.session.query(Subject).\
            join(TeacherSubject, Subject.id == TeacherSubject.subject_id).\
            join(User, TeacherSubject.teacher_id == User.id).\
            filter(User.id == teacher_id).all()

        return subjects


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


class GetUserSubjects(BaseService):

    def input(self):
        return {
            'user_id': IntegerValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.array_of(x, Subject) or x is []

    def execute(self, args):
        user_id = args.get('user_id')
        get_user_srv = GetUser()
        user = get_user_srv.call({'id': user_id})

        dispatcher = {
            UserType.TEACHER: (GetTeacherSubjects, 'teacher_id'),
            UserType.STUDENT: (GetStudentSubjects, 'student_id')
        }

        get_subjects_cls, arg = dispatcher.get(user.type.id)
        get_subjects_srv = get_subjects_cls()
        subjects = get_subjects_srv.call({arg: user.id})
        return subjects



