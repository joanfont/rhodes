from application.services.base import BasePersistanceService, BaseService
from application.lib.validators import IntegerValidator
from application.lib.models import Group, StudentGroup, User, TeacherSubject, Subject, UserType
from application.services.user import GetUser

from common.helper import Helper
from common.exceptions import GroupNotFoundError


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
        return lambda x: Helper.array_of(x, Group) or x is []

    def execute(self, args):
        subject_id = args.get('subject_id')
        groups = self.session.query(Group).filter(Group.subject_id == subject_id).all()
        return groups


class GetTeacherGroups(BasePersistanceService):

    def input(self):
        return {
            'teacher_id': IntegerValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.array_of(x, Group) or x is []

    def execute(self, args):
        teacher_id = args.get('teacher_id')
        groups = self.session.query(Group).\
            join(Subject, Group.subject_id == Subject.id).\
            join(TeacherSubject, Subject.id == TeacherSubject.subject_id).\
            join(User, TeacherSubject.teacher_id == User.id).\
            filter(User.id == teacher_id).all()
        return groups


class GetStudentGroups(BasePersistanceService):

    def input(self):
        return {
            'student_id': IntegerValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.array_of(x, Group) or x is []

    def execute(self, args):
        student_id = args.get('student_id')
        groups = self.session.query(Group).\
            join(StudentGroup, Group.id == StudentGroup.group_id).\
            join(User, StudentGroup.student_id == User.id).\
            filter(User.id == student_id).all()
        return groups


class GetUserGroups(BaseService):

    def input(self):
        return {
            'user_id': IntegerValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.array_of(x, Group) or x is []

    def execute(self, args):
        user_id = args.get('user_id')
        get_user_srv = GetUser()
        user = get_user_srv.call({'id': user_id})

        dispatcher = {
            UserType.TEACHER: (GetTeacherGroups, 'teacher_id'),
            UserType.STUDENT: (GetStudentGroups, 'student_id')
        }

        get_groups_cls, arg = dispatcher.get(user.type.id)
        get_groups_srv = get_groups_cls()
        subjects = get_groups_srv.call({arg: user.id})
        return subjects



