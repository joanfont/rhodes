from datetime import datetime

from api.views.lib.decorators import user_belongs_to_subject, group_exists, user_belongs_to_group, \
    group_belongs_to_subject, auth_token_required, subject_exists
from api.views.lib.mixins import ListAPIViewMixin, CreateAPIViewMixin
from application.services.message import GetGroupMessages, PutGroupMessage, PutSubjectMessage, GetSubjectMessages


class SubjectMessagesView(ListAPIViewMixin, CreateAPIViewMixin):

    @auth_token_required
    @subject_exists
    @user_belongs_to_subject
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

    @auth_token_required
    @subject_exists
    @user_belongs_to_subject
    def get_action(self, *args, **kwargs):

        subject_id = kwargs.get('subject_id')
        get_subject_messages_srv = GetSubjectMessages()
        messages = get_subject_messages_srv.call({'subject_id': subject_id})
        return messages


class GroupMessagesView(ListAPIViewMixin, CreateAPIViewMixin):

    @auth_token_required
    @subject_exists
    @user_belongs_to_subject
    @group_exists
    @user_belongs_to_group
    @group_belongs_to_subject
    def get_action(self, *args, **kwargs):

        group_id = kwargs.get('group_id')

        get_group_messages_srv = GetGroupMessages()
        messages = get_group_messages_srv.call({'group_id': group_id})

        return messages

    @auth_token_required
    @subject_exists
    @user_belongs_to_subject
    @group_exists
    @user_belongs_to_group
    @group_belongs_to_subject
    def post_action(self, *args, **kwargs):

        post_data = self.post_data()

        user = kwargs.get('user')
        group_id = kwargs.get('group_id')

        body = post_data.get('body')

        put_group_message_srv = PutGroupMessage()
        message = put_group_message_srv.call({
            'sender_id': user.id,
            'body': body,
            'created_at': datetime.now(),
            'recipient_id': group_id})

        return message

