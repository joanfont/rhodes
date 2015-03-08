
class Helper(object):

    @staticmethod
    def instance_of(obj, cls):
        return isinstance(obj, cls)

    @staticmethod
    def array_of(array, cls):
        return all(isinstance(x, cls) for x in array)