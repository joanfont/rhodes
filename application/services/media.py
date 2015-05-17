from io import BytesIO
from application.lib.models import Media, MediaType, AvatarMedia, MessageFileMedia
from application.lib.validators import ChoicesValidator, IntegerValidator, BytesIOValidator, ClassValidator
from application.services.base import BasePersistanceService, BaseService
from application.lib.storage import DiskStorage
from common.helper import Helper
from config import config
from datetime import datetime


class GetMediaBytes(BaseService):

    def input(self):
        return {
            'media': ClassValidator({'required': True, 'class': Media})
        }

    def output(self):
        return lambda x: Helper.instance_of(x, BytesIO) or x is None

    def execute(self, args):

        media = args.get('media')

        byte_data = DiskStorage.get_bytes(media.get_path())

        return byte_data


class GetMedia(BasePersistanceService):

    def input(self):
        return {
            'id': IntegerValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.instance_of(x, Media) or x is None

    def execute(self, args):

        media_id = args.get('id')

        media_query = self.session.query(Media).\
            filter(Media.id == media_id)

        if media_query.count():
            media = media_query.all()[0]
        else:
            media = None

        return media



class GetUserProfilePictureMedia(BasePersistanceService):

    def input(self):
        return {
            'user_id': IntegerValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.instance_of(x, AvatarMedia) or x is None

    def execute(self, args):

        user_id = args.get('user_id')

        media_query = self.session.query(AvatarMedia).\
            filter(AvatarMedia.user_id == user_id)

        if media_query.count():
            media = media_query.all()[0]
        else:
            media = None

        return media


class GetMessageFileMedia(BasePersistanceService):

    def input(self):
        return {
            'message_id': IntegerValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.array_of(x, MessageFileMedia)

    def execute(self, args):

        message_id = args.get('message_id')

        media_query = self.session.query(MessageFileMedia).\
            filter(MessageFileMedia.message_id == message_id)

        return media_query.all()


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
            MediaType.AVATAR: AvatarMedia,
            MediaType.MESSAGE_FILE: MessageFileMedia
        }

        return dispatcher.get(media_type)

    @staticmethod
    def adapt_args(args):

        media_type = args.get('type')
        entity_id = args.get('entity_id')

        dispatcher = {
            MediaType.AVATAR: 'user_id',
            MediaType.MESSAGE_FILE: 'message_id'
        }
        new_key = dispatcher.get(media_type)
        args[new_key] = entity_id
        args.pop('entity_id')
        args.pop('bytes')

        now = datetime.now()
        args['created_at'] = now

    def execute(self, args):
        media_type = args.get('type')
        byte_data = args.get('bytes')

        media_class = self.get_media_class(media_type)
        self.adapt_args(args)

        media = media_class(**args)
        media.path = media.get_file_name()

        self.session.add(media)
        self.session.commit()

        directory = media.get_directory()
        path = media.get_path()

        DiskStorage.ensure_path(directory)
        DiskStorage.save_bytes(byte_data, path)

        return media


class AttachAvatar(BasePersistanceService):

    def input(self):
        return {
            'bytes': BytesIOValidator({'required': True}),
            'mime': ChoicesValidator({'required': True, 'choices': config.ALLOWED_MIME_TYPES}),
            'user_id': IntegerValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.instance_of(x, AvatarMedia) or x is None

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
            'type': MediaType.AVATAR,
            'entity_id': user_id})

        attach_media_srv = AttachMedia()
        media = attach_media_srv.call(args)

        return media


class AttachMessageFile(BasePersistanceService):

    def input(self):
        return {
            'bytes': BytesIOValidator({'required': True}),
            'mime': ChoicesValidator({'required': True, 'choices': config.ALLOWED_MIME_TYPES}),
            'message_id': IntegerValidator({'required': True})
        }

    def output(self):
        return lambda x: Helper.instance_of(x, MessageFileMedia) or x is None

    def execute(self, args):

        message_id = args.pop('message_id')

        args.update({
            'type': MediaType.MESSAGE_FILE,
            'entity_id': message_id
        })

        attach_media_srv = AttachMedia()
        media = attach_media_srv.call(args)

        return media