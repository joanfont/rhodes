from application.services.base import BasePersistanceService
from application.lib.validators import IntegerValidator, StringValidator
from common.helper import Helper
from application.lib.models import User, StudentGroup, Group, Subject, TeacherSubject
from common.exceptions import UserNotFoundError


class GetUser(BasePersistanceService):

    def input(self):
        return {
            'user_id': IntegerValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.instance_of(x, User)

    def execute(self, args):
        user_id = args.get('user_id')
        user = self.session.query(User).get(user_id)

        if not user:
            raise UserNotFoundError()

        return user


class GetUserByAuthToken(BasePersistanceService):

    def input(self):
        return {
            'auth_token': StringValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.instance_of(x, User)

    def execute(self, args):
        auth_token = args.get('auth_token')
        user = self.session.query(User).\
            filter(User.auth_token == auth_token).\
            one()

        if not user:
            raise UserNotFoundError()

        return user


class GetUserByUserAndPassword(BasePersistanceService):

    def input(self):
        return {
            'user': StringValidator({'required': True}),
            'password': StringValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.instance_of(x, User)

    def execute(self, args):

        user = args.get('user')
        password = args.get('password')

        user = self.session.query(User).\
            filter(User.user == user).\
            filter(User.password == password).\
            one()

        if not user:
            raise UserNotFoundError()

        return user


class GetUserAuthTokenByUserAndPassword(BasePersistanceService):

    def input(self):
        return {
            'user': StringValidator({'required': True}),
            'password': StringValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.instance_of(x, str)

    def execute(self, args):

        get_user = GetUserByUserAndPassword()
        user = get_user.call(args)

        return user.auth_token


class CheckUserExistsByUserAndPassword(BasePersistanceService):

    def input(self):
            return {
                'user': StringValidator({'required': True}),
                'password': StringValidator({'required': True})
            }

    def output(self):
        return lambda x: Helper.instance_of(x, bool)

    def execute(self, args):

        user = args.get('user')
        password = args.get('password')

        user_query = self.session.query(User).\
            filter(User.user == user).\
            filter(User.password == password)

        return user_query.count() == 1


class GetSubjectTeachers(BasePersistanceService):

    def input(self):
        return {
            'subject_id': IntegerValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.array_of(x, User) or x is []

    def execute(self, args):

        subject_id = args.get('subject_id')

        teachers = self.session.query(User).\
            join(TeacherSubject, User.id == TeacherSubject.teacher_id).\
            join(Subject, TeacherSubject.subject_id == Subject.id).\
            filter(Subject.id == subject_id).all()

        return teachers


class GetSubjectStudents(BasePersistanceService):

    def input(self):
        return {
            'subject_id': IntegerValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.array_of(x, User) or x is []

    def execute(self, args):

        subject_id = args.get('subject_id')
        students = self.session.query(User).\
            join(StudentGroup, User.id == StudentGroup.student_id).\
            join(Group, StudentGroup.group_id == Group.id).\
            join(Subject, Group.subject_id == Subject.id).\
            filter(Subject.id == subject_id).all()

        return students

