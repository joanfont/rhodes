from application.services.base import BasePersistanceService
from application.lib.validators import IntegerValidator
from common.helper import Helper
from application.lib.models import User
from common.exceptions import UserNotFoundError


class GetUser(BasePersistanceService):

    def input(self):
        return {
            'user_id': IntegerValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.instance_of(x, User)

    def execute(self, args):
        user_id = args.get('user_id')
        user = self.session.query(User).get(user_id)

        if not user:
            raise UserNotFoundError()

        return user