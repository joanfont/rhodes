from datetime import datetime
from api.exceptions.message import MessageNotFoundErorr

from api.lib.decorators import user_belongs_to_subject, group_exists, user_belongs_to_group, \
    group_belongs_to_subject, auth_token_required, subject_exists
from api.lib.mixins import ListAPIViewMixin, CreateAPIViewMixin, ModelResponseMixin
from application.services.message import GetGroupMessages, PutGroupMessage, PutSubjectMessage, GetSubjectMessages, \
    GetMessage


class SubjectMessagesView(ListAPIViewMixin, CreateAPIViewMixin, ModelResponseMixin):

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


class GroupMessagesView(ListAPIViewMixin, CreateAPIViewMixin, ModelResponseMixin):

    @auth_token_required
    @subject_exists
    @user_belongs_to_subject
    @group_exists
    @group_belongs_to_subject
    @user_belongs_to_group
    def get_action(self, *args, **kwargs):

        group_id = kwargs.get('group_id')
        get_group_messages_srv = GetGroupMessages()
        messages = get_group_messages_srv.call({'group_id': group_id})
        return messages

    @auth_token_required
    @subject_exists
    @user_belongs_to_subject
    @group_exists
    @group_belongs_to_subject
    @user_belongs_to_group
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


class MessageDetailView(ListAPIViewMixin, ModelResponseMixin):

    def get_action(self, *args, **kwargs):

        message_id = kwargs.get('message_id')
        print message_id
        get_message_srv = GetMessage()

        message = get_message_srv.call({'message_id': message_id})

        if not message:
            raise MessageNotFoundErorr()

        return message


class SubjectMessageDetailView(MessageDetailView):

    @auth_token_required
    @subject_exists
    @user_belongs_to_subject
    def get_action(self, *args, **kwargs):
        return super(SubjectMessageDetailView, self).get_action(*args, **kwargs)


class GroupMessageDetailView(MessageDetailView):

    @auth_token_required
    @subject_exists
    @user_belongs_to_subject
    @group_exists
    @group_belongs_to_subject
    @user_belongs_to_group
    def get_action(self, *args, **kwargs):
        return super(GroupMessageDetailView, self).get_action(*args, **kwargs)


