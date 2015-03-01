from application.services.base import BasePersistanceService
from application.lib.validators import StringValidator

from application.lib.models import Message

class PutMessage(BasePersistanceService):

  def input(self):
    return {
      'message': StringValidator({'required': True}),
    }

  def output(self):
    return lambda x: isinstance(x, Message)

  def execute(self, args):
    message = args.get('message')
    msg = Message(message = message)
    self.session.add(msg)
    return msg




