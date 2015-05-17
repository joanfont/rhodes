from api.exceptions import ObjectNotFoundError, ForbiddenActionError
from config import config

class MediaNotFoundError(ObjectNotFoundError):

    message = 'Media not found'



class UserCanNotSeeMediaError(ForbiddenActionError):

    message = 'User can not see media'


class LimitOfMessageFilesReachedError(ForbiddenActionError):

    message = 'Limit of {num_files} files has been reached'.format(num_files=config.MAX_MESSAGE_FILES)


class CantAttachMediaToMessageError(ForbiddenActionError):

    message = 'Can\'t attach media to this message'

