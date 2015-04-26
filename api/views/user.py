from api.lib.decorators import login_required, user_belongs_to_subject, subject_exists, is_teacher, auth_token_required, \
    validate, group_exists, user_belongs_to_group, user_can_see_teacher, teacher_exists, teacher_can_see_student, \
    student_exists
from api.lib.mixins import ListAPIViewMixin, ModelResponseMixin
from application.lib.validators import IntegerValidator, StringValidator
from application.services.user import GetSubjectTeachers, GetSubjectStudents, GetUserAuthTokenByUserAndPassword, \
    GetGroupStudents, GetTeacherTeacherPeers, GetStudentTeacherPeers, GetUserTeacherPeers, GetTeacherStudentPeers, \
    GetUser, GetUserConversators
from common.auth import encode_password


class LoginView(ListAPIViewMixin):

    def params(self):
        return {
            'user': [self.PARAM_GET, StringValidator({'required': True})],
            'password': [self.PARAM_GET, StringValidator({'required': True})]
        }

    @validate
    @login_required
    def get_action(self, *args, **kwargs):
        user = kwargs.get('get').get('user')
        password = kwargs.get('get').get('password')
        password_encoded = encode_password(password)

        get_auth_token_srv = GetUserAuthTokenByUserAndPassword()

        token = get_auth_token_srv.call({
            'user': user,
            'password': password_encoded
        })

        return {'token': token}


class SubjectTeachersView(ListAPIViewMixin, ModelResponseMixin):

    def params(self):
        return {
            'subject_id': [self.PARAM_URL, IntegerValidator({'required': True})]
        }

    @validate
    @auth_token_required
    @subject_exists
    @user_belongs_to_subject
    def get_action(self, *args, **kwargs):

        subject_id = kwargs.get('url').get('subject_id')

        get_subject_teachers_srv = GetSubjectTeachers()
        teachers = get_subject_teachers_srv.call({'subject_id': subject_id})
        return teachers


class SubjectStudentsView(ListAPIViewMixin, ModelResponseMixin):

    def params(self):
        return {
            'subject_id': [self.PARAM_URL, IntegerValidator({'required': True})]
        }

    @validate
    @auth_token_required
    @is_teacher
    @subject_exists
    @user_belongs_to_subject
    def get_action(self, *args, **kwargs):

        subject_id = kwargs.get('url').get('subject_id')

        get_subject_students_srv = GetSubjectStudents()
        students = get_subject_students_srv.call({'subject_id': subject_id})
        return students


class GroupStudentsView(ListAPIViewMixin, ModelResponseMixin):

    def params(self):
        return {
            'subject_id': [self.PARAM_URL, IntegerValidator({'required': True})],
            'group_id': [self.PARAM_URL, IntegerValidator({'required': True})]
        }

    @validate
    @auth_token_required
    @subject_exists
    @group_exists
    @user_belongs_to_group
    def get_action(self, *args, **kwargs):
        group_id = kwargs.get('url').get('group_id')

        get_group_students_srv = GetGroupStudents()
        students = get_group_students_srv.call({'group_id': group_id})
        return students


class UserPeerView(ListAPIViewMixin, ModelResponseMixin):

    def get_action(self, *args, **kwargs):
        peer_id = kwargs.get('peer_id')
        get_user_srv = GetUser()
        chats = get_user_srv.call({'user_id': peer_id})
        return chats


class TeacherPeersView(ListAPIViewMixin, ModelResponseMixin):

    @auth_token_required
    def get_action(self, *args, **kwargs):
        user = kwargs.get('user')
        get_teacher_peers = GetUserTeacherPeers()
        peers = get_teacher_peers.call({'user_id': user.id})
        return peers


class TeacherPeerView(UserPeerView):

    def params(self):
        return {
            'teacher_id': [self.PARAM_URL, IntegerValidator({'required': True})]
        }

    @validate
    @auth_token_required
    @teacher_exists
    @user_can_see_teacher
    def get_action(self, *args, **kwargs):
        kwargs['peer_id'] = kwargs.get('url').get('teacher_id')
        return super(TeacherPeerView, self).get_action(*args, **kwargs)


class StudentPeersView(ListAPIViewMixin, ModelResponseMixin):

    @auth_token_required
    @is_teacher
    def get_action(self, *args, **kwargs):

        user = kwargs.get('user')
        get_student_peers = GetTeacherStudentPeers()
        peers = get_student_peers.call({'user_id': user.id})
        return peers


class StudentPeerView(ListAPIViewMixin, ModelResponseMixin):

    def params(self):
        return {
            'student_id': IntegerValidator({'required': True})
        }

    @validate
    @auth_token_required
    @is_teacher
    @student_exists
    @teacher_can_see_student
    def get_action(self, *args, **kwargs):
        kwargs['peer_id'] = kwargs.get('url').get('student_id')
        return super(StudentPeerView, self).get_action(*args, **kwargs)


class UserChatsView(ListAPIViewMixin, ModelResponseMixin):

    @auth_token_required
    def get_action(self, *args, **kwargs):

        user = kwargs.get('user')

        get_conversators_srv = GetUserConversators()
        chats = get_conversators_srv.call({'user_id': user.id})

        return chats


class ProfileView(ListAPIViewMixin, ModelResponseMixin):

    @auth_token_required
    def get_action(self, *args, **kwargs):

        user = kwargs.get('user')
        return user
