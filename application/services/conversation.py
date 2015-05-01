from sqlalchemy import or_
from application.lib.entities import Conversation
from application.lib.models import User, DirectMessage, MessageType
from application.lib.validators import IntegerValidator
from application.services.base import BasePersistanceService
from application.services.message import GetLastDirectMessageBetweenUsers
from application.services.user import GetUserConversators, GetUser
from common.helper import Helper


class GetUserConversations(BasePersistanceService):

    def input(self):
        return {
            'user_id': IntegerValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.array_of(x, Conversation) or x == []

    def execute(self, args):

        user_id = args.get('user_id')

        def add_last_message_to_conversation(carry, user):
            get_last_direct_message_srv = GetLastDirectMessageBetweenUsers()
            message = get_last_direct_message_srv.call({
                'my_id': user_id,
                'its_id': user.id})

            conversation = Conversation(user, message)
            carry.append(conversation)
            return carry

        get_conversators_srv = GetUserConversators()
        users = get_conversators_srv.call({'user_id': user_id})

        conversations = reduce(add_last_message_to_conversation, users, [])
        return conversations


class GetConversationBetweenUsers(BasePersistanceService):

    def input(self):
        return {
            'my_id': IntegerValidator({'required': True}),
            'its_id': IntegerValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.instance_of(x, Conversation)

    def execute(self, args):

        my_id = args.get('my_id')
        its_id = args.get('its_id')

        get_user_srv = GetUser()
        user = get_user_srv.call({'user_id': its_id})

        get_last_direct_message_srv = GetLastDirectMessageBetweenUsers()
        message = get_last_direct_message_srv.call({
            'my_id': my_id,
            'its_id': its_id
        })

        return Conversation(user, message)


class CheckConversationExistsBetweenUsers(BasePersistanceService):

    def input(self):
        return {
            'my_id': IntegerValidator({'required': True}),
            'its_id': IntegerValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.instance_of(x, bool)

    def execute(self, args):

        my_id = args.get('my_id')
        its_id = args.get('its_id')

        users_query = self.session.query(DirectMessage).\
            join(User, or_(DirectMessage.sender_id == User.id, DirectMessage.user_id == User.id)).\
            filter(or_(DirectMessage.sender_id == my_id, DirectMessage.sender_id == its_id)).\
            filter(DirectMessage.type == MessageType.DIRECT_MESSAGE)

        return users_query.count() > 0