
class Helper(object):

    @staticmethod
    def array_of(array, cls):
        return all(isinstance(x, cls) for x in array)