from io import BytesIO
from application.lib.models import Media, MediaType, ProfilePictureMedia, MessageFileMedia
from application.lib.validators import ChoicesValidator, IntegerValidator, BytesIOValidator, ClassValidator
from application.services.base import BasePersistanceService, BaseService
from application.lib.storage import DiskStorage
from common.helper import Helper
from config import config


class GetMediaBytes(BaseService):

    def input(self):
        return {
            'media': ClassValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.instance_of(x, BytesIO) or x is None

    def execute(self, args):

        media = args.get('media')

        byte_data = DiskStorage.get_bytes(media.get_path())

        return byte_data

class GetUserProfilePictureMedia(BasePersistanceService):

    def input(self):
        return {
            'user_id': IntegerValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.instance_of(x, ProfilePictureMedia) or x is None

    def execute(self, args):

        user_id = args.get('user_id')

        media_query = self.session.query(ProfilePictureMedia).\
            filter(ProfilePictureMedia.user_id == user_id)

        if media_query.count():
            media = media_query.all()[0]
        else:
            media = None

        return media


class AttachMedia(BasePersistanceService):

    def input(self):
        return {
            'bytes': BytesIOValidator({'required': True}),
            'mime': ChoicesValidator({'required': True, 'choices': config.ALLOWED_MIME_TYPES}),
            'type': ChoicesValidator({'required': True, 'choices': MediaType.CHOICES}),
            'entity_id': IntegerValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.instance_of(x, Media) or x is None

    @staticmethod
    def get_media_class(media_type):
        dispatcher = {
            MediaType.PROFILE_PICTURE: ProfilePictureMedia,
            MediaType.MESSAGE_FILE: MessageFileMedia
        }

        return dispatcher.get(media_type)

    @staticmethod
    def adapt_args(args):

        media_type = args.get('type')
        entity_id = args.get('entity_id')

        dispatcher = {
            MediaType.PROFILE_PICTURE: 'user_id',
            MediaType.MESSAGE_FILE: 'message_id'
        }
        new_key = dispatcher.get(media_type)
        args[new_key] = entity_id
        args.pop('entity_id')
        args.pop('bytes')

    def execute(self, args):
        media_type = args.get('type')
        byte_data = args.get('bytes')

        media_class = self.get_media_class(media_type)
        self.adapt_args(args)

        media = media_class(**args)

        path = media.get_path()
        media.path = media.get_file_name()

        DiskStorage.save_bytes(byte_data, path)

        self.session.add(media)
        self.session.commit()

        return media


class AttachAvatar(BasePersistanceService):

    def input(self):
        return {
            'bytes': BytesIOValidator({'required': True}),
            'mime': ChoicesValidator({'required': True, 'choices': config.ALLOWED_MIME_TYPES}),
            'user_id': IntegerValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.instance_of(x, Media) or x is None

    def execute(self, args):
        user_id = args.pop('user_id')

        get_user_media_srv = GetUserProfilePictureMedia()
        user_media = get_user_media_srv.call({
            'user_id': user_id
        })

        if user_media:
            DiskStorage.remove(user_media.get_path())
            self.session.delete(user_media)
            self.session.commit()

        args.update({
            'type': MediaType.PROFILE_PICTURE,
            'entity_id': user_id})

        attach_media_srv = AttachMedia()
        media = attach_media_srv.call(args)

        return media