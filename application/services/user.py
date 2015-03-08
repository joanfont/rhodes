from application.services.base import BasePersistanceService
from application.lib.validators import IntegerValidator
from common.helper import Helper
from application.lib.models import User
from common.exceptions import UserNotFoundError


class GetUser(BasePersistanceService):

    def input(self):
        return {
            'id': IntegerValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.instance_of(x, User)

    def execute(self, args):
        _id = args.get('id')
        user = self.session.query(User).get(_id)

        if not user:
            raise UserNotFoundError()

        return user