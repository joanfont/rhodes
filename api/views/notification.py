from api.lib.decorators import auth_token_required
from api.lib.mixins import ListAPIViewMixin, ModelResponseMixin
from application.services.message import GetUserSubjectsLastMessages, GetUserGroupsLastMessages, \
    GetUserConversationsLastMessages


class SubjectMessagesNotificationsView(ListAPIViewMixin, ModelResponseMixin):

    @auth_token_required
    def get_action(self, *args, **kwargs):

        user = kwargs.get('user')

        get_last_subject_messages = GetUserSubjectsLastMessages()
        messages = get_last_subject_messages.call({
            'user_id': user.id
        })

        return messages


class GroupMessagesNotificationsView(ListAPIViewMixin, ModelResponseMixin):

    @auth_token_required
    def get_action(self, *args, **kwargs):

        user = kwargs.get('user')

        get_last_group_messages = GetUserGroupsLastMessages()
        messages = get_last_group_messages.call({
            'user_id': user.id
        })

        return messages


class ConversationNotificationsView(ListAPIViewMixin, ModelResponseMixin):

    @auth_token_required
    def get_action(self, *args, **kwargs):

        user = kwargs.get('user')

        get_last_conversations_messages = GetUserConversationsLastMessages()
        messages = get_last_conversations_messages.call({
            'user_id': user.id
        })

        return messages

