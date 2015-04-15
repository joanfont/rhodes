from datetime import datetime
from api.exceptions.message import MessageNotFoundErorr

from api.lib.decorators import user_belongs_to_subject, group_exists, user_belongs_to_group, \
    group_belongs_to_subject, auth_token_required, subject_exists
from api.lib.mixins import ListAPIViewMixin, CreateAPIViewMixin, ModelResponseMixin, PaginatedResponseMixin
from application.services.message import GetGroupMessages, PutGroupMessage, PutSubjectMessage, GetSubjectMessages, \
    GetMessage


class ListSubjectMessagesView(ListAPIViewMixin, PaginatedResponseMixin):

    @auth_token_required
    @subject_exists
    @user_belongs_to_subject
    def get_action(self, *args, **kwargs):

        get_data = self.get_data()

        subject_id = kwargs.get('subject_id')
        message_id = get_data.get('message_id')
        order = get_data.get('order')
        direction = get_data.get('direction')

        get_subject_messages_srv = GetSubjectMessages()
        messages = get_subject_messages_srv.call({
            'subject_id': subject_id,
            'message_id': message_id,
            'order': order,
            'direction': direction
        })
        return messages


class PostSubjectMessageView(CreateAPIViewMixin, ModelResponseMixin):

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


class GroupMessagesView(ListAPIViewMixin, CreateAPIViewMixin, ModelResponseMixin):

    @auth_token_required
    @subject_exists
    @user_belongs_to_subject
    @group_exists
    @group_belongs_to_subject
    @user_belongs_to_group
    def get_action(self, *args, **kwargs):

        group_id = kwargs.get('group_id')

        service_args = {'group_id': group_id}
        get_group_messages_srv = GetGroupMessages()
        messages = get_group_messages_srv.call(service_args)
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


