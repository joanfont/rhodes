from api.lib.decorators import auth_token_required
from api.lib.mixins import ListAPIViewMixin
from application.lib.models import UserType

from config import config


class ConfigView(ListAPIViewMixin):

    @auth_token_required
    def get_action(self, *args, **kwargs):
        return {
            'message_max_length': config.MESSAGE_MAX_LENGTH,
            'max_file_size': config.MAX_FILE_SIZE,
            'allowed_mime_types': config.ALLOWED_MIME_TYPES,
            'max_message_files': config.MAX_MESSAGE_FILES,
            'user_types': {
                UserType.TEACHER: 'Teacher',
                UserType.STUDENT: 'Student'
            },

        }

