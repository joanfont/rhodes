from application.services.base import BaseService
from lib.validators import StringValidator

from application.lib.models import SessionWrapper
from application.lib.models import Message

class PutMessage(BaseService):

  def input(self):
    return {
      'message': StringValidator({'required': True}),
    }

  def execute(self, args):

    message = args.get('message')
    msg = Message(message = message)

    session = SessionWrapper.get_session()
    session.add(msg)
    session.commit()

    return msg



