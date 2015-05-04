from datetime import datetime
from api.exceptions.message import MessageNotFoundErorr

from api.lib.decorators import user_belongs_to_subject, group_exists, user_belongs_to_group, \
    group_belongs_to_subject, auth_token_required, subject_exists, message_belongs_to_subject, \
    message_belongs_to_group, message_exists, validate, peer_exists, users_can_conversate, message_belongs_to_peers
from api.lib.mixins import ListAPIViewMixin, CreateAPIViewMixin, ModelResponseMixin, PaginatedResponseMixin
from application.lib.validators import IntegerValidator, StringValidator
from application.services.message import GetGroupMessages, PutGroupMessage, PutSubjectMessage, GetSubjectMessages, \
    GetMessage, GetDirectMessages, PutDirectMessage


class ListSubjectMessagesView(ListAPIViewMixin, PaginatedResponseMixin):
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
        get_subject_messages_srv = GetSubjectMessages()
        messages = get_subject_messages_srv.call({'subject_id': subject_id})
        return messages


class ListPaginatedSubjectMessagesView(ListAPIViewMixin, PaginatedResponseMixin):
    def params(self):
        return {
            'subject_id': [self.PARAM_URL, IntegerValidator({'required': True})],
            'message_id': [self.PARAM_URL, IntegerValidator({'required': True})],
            'direction': [self.PARAM_URL, StringValidator({'required': True})],
            'order': [self.PARAM_GET, StringValidator({'required': False})],
        }

    @validate
    @auth_token_required
    @subject_exists
    @user_belongs_to_subject
    @message_exists
    @message_belongs_to_subject
    def get_action(self, *args, **kwargs):
        subject_id = kwargs.get('url').get('subject_id')
        message_id = kwargs.get('url').get('message_id')
        direction = kwargs.get('url').get('direction')
        order = kwargs.get('get').get('order')

        get_subject_messages_srv = GetSubjectMessages()
        messages = get_subject_messages_srv.call({
            'subject_id': subject_id,
            'message_id': message_id,
            'order': order,
            'direction': direction
        })

        return messages


class PostSubjectMessageView(CreateAPIViewMixin, ModelResponseMixin):
    def params(self):
        return {
            'subject_id': [self.PARAM_URL, IntegerValidator({'required': True})],
            'body': [self.PARAM_POST, StringValidator({'required': True})],
        }

    @validate
    @auth_token_required
    @subject_exists
    @user_belongs_to_subject
    def post_action(self, *args, **kwargs):

        user = kwargs.get('user')
        subject_id = kwargs.get('url').get('subject_id')

        body = kwargs.get('post').get('body')

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
            'group_id': [self.PARAM_URL, IntegerValidator({'required': True})]
        }

    @validate
    @auth_token_required
    @subject_exists
    @group_exists
    @group_belongs_to_subject
    @user_belongs_to_group
    def get_action(self, *args, **kwargs):
        group_id = kwargs.get('url').get('group_id')

        get_group_messages_srv = GetGroupMessages()
        messages = get_group_messages_srv.call({'group_id': group_id})

        return messages


class ListPaginatedGroupMessagesView(ListAPIViewMixin, PaginatedResponseMixin):
    def params(self):
        return {
            'group_id': [self.PARAM_URL, IntegerValidator({'required': True})],
            'message_id': [self.PARAM_URL, IntegerValidator({'required': True})],
            'direction': [self.PARAM_URL, StringValidator({'required': True})],
            'order': [self.PARAM_GET, StringValidator({'required': False})],
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
        message_id = kwargs.get('url').get('message_id')
        direction = kwargs.get('url').get('direction')
        order = kwargs.get('get').get('order')

        get_group_messages_srv = GetGroupMessages()
        messages = get_group_messages_srv.call({
            'group_id': group_id,
            'message_id': message_id,
            'order': order,
            'direction': direction
        })

        return messages


class PostGroupMessageView(CreateAPIViewMixin, ModelResponseMixin):
    def params(self):
        return {
            'subject_id': [self.PARAM_URL, IntegerValidator({'required': True})],
            'group_id': [self.PARAM_URL, IntegerValidator({'required': True})],
            'body': [self.PARAM_POST, StringValidator({'required': True})],
        }

    @validate
    @auth_token_required
    @subject_exists
    @group_exists
    @group_belongs_to_subject
    @user_belongs_to_group
    def post_action(self, *args, **kwargs):

        user = kwargs.get('user')
        group_id = kwargs.get('url').get('group_id')
        body = kwargs.get('post').get('body')

        put_group_message_srv = PutGroupMessage()
        message = put_group_message_srv.call({
            'sender_id': user.id,
            'body': body,
            'created_at': datetime.now(),
            'recipient_id': group_id})

        return message


class ListDirectMessagesView(ListAPIViewMixin, PaginatedResponseMixin):

    def params(self):
        return {
            'peer_id': [self.PARAM_URL, IntegerValidator({'required': True})],
        }

    @validate
    @auth_token_required
    @peer_exists
    @users_can_conversate
    def get_action(self, *args, **kwargs):
        user = kwargs.get('user')
        peer_id = kwargs.get('peer_id')

        get_direct_messages_srv = GetDirectMessages()
        messages = get_direct_messages_srv.call({
            'sender_id': user.id,
            'recipient_id': peer_id,
        })

        return messages


class ListPaginatedDirectMessagesView(ListAPIViewMixin, PaginatedResponseMixin):

    def params(self):
        return {
            'peer_id': [self.PARAM_URL, IntegerValidator({'required': True})],
            'message_id': [self.PARAM_URL, IntegerValidator({'required': True})],
            'direction': [self.PARAM_URL, StringValidator({'required': True})],
            'order': [self.PARAM_GET, StringValidator({'required': False})],
        }

    @validate
    @auth_token_required
    @peer_exists
    @users_can_conversate
    @message_exists
    @message_belongs_to_peers
    def get_action(self, *args, **kwargs):
        user = kwargs.get('user')
        peer_id = kwargs.get('peer_id')

        message_id = kwargs.get('url').get('message_id')
        direction = kwargs.get('url').get('direction')
        order = kwargs.get('get').get('order')

        get_direct_messages_srv = GetDirectMessages()
        messages = get_direct_messages_srv.call({
            'sender_id': user.id,
            'recipient_id': peer_id,
            'message_id': message_id,
            'order': order,
            'direction': direction
        })

        return messages


class PostDirectMessageView(CreateAPIViewMixin, ModelResponseMixin):

    def params(self):
        return {
            'peer_id': [self.PARAM_URL, IntegerValidator({'required': True})],
            'body': [self.PARAM_POST, StringValidator({'required': True})]
        }

    @validate
    @auth_token_required
    @peer_exists
    @users_can_conversate
    def post_action(self, *args, **kwargs):

        user = kwargs.get('user')
        peer_id = kwargs.get('url').get('peer_id')
        body = kwargs.get('post').get('body')

        put_subject_message_srv = PutDirectMessage()
        message = put_subject_message_srv.call({
            'sender_id': user.id,
            'body': body,
            'created_at': datetime.now(),
            'recipient_id': peer_id})

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
    def params(self):
        return {
            'subject_id': [self.PARAM_URL, IntegerValidator({'required': True})],
            'message_id': [self.PARAM_URL, IntegerValidator({'required': True})]
        }

    @validate
    @auth_token_required
    @subject_exists
    @user_belongs_to_subject
    @message_exists
    @message_belongs_to_subject
    def get_action(self, *args, **kwargs):
        return super(SubjectMessageDetailView, self).get_action(*args, **kwargs)


class GroupMessageDetailView(MessageDetailView):
    def params(self):
        return {
            'subject_id': [self.PARAM_URL, IntegerValidator({'required': True})],
            'group_id': [self.PARAM_URL, IntegerValidator({'required': True})],
            'message_id': [self.PARAM_URL, IntegerValidator({'required': True})],
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
        return super(GroupMessageDetailView, self).get_action(*args, **kwargs)
