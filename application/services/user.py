from application.services.base import BasePersistanceService, BaseService
from application.lib.validators import IntegerValidator, StringValidator
from common.helper import Helper
from application.lib.models import User, StudentGroup, Group, Subject, TeacherSubject, UserType
from sqlalchemy.orm import aliased


class GetUser(BasePersistanceService):

    def input(self):
        return {
            'user_id': IntegerValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.instance_of(x, User) or x is None

    def execute(self, args):
        user_id = args.get('user_id')
        user_query = self.session.query(User)

        if user_query.filter(User.id == user_id).count():
            user = user_query.get(user_id)
        else:
            user = None

        return user


class GetUserByAuthToken(BasePersistanceService):

    def input(self):
        return {
            'auth_token': StringValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.instance_of(x, User) or x is None

    def execute(self, args):
        auth_token = args.get('auth_token')
        user_query = self.session.query(User).\
            filter(User.auth_token == auth_token)

        if user_query.count():
            user = user_query.one()
        else:
            user = None

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

        user_query = self.session.query(User).\
            filter(User.user == user).\
            filter(User.password == password)

        if user_query.count():
            user = user_query.one()
        else:
            user = None

        return user


class GetUserAuthTokenByUserAndPassword(BasePersistanceService):

    def input(self):
        return {
            'user': StringValidator({'required': True}),
            'password': StringValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.instance_of(x, unicode)

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
        return lambda x: Helper.array_of(x, User) or x == []

    def execute(self, args):

        subject_id = args.get('subject_id')
        students = self.session.query(User).\
            join(StudentGroup, User.id == StudentGroup.student_id).\
            join(Group, StudentGroup.group_id == Group.id).\
            join(Subject, Group.subject_id == Subject.id).\
            filter(Subject.id == subject_id).all()

        return students


class GetGroupStudents(BasePersistanceService):

    def input(self):
        return {
            'group_id': IntegerValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.array_of(x, User) or x == []

    def execute(self, args):

        group_id = args.get('group_id')
        students = self.session.query(User).\
            join(StudentGroup, User.id == StudentGroup.student_id).\
            join(Group, StudentGroup.group_id == Group.id).\
            filter(Group.id == group_id).all()

        return students


class GetTeacherTeacherPeers(BasePersistanceService):

    def input(self):
        return {
            'user_id': IntegerValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.array_of(x, User) or x == []

    def execute(self, args):

        user_id = args.get('user_id')

        me = aliased(User, name='me')
        others = aliased(User, name='others')
        my_teacher_subject = aliased(TeacherSubject, name='ts1')
        their_teacher_subject = aliased(TeacherSubject, name='ts2')

        peers_query = self.session.query(others).\
            join(their_teacher_subject, their_teacher_subject.teacher_id == others.id).\
            join(Subject, their_teacher_subject.subject_id == Subject.id).\
            join(my_teacher_subject, Subject.id == my_teacher_subject.subject_id).\
            join(me, my_teacher_subject.teacher_id == me.id).\
            filter(me.id == user_id).\
            filter(others.id != user_id)

        peers = peers_query.all()

        return peers


class GetStudentTeacherPeers(BasePersistanceService):

    def input(self):
        return {
            'user_id': IntegerValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.array_of(x, User) or x == []

    def execute(self, args):

        user_id = args.get('user_id')

        teachers = aliased(User, name='teachers')
        me = aliased(User, name='me')

        peers_query = self.session.query(teachers).\
            join(TeacherSubject, teachers.id == TeacherSubject.teacher_id).\
            join(Subject, TeacherSubject.subject_id == Subject.id).\
            join(Group, Subject.id == Group.subject_id).\
            join(StudentGroup, Group.id == StudentGroup.group_id).\
            join(me, StudentGroup.student_id == me.id).\
            filter(me.id == user_id)

        peers = peers_query.all()

        return peers


class GetUserTeacherPeers(BaseService):

    def input(self):
        return {
            'user_id': IntegerValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.array_of(x, User) or x == []

    def execute(self, args):

        user_id = args.get('user_id')

        dispatcher = {
            UserType.TEACHER: GetTeacherTeacherPeers,
            UserType.STUDENT: GetStudentTeacherPeers
        }

        get_user_srv = GetUser()
        user = get_user_srv.call({'user_id': user_id})

        get_teacher_peers_cls = dispatcher.get(user.type_id)
        get_teacher_peers = get_teacher_peers_cls()

        peers = get_teacher_peers.call({'user_id': user_id})

        return peers


class GetTeacherStudentPeers(BasePersistanceService):

    def input(self):
        return {
            'user_id': IntegerValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.array_of(x, User) or x == []

    def execute(self, args):

        user_id = args.get('user_id')

        students = aliased(User, name='students')
        me = aliased(User, name='me')

        peers_query = self.session.query(students).\
            join(StudentGroup, students.id == StudentGroup.student_id).\
            join(Group, StudentGroup.group_id == Group.id).\
            join(Subject, Group.subject_id == Subject.id).\
            join(TeacherSubject, Subject.id == TeacherSubject.subject_id).\
            join(me, TeacherSubject.teacher_id == me.id).\
            filter(me.id == user_id)

        peers = peers_query.all()

        return peers
