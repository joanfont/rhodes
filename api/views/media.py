from api.lib.decorators import validate, auth_token_required, media_exists, user_can_see_media
from api.lib.mixins import MediaResponseMixin, ListAPIViewMixin
from application.lib.validators import IntegerValidator


class MediaView(ListAPIViewMixin, MediaResponseMixin):

    def params(self):
        return {
            'media_id': [self.PARAM_URL, IntegerValidator({'required': True})]
        }

    @validate
    @auth_token_required
    @media_exists
    @user_can_see_media
    def get_action(self, *args, **kwargs):
        media = kwargs.get('media')
        return media
