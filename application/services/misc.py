from base import BaseService
from lib.validators import IntegerValidator

import math

class Pow(BaseService):

  def input(self):
    return {
      'base': IntegerValidator({'required': True}),
      'exponent': IntegerValidator({'required': False, 'default': 2}),
    }

  def execute(self, args):
    base = args.get('base')
    exponent = args.get('exponent')
    return math.pow(base, exponent)