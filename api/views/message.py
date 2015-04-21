from datetime import datetime
from api.exceptions.message import MessageNotFoundErorr

from api.lib.decorators import user_belongs_to_subject, group_exists, user_belongs_to_group, \
    group_belongs_to_subject, auth_token_required, subject_exists, message_belongs_to_subject, \
    message_belongs_to_group, message_exists, validate
from api.lib.mixins import ListAPIViewMixin, CreateAPIViewMixin, ModelResponseMixin, PaginatedResponseMixin
from application.lib.validators import IntegerValidator, StringValidator
from application.services.message import GetGroupMessages, PutGroupMessage, PutSubjectMessage, GetSubjectMessages, \
    GetMessage


class ListSubjectMessagesView(ListAPIViewMixin, PaginatedResponseMixin):

    def params(self):
        return {
            'subject_id': [self.PARAM_URL, IntegerValidator({'required': True})],
            'message_id': [self.PARAM_GET, IntegerValidator({'required': False})],
            'order': [self.PARAM_GET, StringValidator({'required': False})],
            'direction': [self.PARAM_GET, StringValidator({'required': False})]
        }

    @validate
    @auth_token_required
    @subject_exists
    @user_belongs_to_subject
    @message_exists
    @message_belongs_to_subject
    def get_action(self, *args, **kwargs):

        subject_id = kwargs.get('url').get('subject_id')
        message_id = kwargs.get('get').get('message_id')
        order = kwargs.get('get').get('order')
        direction = kwargs.get('get').get('direction')

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
        subject_id = kwargs.get('url').get('subject_id')

        body = post_data.get('body')

        put_subject_message_srv = PutSubjectMessage()
        message = put_subject_message_srv.call({
            'sender_id': user.id,
            'body': body,
            'created_at': datetime.now(),
            'recipient_id': subject_id})

        return message


class ListGroupMessagesView(ListAPIViewMixin, PaginatedResponseMixin):

    def params(self):
        return {
            'group_id': [self.PARAM_URL, IntegerValidator({'required': True})],
            'message_id': [self.PARAM_GET, IntegerValidator({'required': False})],
            'order': [self.PARAM_GET, StringValidator({'required': False})],
            'direction': [self.PARAM_GET, StringValidator({'required': False})]
        }

    @validate
    @auth_token_required
    @subject_exists
    @group_exists
    @group_belongs_to_subject
    @user_belongs_to_group
    @message_exists
    @message_belongs_to_group
    def get_action(self, *args, **kwargs):

        group_id = kwargs.get('url').get('group_id')
        message_id = kwargs.get('get').get('message_id')
        order = kwargs.get('get').get('order')
        direction = kwargs.get('get').get('direction')

        get_group_messages_srv = GetGroupMessages()
        messages = get_group_messages_srv.call({
            'group_id': group_id,
            'message_id': message_id,
            'order': order,
            'direction': direction
        })

        return messages


class PostGroupMessageView(CreateAPIViewMixin, ModelResponseMixin):

    @auth_token_required
    @subject_exists
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

        message_id = kwargs.get('url').get('message_id')
        get_message_srv = GetMessage()

        message = get_message_srv.call({'message_id': message_id})

        if not message:
            raise MessageNotFoundErorr()

        return message


class SubjectMessageDetailView(MessageDetailView):

    @auth_token_required
    @subject_exists
    @user_belongs_to_subject
    @message_exists
    @message_belongs_to_subject
    def get_action(self, *args, **kwargs):
        return super(SubjectMessageDetailView, self).get_action(*args, **kwargs)


class GroupMessageDetailView(MessageDetailView):

    @auth_token_required
    @subject_exists
    @group_exists
    @group_belongs_to_subject
    @user_belongs_to_group
    @message_exists
    @message_belongs_to_group
    def get_action(self, *args, **kwargs):
        return super(GroupMessageDetailView, self).get_action(*args, **kwargs)


