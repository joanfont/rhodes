import math

from base import BaseService
from application.lib.validators import IntegerValidator


class Pow(BaseService):
    def input(self):
        return {
            'base': IntegerValidator({'required': True}),
            'exponent': IntegerValidator({'required': False, 'default': 2}),
        }

    def output(self):
        return lambda x: isinstance(x, int)

    def execute(self, args):
        base = args.get('base')
        exponent = args.get('exponent')
        return math.pow(base, exponent)