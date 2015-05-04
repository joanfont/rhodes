import os


class Environment(object):

    @staticmethod
    def get(key, default=None):
        return os.environ.get(key, default)


