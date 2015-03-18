from api.decorators import login_required, check_subject_exists, belong_to_subject
from api.mixins import ListAPIViewMixin, CreateAPIViewMixin
from application.services.group import GetUserGroups
from application.services.message import PutSubjectMessage, GetSubjectMessages
from application.services.subject import GetUserSubjects, GetUserSubject

from datetime import datetime


class SubjectsView(ListAPIViewMixin):

    def __init__(self):
        self.kwargs = {
            'with_student_group': False,
            'with_groups': False
        }

    @login_required
    def get_action(self, *args, **kwargs):
        user = kwargs.get('user')

        if user.is_teacher():
            self.kwargs['with_groups'] = True
        elif user.is_student():
            self.kwargs['with_student_group'] = True

        get_user_subjects_srv = GetUserSubjects()
        subjects = get_user_subjects_srv.call({'user_id': user.id})
        return subjects


class SubjectDetailView(ListAPIViewMixin):

    def __init__(self):
        self.kwargs = {
            'with_student_group': False,
            'with_groups': False
        }

    @login_required
    @check_subject_exists
    @belong_to_subject
    def get_action(self, *args, **kwargs):

        user = kwargs.get('user')
        subject_id = kwargs.get('subject_id')

        if user.is_teacher():
            self.kwargs['with_groups'] = True
        elif user.is_student():
            self.kwargs['with_student_group'] = True

        get_subject_srv = GetUserSubject()
        subject = get_subject_srv.call({'subject_id': subject_id, 'user_id': user.id})
        return subject


class GroupsView(ListAPIViewMixin):

    @login_required
    def get_action(self, *args, **kwargs):
        user = kwargs.get('user')
        get_user_groups_srv = GetUserGroups()
        groups = get_user_groups_srv.call({'user_id': user.id})
        return groups


class SubjectMessagesView(ListAPIViewMixin, CreateAPIViewMixin):

    @login_required
    @check_subject_exists
    @belong_to_subject
    def post_action(self, *args, **kwargs):
        post_data = self.post_data()

        user = kwargs.get('user')
        subject_id = kwargs.get('subject_id')

        body = post_data.get('body')

        put_subject_message_srv = PutSubjectMessage()
        message = put_subject_message_srv.call({
            'sender_id': user.id,
            'body': body,
            'created_at': datetime.now(),
            'recipient_id': subject_id})

        return message

    @login_required
    @check_subject_exists
    @belong_to_subject
    def get_action(self, *args, **kwargs):

        subject_id = kwargs.get('subject_id')
        get_subject_messages_srv = GetSubjectMessages()
        messages = get_subject_messages_srv.call({'subject_id': subject_id})
        return messages
