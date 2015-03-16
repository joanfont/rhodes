from config import rhodes as config


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