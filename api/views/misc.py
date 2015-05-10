from api.lib.decorators import auth_token_required
from api.lib.mixins import ListAPIViewMixin
from application.lib.models import UserType

from config import config


class ConfigView(ListAPIViewMixin):

    @auth_token_required
    def get_action(self, *args, **kwargs):
        return {
            'message_max_length': config.MESSAGE_MAX_LENGTH,
            'user_types': {
                UserType.TEACHER: 'Teacher',
                UserType.STUDENT: 'Student'
            },
        }

