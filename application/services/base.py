from lib.validators import BaseValidator

class BaseService(object):

  def __init__(self):
    self.input_contract = {}
    self.output_contract = {}


  def input(self):
    raise NotImplementedError()

  def output(self):
    raise NotImplementedError()

  def check_input(self):
    input_contract = self.input()

    if not input_contract:
      raise RuntimeError('You must provide an input contract')

    for (k,v) in input_contract.items():
      if not isinstance(v, BaseValidator):
        error = 'The validator {validator} must be an instance of BaseValidator'.format(validator = k)
        raise ValueError(error)

    self.input_contract = input_contract

  def check_args(self, args):
    cleaned_args = {}
    for (k,v) in self.input_contract.items():
      value = args.get(k)
      cleaned_args[k] = v.validate(value)

    return cleaned_args

  def call(self, args):
    self.check_input()
    cleaned_args = self.check_args(args)
    result = self.execute(cleaned_args)

    return result


  def execute(self, args):
    raise NotImplementedError()