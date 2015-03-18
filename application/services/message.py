from application.lib.models import Message, MessageType, DirectMessage, SubjectMessage, GroupMessage
from application.lib.validators import StringValidator, IntegerValidator, ChoicesValidator, DateValidator
from application.services.base import BasePersistanceService, BaseService
from common.helper import Helper


class PutMessage(BasePersistanceService):

    def input(self):
        return {
            'sender_id': IntegerValidator({'required': True}),
            'body': StringValidator({'required': True, 'max_length': Message.MAX_LENGTH}),
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

        message_cls = self.get_message_instance(message_type)

        self.adapt_args(args)
        message = message_cls(**args)

        self.session.add(message)
        return message


class PutMessageInputAndOutputContractMixin(BaseService):

    def input(self):
        return {
            'sender_id': IntegerValidator({'required': True}),
            'body': StringValidator({'required': True, 'max_length': Message.MAX_LENGTH}),
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
            'subject_id': IntegerValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.array_of(x, SubjectMessage)

    def execute(self, args):
        subject_id = args.get('subject_id')

        messages = self.session.query(SubjectMessage).\
            filter(SubjectMessage.subject_id == subject_id).\
            order_by(SubjectMessage.created_at.desc()).all()
        return messages


class GetGroupMessages(BasePersistanceService):

    def input(self):
        return {
            'group_id': IntegerValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.array_of(x, GroupMessage)

    def execute(self, args):
        group_id = args.get('group_id')
        messages = self.session.query(GroupMessage).\
            filter(GroupMessage.group_id == group_id).all()
        return messages