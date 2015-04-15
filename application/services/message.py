from application.lib.models import Message, MessageType, DirectMessage, SubjectMessage, GroupMessage, MessageBody
from application.lib.validators import StringValidator, IntegerValidator, ChoicesValidator, DateValidator
from application.services.base import BasePersistanceService, BaseService
from application.lib.entities import PaginatedMessagesEntity
from common.helper import Helper
from common import constants
from config import config


class GetMessage(BasePersistanceService):
    def input(self):
        return {
            'message_id': IntegerValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.instance_of(x, Message) or x is None

    def execute(self, args):
        message_id = args.get('message_id')

        message_query = self.session.query(Message)

        if message_query.filter(Message.id == message_id).count():
            message = message_query.get(message_id)
        else:
            message = None

        return message


class PutMessageBody(BasePersistanceService):
    def input(self):
        return {
            'body': StringValidator({'required': True, 'max_length': MessageBody.MAX_LENGTH}),
        }

    def output(self):
        return lambda x: Helper.instance_of(x, MessageBody)

    def execute(self, args):
        body = args.get('body')
        message_body = MessageBody(content=body)

        self.session.add(message_body)
        self.session.commit()
        return message_body


class PutMessage(BasePersistanceService):
    def input(self):
        return {
            'sender_id': IntegerValidator({'required': True}),
            'body': StringValidator({'required': True, 'max_length': MessageBody.MAX_LENGTH}),
            'type': ChoicesValidator({'required': True, 'choices': MessageType.CHOICES}),
            'created_at': DateValidator({'required': True}),
            'recipient_id': IntegerValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.instance_of(x, Message)

    @staticmethod
    def get_message_instance(message_type):
        dispatcher = {
            MessageType.DIRECT_MESSAGE: DirectMessage,
            MessageType.GROUP_MESSAGE: GroupMessage,
            MessageType.SUBJECT_MESSAGE: SubjectMessage
        }

        return dispatcher.get(message_type)

    @staticmethod
    def adapt_args(args):
        recipient_id = args.get('recipient_id')
        message_type = args.get('type')

        dispatcher = {
            MessageType.DIRECT_MESSAGE: 'user_id',
            MessageType.GROUP_MESSAGE: 'group_id',
            MessageType.SUBJECT_MESSAGE: 'subject_id'
        }

        new_key = dispatcher.get(message_type)
        args[new_key] = recipient_id
        args.pop('recipient_id')

    def execute(self, args):
        message_type = args.get('type')
        body = args.pop('body')

        put_message_body_srv = PutMessageBody()
        message_body = put_message_body_srv.call({'body': body})

        message_cls = self.get_message_instance(message_type)
        self.adapt_args(args)

        args['body_id'] = message_body.id
        message = message_cls(**args)

        self.session.add(message)
        self.session.commit()
        return message


class PutMessageInputAndOutputContractMixin(BaseService):
    def input(self):
        return {
            'sender_id': IntegerValidator({'required': True}),
            'body': StringValidator({'required': True, 'max_length': MessageBody.MAX_LENGTH}),
            'created_at': DateValidator({'required': True}),
            'recipient_id': IntegerValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.instance_of(x, Message)

    def execute(self, args):
        raise NotImplementedError()


class PutSubjectMessage(PutMessageInputAndOutputContractMixin, BaseService):
    def execute(self, args):
        args.update({'type': MessageType.SUBJECT_MESSAGE})
        put_message_srv = PutMessage()
        return put_message_srv.call(args)


class PutGroupMessage(PutMessageInputAndOutputContractMixin, BaseService):
    def execute(self, args):
        args.update({'type': MessageType.GROUP_MESSAGE})
        put_message_srv = PutMessage()
        return put_message_srv.call(args)


class GetSubjectMessages(BasePersistanceService):

    def input(self):
        return {
            'subject_id': IntegerValidator({'required': True}),

            'items': IntegerValidator({'required': False, 'default': config.ITEMS_PER_PAGE}),
            'message_id': IntegerValidator({'required': False}),
            'order': ChoicesValidator({
                'required': False,
                'choices': constants.ORDER_CHOICES,
                'default': constants.ORDER_DESC
            }),

            'direction': ChoicesValidator({
                'required': False,
                'choices': constants.MESSAGES_PAGINATION_CHOICES,
                'default': constants.MESSAGES_PAGINATION_NEXT
            })
        }

    def output(self):
        def _output(x):
            return Helper.instance_of(x, PaginatedMessagesEntity)

        return _output

    def execute(self, args):

        subject_id = args.get('subject_id')
        items = args.get('items')
        message_id = args.get('message_id')
        order = args.get('order')
        direction = args.get('direction')
        more = False

        orders = {
            constants.ORDER_ASC: SubjectMessage.created_at.asc(),
            constants.ORDER_DESC: SubjectMessage.created_at.desc()
        }

        messages_query = self.session.query(SubjectMessage). \
            filter(SubjectMessage.subject_id == subject_id)

        total = messages_query.count()

        if message_id:

            direction_clause = None
            if direction is constants.MESSAGES_PAGINATION_PREVIOUS:
                direction_clause = messages_query.filter(SubjectMessage.id < message_id)
            elif direction is constants.MESSAGES_PAGINATION_NEXT:
                direction_clause = messages_query.filter(SubjectMessage.id > message_id)

            messages_query = direction_clause

        order_clause = orders.get(order)
        messages_query = messages_query.order_by(order_clause)

        messages_query = messages_query.limit(items)

        count = messages_query.count()
        messages = messages_query.all()

        return PaginatedMessagesEntity(messages, total, count, more)


class GetGroupMessages(BasePersistanceService):

    def input(self):
        return {
            'group_id': IntegerValidator({'required': True}),

            'items': IntegerValidator({'required': False, 'default': config.ITEMS_PER_PAGE}),
            'message_id': IntegerValidator({'required': False}),
            'order': ChoicesValidator({
                'required': False,
                'choices': constants.ORDER_CHOICES,
                'default': constants.ORDER_DESC
            }),

            'direction': ChoicesValidator({
                'required': False,
                'choices': constants.MESSAGES_PAGINATION_CHOICES,
                'default': constants.MESSAGES_PAGINATION_NEXT
            })
        }

    def output(self):
        def _output(x):
            return Helper.instance_of(x, PaginatedMessagesEntity)

        return _output

    def execute(self, args):
        group_id = args.get('group_id')
        items = args.get('items')
        message_id = args.get('message_id')
        order = args.get('order')
        direction = args.get('direction')
        more = False

        orders = {
            constants.ORDER_ASC: SubjectMessage.created_at.asc(),
            constants.ORDER_DESC: SubjectMessage.created_at.desc()
        }

        messages_query = self.session.query(GroupMessage). \
            filter(GroupMessage.group_id == group_id)

        total = messages_query.count()

        if message_id:

            direction_clause = None
            if direction is constants.MESSAGES_PAGINATION_PREVIOUS:
                direction_clause = messages_query.filter(GroupMessage.id < message_id)
            elif direction is constants.MESSAGES_PAGINATION_NEXT:
                direction_clause = messages_query.filter(GroupMessage.id > message_id)

            messages_query = direction_clause

        order_clause = orders.get(order)
        messages_query = messages_query.order_by(order_clause)

        messages_query = messages_query.limit(items)

        count = messages_query.count()
        messages = messages_query.all()

        return PaginatedMessagesEntity(messages, total, count, more)


