from api.lib.decorators import login_required, user_belongs_to_subject, subject_exists, is_teacher, auth_token_required
from api.lib.mixins import ListAPIViewMixin, ModelResponseMixin
from application.services.user import GetSubjectTeachers, GetSubjectStudents, GetUserAuthTokenByUserAndPassword
from common.auth import encode_password


class LoginView(ListAPIViewMixin, ModelResponseMixin):

    @login_required
    def get_action(self, *args, **kwargs):
        qs = self.get_data()
        user = qs.get('user')
        password = qs.get('password')
        password_encoded = encode_password(password)

        get_auth_token_srv = GetUserAuthTokenByUserAndPassword()

        token = get_auth_token_srv.call({
            'user': user,
            'password': password_encoded
        })

        return {'token': token}


class SubjectTeachersView(ListAPIViewMixin, ModelResponseMixin):

    @auth_token_required
    @subject_exists
    @user_belongs_to_subject
    def get_action(self, *args, **kwargs):

        subject_id = kwargs.get('subject_id')

        get_subject_teachers_srv = GetSubjectTeachers()
        teachers = get_subject_teachers_srv.call({'subject_id': subject_id})
        return teachers


class SubjectStudentsView(ListAPIViewMixin, ModelResponseMixin):

    @auth_token_required
    @is_teacher
    @subject_exists
    @user_belongs_to_subject
    def get_action(self, *args, **kwargs):

        subject_id = kwargs.get('subject_id')

        get_subject_students_srv = GetSubjectStudents()
        students = get_subject_students_srv.call({'subject_id': subject_id})
        return students


class ProfileView(ListAPIViewMixin, ModelResponseMixin):

    @auth_token_required
    def get_action(self, *args, **kwargs):

        user = kwargs.get('user')
        return user
