import common.status as status


# Base exception
class BaseError(Exception):
    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    CODE = 'generic_error'
    MESSAGE = 'Generic error'

    def __init__(self, *args, **kwargs):
        super(BaseError, self).__init__(*args)
        self.status_code = kwargs.get('status_code', self.STATUS_CODE)
        if kwargs.get('error'):
            self.error = kwargs.get('error')
        else:
            message = kwargs.get('error_message', self.MESSAGE)
            self.error = {'code': self.CODE, 'message': message}


