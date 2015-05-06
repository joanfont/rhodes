from application.services.base import BasePersistanceService, BaseService
from application.lib.validators import IntegerValidator
from application.lib.models import Group, StudentGroup, User, TeacherSubject, Subject, UserType
from application.services.user import GetUser

from common.helper import Helper


class GetGroup(BasePersistanceService):

    def input(self):
        return {
            'group_id': IntegerValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.instance_of(x, Group) or x is None

    def execute(self, args):
        group_id = args.get('group_id')
        group_query = self.session.query(Group)

        if group_query.filter(Group.id == group_id).count():
            group = group_query.get(group_id)
        else:
            group = None

        return group


class CheckGroupExists(BasePersistanceService):

        def input(self):
            return {
                'group_id': IntegerValidator({'required': True})
            }

        def output(self):
            return lambda x: Helper.instance_of(x, bool)

        def execute(self, args):
            group_id = args.get('group_id')
            group_query = self.session.query(Group).\
                filter(Group.id == group_id)

            return group_query.count() == 1


class CheckTeacherTeachesGroup(BasePersistanceService):

    def input(self):
        return {
            'group_id': IntegerValidator({'required': True}),
            'teacher_id': IntegerValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.instance_of(x, bool)

    def execute(self, args):

        group_id = args.get('group_id')
        teacher_id = args.get('teacher_id')

        group_count = self.session.query(Group).\
            join(Subject, Group.subject_id == Subject.id).\
            join(TeacherSubject, Subject.id == TeacherSubject.subject_id).\
            join(User, TeacherSubject.teacher_id == User.id).\
            filter(Group.id == group_id).\
            filter(User.id == teacher_id).\
            count()

        return group_count > 0


class CheckStudentIsEnrolledToGroup(BasePersistanceService):

    def input(self):
        return {
            'group_id': IntegerValidator({'required': True}),
            'student_id': IntegerValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.instance_of(x, bool)

    def execute(self, args):

        group_id = args.get('group_id')
        student_id = args.get('student_id')

        group_count = self.session.query(Group).\
            join(StudentGroup, Group.id == StudentGroup.group_id).\
            join(User, StudentGroup.student_id == User.id).\
            filter(Group.id == group_id).\
            filter(User.id == student_id).\
            count()

        return group_count > 0


class CheckUserBelongsToGroup(BaseService):

    def input(self):
        return {
            'group_id': IntegerValidator({'required': True}),
            'user_id': IntegerValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.instance_of(x, bool)

    def execute(self, args):

        group_id = args.get('group_id')
        user_id = args.get('user_id')

        get_user_srv = GetUser()
        user = get_user_srv.call({'user_id': user_id})

        dispatcher = {
            UserType.TEACHER: (CheckTeacherTeachesGroup, 'teacher_id'),
            UserType.STUDENT: (CheckStudentIsEnrolledToGroup, 'student_id')
        }

        check_belongs_cls, arg = dispatcher.get(user.type.id)
        check_belongs_srv = check_belongs_cls()
        check = check_belongs_srv.call({'group_id': group_id, arg: user.id})
        return check


class GroupBelongsToSubject(BasePersistanceService):

    def input(self):
        return {
            'group_id': IntegerValidator({'required': True}),
            'subject_id': IntegerValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.instance_of(x, bool)

    def execute(self, args):

        group_id = args.get('group_id')
        subject_id = args.get('subject_id')

        group_query = self.session.query(Group).\
            join(Subject, Group.subject_id == Subject.id).\
            filter(Group.id == group_id).\
            filter(Subject.id == subject_id)

        return group_query.count() > 0


class GetSubjectGroups(BasePersistanceService):

    def input(self):
        return {
            'subject_id': IntegerValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.array_of(x, Group) or x is []

    def execute(self, args):
        subject_id = args.get('subject_id')
        groups = self.session.query(Group).filter(Group.subject_id == subject_id).all()
        return groups


class GetSubjectTeacherGroups(BaseService):

    def input(self):
        return {
            'subject_id': IntegerValidator({'required': True}),
            'teacher_id': IntegerValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.array_of(x, Group) or x is []

    def execute(self, args):

        # teacher_id arg is not used because a teacher teaches all the groups of a subject
        subject_id = args.get('subject_id')
        get_subject_groups = GetSubjectGroups()
        groups = get_subject_groups.call({'subject_id': subject_id})
        return groups


class GetSubjectStudentGroups(BasePersistanceService):

    def input(self):
        return {
            'subject_id': IntegerValidator({'required': True}),
            'student_id': IntegerValidator({'required': True}),
        }

    def output(self):
        return lambda x: Helper.array_of(x, Group) or x is []

    def execute(self, args):

        subject_id = args.get('subject_id')
        student_id = args.get('student_id')

        groups = self.session.query(Group).\
            join(StudentGroup, Group.id == StudentGroup.group_id).\
            join(User, StudentGroup.student_id == User.id).\
            filter(Group.subject_id == subject_id).\
            filter(User.id == student_id).all()

        return groups


class GetSubjectUserGroups(BaseService):

    def input(self):
        return {
            'subject_id': IntegerValidator({'required': True}),
            'user_id': IntegerValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.array_of(x, Group) or x is []

    def execute(self, args):
        subject_id = args.get('subject_id')
        user_id = args.get('user_id')
        get_user_srv = GetUser()
        user = get_user_srv.call({'user_id': user_id})

        dispatcher = {
            UserType.TEACHER: (GetSubjectTeacherGroups, 'teacher_id'),
            UserType.STUDENT: (GetSubjectStudentGroups, 'student_id')
        }

        get_groups_cls, arg = dispatcher.get(user.type.id)
        get_groups_srv = get_groups_cls()
        groups = get_groups_srv.call({'subject_id': subject_id, arg: user.id})
        return groups


class GetTeacherGroups(BasePersistanceService):

    def input(self):
        return {
            'teacher_id': IntegerValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.array_of(x, Group) or x == []

    def execute(self, args):

        teacher_id = args.get('teacher_id')

        teacher_groups_query = self.session.query(Group).\
            join(Subject, Group.subject_id == Subject.id).\
            join(TeacherSubject, Subject.id == TeacherSubject.subject_id).\
            join(User, TeacherSubject.teacher_id == User.id).\
            filter(User.id == teacher_id)

        return teacher_groups_query.all()


class GetStudentGroups(BasePersistanceService):

    def input(self):
        return {
            'student_id': IntegerValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.array_of(x, Group) or x == []

    def execute(self, args):

        student_id = args.get('student_id')

        student_groups_query = self.session.query(Group).\
            join(StudentGroup, Group.id == StudentGroup.group_id).\
            join(User, StudentGroup.student_id == User.id).\
            filter(User.id == student_id)

        return student_groups_query.all()


class GetUserGroups(BaseService):

    def input(self):
        return {
            'user_id': IntegerValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.array_of(x, Group) or x == []

    def execute(self, args):

        user_id = args.get('user_id')
        get_user_srv = GetUser()
        user = get_user_srv.call({'user_id': user_id})

        dispatcher = {
            UserType.TEACHER: (GetTeacherGroups, 'teacher_id'),
            UserType.STUDENT: (GetStudentGroups, 'student_id')
        }

        get_groups_cls, arg = dispatcher.get(user.type.id)
        get_groups_srv = get_groups_cls()
        groups = get_groups_srv.call({arg: user.id})
        return groups