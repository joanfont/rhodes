from api.lib.decorators import login_required, user_belongs_to_subject, subject_exists, is_teacher, auth_token_required, \
    validate, group_exists, user_belongs_to_group, peer_exists, user_is_related_to_peer, peer_is_teacher, \
    peer_is_student, users_can_conversate
from api.lib.mixins import ListAPIViewMixin, ModelResponseMixin
from application.lib.validators import IntegerValidator, StringValidator
from application.services.user import GetSubjectTeachers, GetSubjectStudents, GetUserAuthTokenByUserAndPassword, \
    GetGroupStudents, GetUserTeacherPeers, GetTeacherStudentPeers, GetUserConversators
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


class ListSubjectTeachersView(ListAPIViewMixin, ModelResponseMixin):

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


class ListSubjectStudentsView(ListAPIViewMixin, ModelResponseMixin):

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


class ListGroupStudentsView(ListAPIViewMixin, ModelResponseMixin):

    def params(self):
        return {
            'subject_id': [self.PARAM_URL, IntegerValidator({'required': True})],
            'group_id': [self.PARAM_URL, IntegerValidator({'required': True})]
        }

    @validate
    @auth_token_required
    @is_teacher
    @subject_exists
    @group_exists
    @user_belongs_to_group
    def get_action(self, *args, **kwargs):
        group_id = kwargs.get('url').get('group_id')

        get_group_students_srv = GetGroupStudents()
        students = get_group_students_srv.call({'group_id': group_id})
        return students


class TeacherDetailPeerView(ListAPIViewMixin, ModelResponseMixin):

    def params(self):
        return {
            'peer_id': [self.PARAM_URL, IntegerValidator({'required': True})]
        }

    @validate
    @auth_token_required
    @peer_exists
    @peer_is_teacher
    @user_is_related_to_peer
    def get_action(self, *args, **kwargs):
        peer = kwargs.get('peer')
        return peer


class StudentDetailPeerView(ListAPIViewMixin, ModelResponseMixin):

    def params(self):
        return {
            'peer_id': [self.PARAM_URL, IntegerValidator({'required': True})]
        }

    @validate
    @auth_token_required
    @is_teacher
    @peer_exists
    @peer_is_student
    @user_is_related_to_peer
    def get_action(self, *args, **kwargs):
        peer = kwargs.get('peer')
        return peer


class ListTeacherPeersView(ListAPIViewMixin, ModelResponseMixin):

    @auth_token_required
    def get_action(self, *args, **kwargs):
        user = kwargs.get('user')
        get_teacher_peers = GetUserTeacherPeers()
        peers = get_teacher_peers.call({'user_id': user.id})
        return peers


class ListStudentPeersView(ListAPIViewMixin, ModelResponseMixin):

    @auth_token_required
    @is_teacher
    def get_action(self, *args, **kwargs):

        user = kwargs.get('user')
        get_student_peers = GetTeacherStudentPeers()
        peers = get_student_peers.call({'user_id': user.id})
        return peers


class ListConversatorsView(ListAPIViewMixin, ModelResponseMixin):

    @auth_token_required
    def get_action(self, *args, **kwargs):

        user = kwargs.get('user')
        get_conversations_srv = GetUserConversators()
        conversations = get_conversations_srv.call({'user_id': user.id})

        return conversations


class ConversatorDetailView(ListAPIViewMixin, ModelResponseMixin):

    def params(self):
        return {
            'peer_id': [self.PARAM_URL, IntegerValidator({'required': True})]
        }

    @validate
    @auth_token_required
    @peer_exists
    @users_can_conversate
    def get_action(self, *args, **kwargs):
        peer = kwargs.get('peer')
        return peer


class ProfileView(ListAPIViewMixin, ModelResponseMixin):

    @auth_token_required
    def get_action(self, *args, **kwargs):

        user = kwargs.get('user')
        return user
