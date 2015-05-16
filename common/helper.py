import base64
import hashlib
from config import config


class Helper(object):

    @staticmethod
    def instance_of(obj, cls):
        return isinstance(obj, cls)

    @staticmethod
    def array_of(array, cls):
        return all(isinstance(x, cls) for x in array)

    @staticmethod
    def datetime_format(dt, fmt=None):
        if not fmt:
            fmt = config.DATETIME_FORMAT

        return dt.strftime(fmt)

    @staticmethod
    def md5(text):
        m = hashlib.md5()
        m.update(text)
        return m.hexdigest()

    @staticmethod
    def b64_encode(data):
        return base64.b64encode(data)

    @staticmethod
    def b64_decode(data):
        return base64.b64decode(data)