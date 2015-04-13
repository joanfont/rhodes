from application.lib.models import Message, MessageType, DirectMessage, SubjectMessage, GroupMessage, MessageBody
from application.lib.validators import StringValidator, IntegerValidator, ChoicesValidator, DateValidator
from application.services.base import BasePersistanceService, BaseService
from application.lib.entities import PaginatedEntity
from common.helper import Helper
from common import constants
from config import config

ORDER_CHOICES = ['asc', 'desc']


class PaginatedMessages(BasePersistanceService):
    def input(self):
        return {
            'items': IntegerValidator({'required': False, 'default': config.ITEMS_PER_PAGE}),
            'last_message_id': IntegerValidator({'required': False}),
            'order': ChoicesValidator({
                'required': False,
                'choices': constants.MESSAGES_PAGINATION_CHOICES,
                'default': constants.MESSAGES_PAGINATION_NEXT})
        }

    def output(self):
        def _output(x):
            return Helper.array_of(x, Message)

        return _output

    def execute(self, args):
        raise NotImplementedError


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


class GetSubjectMessages(PaginatedMessages):

    def input(self):
        _input = super(GetSubjectMessages, self).input()
        _input.update({'subject_id': IntegerValidator({'required': True})})
        return _input

    def execute(self, args):

        subject_id = args.get('subject_id')

        items = args.get('items')
        last_message_id = args.get('last_message_id')
        order = args.get('order')

        messages_query = self.session.query(SubjectMessage). \
            filter(SubjectMessage.subject_id == subject_id)

        if last_message_id:

            if order == constants.MESSAGES_PAGINATION_NEXT:
                messages_query = messages_query.filter(SubjectMessage.id > last_message_id)
            elif order == constants.MESSAGES_PAGINATION_PREVIOUS:
                messages_query = messages_query.filter(SubjectMessage.id < last_message_id)

        messages_query = messages_query.order_by(SubjectMessage.created_at.desc()). \
            limit(items)

        messages = messages_query.all()

        # n_messages = messages_query.count()
        # paginated_messages = PaginatedEntity(messages, n_messages, last_message_id, order)
        return messages


class GetGroupMessages(PaginatedMessages):

    def input(self):
        _input = super(GetGroupMessages, self).input()
        _input.update({'group_id': IntegerValidator({'required': True})})
        return _input

    def execute(self, args):
        group_id = args.get('group_id')

        items = args.get('items')
        last_message_id = args.get('last_message_id')
        order = args.get('order')

        print args

        messages_query = self.session.query(GroupMessage). \
            filter(GroupMessage.group_id == group_id)

        if last_message_id:

            if order == constants.MESSAGES_PAGINATION_NEXT:
                messages_query = messages_query.filter(GroupMessage.id > last_message_id)
            elif order == constants.MESSAGES_PAGINATION_PREVIOUS:
                messages_query = messages_query.filter(GroupMessage.id < last_message_id)

        messages_query = messages_query.order_by(GroupMessage.created_at.desc()). \
            limit(items)

        messages = messages_query.all()

        # n_messages = messages_query.count()
        # paginated_messages = PaginatedEntity(messages, n_messages, last_message_id, order)
        return messages


