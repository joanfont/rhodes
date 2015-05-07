from api.lib.decorators import auth_token_required
from api.lib.mixins import ListAPIViewMixin, ModelResponseMixin
from application.services.message import GetUserSubjectsLastMessages, GetUserGroupsLastMessages, \
    GetUserConversationsLastMessages


class MessagesNotificationsView(ListAPIViewMixin):

    @auth_token_required
    def get_action(self, *args, **kwargs):

        def serialize(x):
            return x.to_dict()

        user = kwargs.get('user')

        get_last_subject_messages = GetUserSubjectsLastMessages()
        subject_messages = get_last_subject_messages.call({
            'user_id': user.id
        })

        subject_messages_serialized = map(serialize, subject_messages)

        get_last_group_messages = GetUserGroupsLastMessages()
        group_messages = get_last_group_messages.call({
            'user_id': user.id
        })
        group_messages_serialized = map(serialize, group_messages)

        get_last_conversations_messages = GetUserConversationsLastMessages()
        direct_messages = get_last_conversations_messages.call({
            'user_id': user.id
        })
        direct_messages_serialized = map(serialize, direct_messages)

        return {
            'subjects': subject_messages_serialized,
            'groups': group_messages_serialized,
            'chats': direct_messages_serialized
        }



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

