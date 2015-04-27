from api.lib.decorators import auth_token_required, validate, users_can_conversate, peer_exists
from api.lib.mixins import ListAPIViewMixin
from application.lib.validators import IntegerValidator
from application.services.conversation import GetUserConversations, GetConversationBetweenUsers


class ListConversationsView(ListAPIViewMixin):

    @auth_token_required
    def get_action(self, *args, **kwargs):

        user = kwargs.get('user')
        get_conversations_srv = GetUserConversations()
        conversations = get_conversations_srv.call({'user_id': user.id})

        return conversations


class ConversationDetailView(ListAPIViewMixin):

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
        peer_id = kwargs.get('url').get('peer_id')

        get_conversation_srv = GetConversationBetweenUsers()
        conversation = get_conversation_srv.call({
            'my_id': user.id,
            'its_id': peer_id
        })

        return conversation