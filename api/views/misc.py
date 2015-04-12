from api.lib.decorators import auth_token_required
from api.lib.mixins import ListAPIViewMixin, APIDict

from config import config


class ConfigView(ListAPIViewMixin):

    @auth_token_required
    def get_action(self, *args, **kwargs):

        config_dict = {
            'message_max_length': config.MESSAGE_MAX_LENGTH
        }

        return APIDict(config_dict)
