from api.lib.decorators import user_belongs_to_subject, subject_exists, auth_token_required
from api.lib.mixins import ListAPIViewMixin
from application.services.subject import GetUserSubject, GetUserSubjects


class SubjectsView(ListAPIViewMixin):


    @auth_token_required
    def get_action(self, *args, **kwargs):
        self.response_args['with_groups'] = True

        user = kwargs.get('user')

        get_user_subjects_srv = GetUserSubjects()
        subjects = get_user_subjects_srv.call({'user_id': user.id})
        return subjects


class SubjectDetailView(ListAPIViewMixin):

    @auth_token_required
    @subject_exists
    @user_belongs_to_subject
    def get_action(self, *args, **kwargs):
        self.response_args['with_groups'] = True

        user = kwargs.get('user')
        subject_id = kwargs.get('subject_id')

        get_subject_srv = GetUserSubject()
        subject = get_subject_srv.call({'subject_id': subject_id, 'user_id': user.id})
        return subject



