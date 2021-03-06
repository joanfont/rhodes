from application.services.base import BasePersistanceService, BaseService
from application.services.user import GetUser
from common.helper import Helper
from application.lib.validators import IntegerValidator

from application.lib.models import Subject, Group, StudentGroup, User, TeacherSubject, UserType
from application.lib.entities import Subject as SubjectEntity, Group as GroupEntity


class SubjectHelper(object):

    @staticmethod
    def attach_group_to_subject(subject_group):
        subject, group = subject_group
        if subject and group:
            new_group = GroupEntity(group.id, group.name)
            new_subject = SubjectEntity(subject.id, subject.name, subject.code, [new_group])
        else:
            new_subject = None
        return new_subject


class GetSubject(BasePersistanceService):

    def input(self):
        return {
            'subject_id': IntegerValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.instance_of(x, Subject) or x is None

    def execute(self, args):
        subject_id = args.get('subject_id')
        subject_query = self.session.query(Subject).\
            filter(Subject.id == subject_id)

        if subject_query.count():
            subject = subject_query.one()
        else:
            subject = None

        return subject


class CheckSubjectExists(BasePersistanceService):
    def input(self):
        return {
            'subject_id': IntegerValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.instance_of(x, bool)

    def execute(self, args):
        subject_id = args.get('subject_id')
        subject_query = self.session.query(Subject). \
            filter(Subject.id == subject_id)

        return subject_query.count() == 1


class CheckTeacherTeachesSubject(BasePersistanceService):
    def input(self):
        return {
            'subject_id': IntegerValidator({'required': True}),
            'teacher_id': IntegerValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.instance_of(x, bool)

    def execute(self, args):
        subject_id = args.get('subject_id')
        teacher_id = args.get('teacher_id')

        subject_query = self.session.query(Subject). \
            join(TeacherSubject, Subject.id == TeacherSubject.subject_id). \
            join(User, TeacherSubject.teacher_id == User.id). \
            filter(Subject.id == subject_id). \
            filter(User.id == teacher_id)

        return subject_query.count() == 1


class CheckStudentIsEnrolledToSubject(BasePersistanceService):
    def input(self):
        return {
            'subject_id': IntegerValidator({'required': True}),
            'student_id': IntegerValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.instance_of(x, bool)

    def execute(self, args):
        subject_id = args.get('subject_id')
        student_id = args.get('student_id')

        subject_query = self.session.query(Subject). \
            join(Group, Subject.id == Group.subject_id). \
            join(StudentGroup, Group.id == StudentGroup.group_id). \
            join(User, StudentGroup.student_id == User.id). \
            filter(Subject.id == subject_id). \
            filter(User.id == student_id)

        return subject_query.count() == 1


class CheckUserBelongsToSubject(BaseService):
    def input(self):
        return {
            'subject_id': IntegerValidator({'required': True}),
            'user_id': IntegerValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.instance_of(x, bool)

    def execute(self, args):
        subject_id = args.get('subject_id')
        user_id = args.get('user_id')

        get_user_srv = GetUser()
        user = get_user_srv.call({'user_id': user_id})

        dispatcher = {
            UserType.TEACHER: (CheckTeacherTeachesSubject, 'teacher_id'),
            UserType.STUDENT: (CheckStudentIsEnrolledToSubject, 'student_id')
        }

        check_user_belongs_cls, arg = dispatcher.get(user.type.id)
        check_user_belongs_srv = check_user_belongs_cls()

        belongs = check_user_belongs_srv.call({'subject_id': subject_id, arg: user.id})

        return belongs


class GetTeacherSubject(BasePersistanceService):
    def input(self):
        return {
            'subject_id': IntegerValidator({'required': True}),
            'teacher_id': IntegerValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.instance_of(x, Subject) or x is None

    def execute(self, args):

        subject_id = args.get('subject_id')
        subject_query = self.session.query(Subject).\
            filter(Subject.id == subject_id)

        if subject_query.count():
            subject = subject_query.one()
        else:
            subject = None

        return subject


class GetStudentSubject(BasePersistanceService):
    def input(self):
        return {
            'subject_id': IntegerValidator({'required': True}),
            'student_id': IntegerValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.instance_of(x, SubjectEntity) or x is None

    def execute(self, args):
        subject_id = args.get('subject_id')
        student_id = args.get('student_id')

        subjects_and_groups_query = self.session.query(Subject, Group). \
            join(Group, Subject.id == Group.subject_id). \
            join(StudentGroup, Group.id == StudentGroup.group_id). \
            join(User, StudentGroup.student_id == User.id). \
            filter(User.id == student_id). \
            filter(Subject.id == subject_id)

        if subjects_and_groups_query.count():
            subject_group = subjects_and_groups_query.one()
            subject = SubjectHelper.attach_group_to_subject(subject_group)
        else:
            subject = None

        return subject


class GetUserSubject(BaseService):
    def input(self):
        return {
            'subject_id': IntegerValidator({'required': True}),
            'user_id': IntegerValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.instance_of(x, (Subject, SubjectEntity)) or x is None

    def execute(self, args):

        subject_id = args.get('subject_id')
        user_id = args.get('user_id')

        get_user_srv = GetUser()
        user = get_user_srv.call({'user_id': user_id})

        dispatcher = {
            UserType.TEACHER: (GetTeacherSubject, 'teacher_id'),
            UserType.STUDENT: (GetStudentSubject, 'student_id')
        }

        get_subject_cls, arg = dispatcher.get(user.type.id)
        get_subject_srv = get_subject_cls()

        subject = get_subject_srv.call({'subject_id': subject_id, arg: user.id})
        return subject


class GetTeacherSubjects(BasePersistanceService):
    def input(self):
        return {
            'teacher_id': IntegerValidator({'required': True}),
        }

    def output(self):
        return lambda x: Helper.array_of(x, Subject) or x == []

    def execute(self, args):
        teacher_id = args.get('teacher_id')
        subjects = self.session.query(Subject). \
            join(TeacherSubject, Subject.id == TeacherSubject.subject_id). \
            join(User, TeacherSubject.teacher_id == User.id). \
            filter(User.id == teacher_id). \
            order_by(Subject.code.asc()).all()
        return subjects


class GetStudentSubjects(BasePersistanceService):
    def input(self):
        return {
            'student_id': IntegerValidator({'required': True}),

        }

    def output(self):
        return lambda x: Helper.array_of(x, SubjectEntity) or x is []

    def execute(self, args):

        student_id = args.get('student_id')

        subjects_and_groups = self.session.query(Subject, Group). \
            join(Group, Subject.id == Group.subject_id). \
            join(StudentGroup, Group.id == StudentGroup.group_id). \
            join(User, StudentGroup.student_id == User.id). \
            filter(User.id == student_id). \
            order_by(Subject.code.asc()).all()

        subjects = map(SubjectHelper.attach_group_to_subject, subjects_and_groups)
        return subjects


class GetUserSubjects(BaseService):
    def input(self):
        return {
            'user_id': IntegerValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.array_of(x, (Subject, SubjectEntity)) or x is []

    def execute(self, args):
        user_id = args.get('user_id')

        get_user_srv = GetUser()
        user = get_user_srv.call({'user_id': user_id})

        dispatcher = {
            UserType.TEACHER: (GetTeacherSubjects, 'teacher_id'),
            UserType.STUDENT: (GetStudentSubjects, 'student_id')
        }

        get_subjects_cls, arg = dispatcher.get(user.type.id)
        get_subjects_srv = get_subjects_cls()

        subjects = get_subjects_srv.call({arg: user.id})

        return subjects