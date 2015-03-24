from api.decorators import login_required, user_belongs_to_subject, subject_exists, is_teacher
from api.mixins import ListAPIViewMixin
from application.services.user import GetSubjectTeachers, GetSubjectStudents


class SubjectTeachersView(ListAPIViewMixin):

    @login_required
    @subject_exists
    @user_belongs_to_subject
    def get_action(self, *args, **kwargs):

        subject_id = kwargs.get('subject_id')

        get_subject_teachers_srv = GetSubjectTeachers()
        teachers = get_subject_teachers_srv.call({'subject_id': subject_id})
        return teachers


class SubjectStudentsView(ListAPIViewMixin):

    @login_required
    @is_teacher
    @subject_exists
    @user_belongs_to_subject
    def get_action(self, *args, **kwargs):

        subject_id = kwargs.get('subject_id')

        get_subject_students_srv = GetSubjectStudents()
        students = get_subject_students_srv.call({'subject_id': subject_id})
        return students


class ProfileView(ListAPIViewMixin):

    @login_required
    def get_action(self, *args, **kwargs):

        user = kwargs.get('user')
        return user
