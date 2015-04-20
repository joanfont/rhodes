from application.lib.models import Message, MessageType, DirectMessage, SubjectMessage, GroupMessage, MessageBody
from application.lib.validators import StringValidator, IntegerValidator, ChoicesValidator, DateValidator
from application.services.base import BasePersistanceService, BaseService
from application.lib.entities import PaginatedMessagesEntity
from common.helper import Helper
from common import constants
from config import config


class PaginatedMessagesService(BasePersistanceService):

    message_class = None

    def input(self):
        return{
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
        return lambda x: Helper.instance_of(x, PaginatedMessagesEntity)

    def execute(self, args):

        type_condition = {
            SubjectMessage: SubjectMessage.subject_id,
            GroupMessage: GroupMessage.group_id
        }

        orders = {
            constants.ORDER_ASC: SubjectMessage.created_at.asc(),
            constants.ORDER_DESC: SubjectMessage.created_at.desc()
        }

        filter_value = args.get('filter_value')
        items = args.get('items')
        message_id = args.get('message_id')
        order = args.get('order')
        direction = args.get('direction')

        more = False

        message_class = self.message_class
        filter_field = type_condition.get(message_class)

        messages_query = self.session.query(message_class). \
            filter(filter_field == filter_value)

        total = messages_query.count()

        if message_id:

            if direction == constants.MESSAGES_PAGINATION_PREVIOUS:
                direction_clause = messages_query.filter(message_class.id < message_id)
            elif direction == constants.MESSAGES_PAGINATION_NEXT:
                direction_clause = messages_query.filter(message_class.id > message_id)
            else:
                direction_clause = None

            if direction_clause:
                messages_query = direction_clause

        order_clause = orders.get(order)
        messages_query = messages_query.order_by(order_clause)

        messages_query = messages_query.limit(items)

        count = messages_query.count()
        messages = messages_query.all()

        print messages_query

        return PaginatedMessagesEntity(messages, total, count, more)


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


class CheckMessageExists(BasePersistanceService):

    def input(self):
        return {
            'message_id': IntegerValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.instance_of(x, bool)

    def execute(self, args):
        message_id = args.get('message_id')
        message_query = self.session.query(Message).\
            filter(Message.id == message_id)

        return message_query.count() == 1


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


class GetSubjectMessages(PaginatedMessagesService):

    message_class = SubjectMessage

    def input(self):
        super_input = super(GetSubjectMessages, self).input()
        super_input.update({'subject_id': IntegerValidator({'required': True})})
        return super_input

    def execute(self, args):
        subject_id = args.pop('subject_id')
        args['filter_value'] = subject_id
        return super(GetSubjectMessages, self).execute(args)


class GetGroupMessages(PaginatedMessagesService):

    message_class = GroupMessage

    def input(self):
        super_input = super(GetGroupMessages, self).input()
        super_input.update({'group_id': IntegerValidator({'required': True})})
        return super_input

    def execute(self, args):
        group_id = args.pop('group_id')
        args['filter_value'] = group_id
        return super(GetGroupMessages, self).execute(args)


