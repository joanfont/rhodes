from sqlalchemy import or_
from application.services.base import BasePersistanceService, BaseService
from application.lib.validators import IntegerValidator, StringValidator
from common.helper import Helper
from application.lib.models import User, StudentGroup, Group, Subject, TeacherSubject, UserType, DirectMessage
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
            filter(Subject.id == subject_id). \
            order_by(User.last_name.asc(), User.first_name.asc()).all()

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
            filter(Subject.id == subject_id). \
            order_by(User.last_name.asc(), User.first_name.asc()).all()

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
            filter(Group.id == group_id). \
            order_by(User.last_name.asc(), User.first_name.asc()).all()

        return students


class GetTeacherTeacherPeers(BasePersistanceService):

    """ Retrieves the teachers of all the subjects a teacher teaches """

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

        """ SELECT others.* FROM user AS others
            INNER JOIN teacher_subject AS ts1 ON others.id = ts1.teacher_id
            INNER JOIN subject ON ts1.subject_id = ts1.subject_id
            INNER JOIN teacher_subject AS ts2 ON subject.id = ts2.subject_id
            INNER JOIN user AS me on me.id = ts2.teacher_id
            WHERE me.id == :my_id AND others.id <> :my_id; """

        peers_query = self.session.query(others).\
            join(their_teacher_subject, their_teacher_subject.teacher_id == others.id).\
            join(Subject, their_teacher_subject.subject_id == Subject.id).\
            join(my_teacher_subject, Subject.id == my_teacher_subject.subject_id).\
            join(me, my_teacher_subject.teacher_id == me.id).\
            filter(me.id == user_id).\
            filter(others.id != user_id).\
            order_by(others.last_name.asc(), others.first_name.asc())

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
            filter(me.id == user_id).\
            order_by(teachers.last_name.asc(), teachers.first_name.asc())

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
            filter(me.id == user_id).\
            order_by(students.last_name.asc(), students.first_name.asc())

        peers = peers_query.all()

        return peers


class GetStudentStudentPeers(BasePersistanceService):

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

        their_student_group = aliased(StudentGroup, name='their_student_group')
        my_student_group = aliased(StudentGroup, name='my_student_gruop')

        peers_query = self.session.query(students).\
            join(their_student_group, students.id == their_student_group.student_id).\
            join(Group, their_student_group.group_id == Group.id).\
            join(my_student_group, Group.id == my_student_group.group_id).\
            join(me, my_student_group.student_id == me.id).\
            filter(me.id == user_id).\
            filter(students.id != user_id).\
            order_by(students.last_name.asc(), students.first_name.asc())

        peers = peers_query.all()

        return peers


class GetUserStudentPeers(BaseService):

    def input(self):
        return {
            'user_id': IntegerValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.array_of(x, User) or x == []

    def execute(self, args):

        user_id = args.get('user_id')

        dispatcher = {
            UserType.TEACHER: GetTeacherStudentPeers,
            UserType.STUDENT: GetStudentStudentPeers
        }

        get_user_srv = GetUser()
        user = get_user_srv.call({'user_id': user_id})

        get_student_peers_cls = dispatcher.get(user.type_id)
        get_student_peers = get_student_peers_cls()

        peers = get_student_peers.call({'user_id': user_id})

        return peers

class TeacherCanSeeTeacher(BasePersistanceService):

    def input(self):
        return {
            'teacher_id': IntegerValidator({'required': True}),
            'user_id': IntegerValidator({'required': True}),
        }

    def output(self):
        return lambda x: Helper.instance_of(x, bool)

    def execute(self, args):
        teacher_id = args.get('teacher_id')
        user_id = args.get('user_id')

        me = aliased(User, name='me')
        other = aliased(User, name='other')
        my_teacher_subject = aliased(TeacherSubject, name='ts1')
        their_teacher_subject = aliased(TeacherSubject, name='ts2')

        peers_query = self.session.query(other).\
            join(their_teacher_subject, their_teacher_subject.teacher_id == other.id).\
            join(Subject, their_teacher_subject.subject_id == Subject.id).\
            join(my_teacher_subject, Subject.id == my_teacher_subject.subject_id).\
            join(me, my_teacher_subject.teacher_id == me.id).\
            filter(me.id == user_id).\
            filter(other.id == teacher_id)

        return peers_query.count() > 0


class StudentCanSeeTeacher(BasePersistanceService):

    def input(self):
        return {
            'teacher_id': IntegerValidator({'required': True}),
            'user_id': IntegerValidator({'required': True}),
        }

    def output(self):
        return lambda x: Helper.instance_of(x, bool)

    def execute(self, args):

        teacher_id = args.get('teacher_id')
        user_id = args.get('user_id')

        teacher = aliased(User, name='teacher')
        me = aliased(User, name='me')

        peers_query = self.session.query(teacher).\
            join(TeacherSubject, teacher.id == TeacherSubject.teacher_id).\
            join(Subject, TeacherSubject.subject_id == Subject.id).\
            join(Group, Subject.id == Group.subject_id).\
            join(StudentGroup, Group.id == StudentGroup.group_id).\
            join(me, StudentGroup.student_id == me.id).\
            filter(me.id == user_id).\
            filter(teacher.id == teacher_id)

        return peers_query.count() > 0


class UserCanSeeTeacher(BaseService):

    def input(self):
        return {
            'teacher_id': IntegerValidator({'required': True}),
            'user_id': IntegerValidator({'required': True}),
        }

    def output(self):
        return lambda x: Helper.instance_of(x, bool)

    def execute(self, args):

        user_id = args.get('user_id')

        dispatcher = {
            UserType.TEACHER: TeacherCanSeeTeacher,
            UserType.STUDENT: StudentCanSeeTeacher
        }

        get_user_srv = GetUser()
        user = get_user_srv.call({'user_id': user_id})

        can_see_teacher_srv_cls = dispatcher.get(user.type_id)
        can_see_teacher_srv = can_see_teacher_srv_cls()

        peers = can_see_teacher_srv.call(args)

        return peers


class TeacherCanSeeStudent(BasePersistanceService):

    def input(self):
        return {
            'student_id': IntegerValidator({'required': True}),
            'user_id': IntegerValidator({'required': True}),
        }

    def output(self):
        return lambda x: Helper.instance_of(x, bool)

    def execute(self, args):

        student_id = args.get('student_id')
        user_id = args.get('user_id')

        student = aliased(User, name='student')
        me = aliased(User, name='me')

        peers_query = self.session.query(student).\
            join(StudentGroup, student.id == StudentGroup.student_id).\
            join(Group, StudentGroup.group_id == Group.id).\
            join(Subject, Group.subject_id == Subject.id).\
            join(TeacherSubject, Subject.id == TeacherSubject.subject_id).\
            join(me, TeacherSubject.teacher_id == me.id).\
            filter(me.id == user_id).\
            filter(student.id == student_id)

        return peers_query.count() > 0


class GetUserConversators(BasePersistanceService):

    def input(self):
        return {
            'user_id': IntegerValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.array_of(x, User) or x == []

    def execute(self, args):

        user_id = args.get('user_id')

        users_query = self.session.query(User).\
            join(DirectMessage, or_(User.id == DirectMessage.sender_id, User.id == DirectMessage.user_id)).\
            filter(or_(DirectMessage.sender_id == user_id, DirectMessage.user_id == user_id)).\
            filter(User.id != user_id).\
            order_by(User.last_name.asc(), User.first_name.asc())

        users = users_query.all()

        return users


class CheckConversationExistsBetweenUsers(BasePersistanceService):

    def input(self):
        return {
            'user_id_1': IntegerValidator({'required': True}),
            'user_id_2': IntegerValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.instance_of(x, bool)

    def execute(self, args):

        user_id_1 = args.get('user_id_1')
        user_id_2 = args.get('user_id_2')

        users_query = self.session.query(User).\
            join(DirectMessage, or_(User.id == DirectMessage.sender_id, User.id == DirectMessage.user_id)).\
            filter(or_(DirectMessage.sender_id == user_id_1, DirectMessage.sender_id == user_id_2))

        return users_query.count() > 0
