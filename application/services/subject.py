from application.services.base import BasePersistanceService, BaseService
from application.services.user import GetUser
from common.helper import Helper
from common.exceptions import TeacherDoesNotTeachSubjectError, StudentIsNotEnrolledToSubjectError, SubjectNotFoundError
from application.lib.validators import IntegerValidator, BooleanValidator

from application.lib.models import Subject, Group, StudentGroup, User, TeacherSubject, UserType


def add_student_group_to_subject(group):
    subject = group.subject
    setattr(subject, 'group', group)
    return subject


class GetTeacherSubject(BasePersistanceService):

    def input(self):
        return {
            'id': IntegerValidator({'required': True}),
            'teacher_id': IntegerValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.instance_of(x, Subject)

    def execute(self, args):

        subject_id = args.get('id')
        teacher_id = args.get('teacher_id')

        subject_query = self.session.query(Subject).\
            filter(Subject.id == subject_id)

        if not subject_query.count():
            raise SubjectNotFoundError()

        subject_query = subject_query.join(TeacherSubject, Subject.id == TeacherSubject.subject_id).\
            join(User, TeacherSubject.teacher_id == User.id).\
            filter(User.id == teacher_id)

        if not subject_query.count():
            raise TeacherDoesNotTeachSubjectError()

        return subject_query.one()


class GetStudentSubject(BasePersistanceService):

    def input(self):
        return {
            'id': IntegerValidator({'required': True}),
            'student_id': IntegerValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.instance_of(x, Subject)

    def execute(self, args):
        subject_id = args.get('id')
        student_id = args.get('student_id')

        group_query = self.session.query(Group).\
            join(Subject, Group.subject_id == Subject.id).\
            filter(Subject.id == subject_id)

        if not group_query.count():
            raise SubjectNotFoundError()

        group_query = group_query.join(StudentGroup, Group.id == StudentGroup.student_id).\
            join(User, StudentGroup.student_id == User.id).\
            filter(User.id == student_id)

        if not group_query.count():
            raise StudentIsNotEnrolledToSubjectError()

        group = group_query.one()
        subject = add_student_group_to_subject(group)
        return subject


class GetUserSubject(BaseService):

    def input(self):
        return {
            'id': IntegerValidator({'required': True}),
            'user_id': IntegerValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.instance_of(x, Subject)

    def execute(self, args):
        user_id = args.get('user_id')
        subject_id = args.get('id')

        get_user_srv = GetUser()
        user = get_user_srv.call({'id': user_id})

        dispatcher = {
            UserType.TEACHER: (GetTeacherSubject, 'teacher_id'),
            UserType.STUDENT: (GetStudentSubject, 'student_id')
        }

        get_subject_cls, arg = dispatcher.get(user.type.id)
        get_subject_srv = get_subject_cls()

        subject = get_subject_srv.call({'id': subject_id, arg: user.id})

        return subject


class GetTeacherSubjects(BasePersistanceService):

    def input(self):
        return {
            'teacher_id': IntegerValidator({'required': True}),
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
            'student_id': IntegerValidator({'required': True}),

        }

    def output(self):
        return lambda x: Helper.array_of(x, Subject) or x is []

    def execute(self, args):

        student_id = args.get('student_id')

        groups = self.session.query(Group).\
            join(StudentGroup, Group.id == StudentGroup.group_id).\
            join(User, StudentGroup.student_id == User.id).\
            filter(User.id == student_id).\
            all()

        subjects = map(add_student_group_to_subject, groups)

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
