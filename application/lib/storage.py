from io import BytesIO
import os


class DiskStorage(object):

    @staticmethod
    def save_bytes(byte_data, path):
        with open(path, 'wb+') as f:
            f.write(byte_data.read())

    @staticmethod
    def get_bytes(path):
        byte_data = None
        try:
            with open(path, 'rb') as f:
                byte_data = BytesIO(f.read())
        except IOError:
            pass

        return byte_data

    @staticmethod
    def remove(path):
        if os.path.exists(path):
            os.remove(path)


    @staticmethod
    def ensure_path(path):





