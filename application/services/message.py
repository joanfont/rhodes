from application.services.base import BasePersistanceService
from application.lib.validators import StringValidator, IntegerValidator

from application.lib.models import Message


class MessageNotFoundError(Exception):
    pass


class PutMessage(BasePersistanceService):
    def input(self):
        return {
            'message': StringValidator({'required': True}),
        }

    def output(self):
        return lambda x: isinstance(x, Message)

    def execute(self, args):
        message = args.get('message')
        msg = Message(message=message)
        self.session.add(msg)
        return msg


class GetMessage(BasePersistanceService):
    def input(self):
        return {
            'id': IntegerValidator({'required': True})
        }

    def output(self):
        return lambda x: isinstance(x, Message)

    def execute(self, args):
        _id = args.get('id')
        message = self.session.query(Message).get(_id)
        if not message:
            raise MessageNotFoundError()
        return message




