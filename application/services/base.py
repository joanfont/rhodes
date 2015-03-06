from application.lib.validators import BaseValidator
from application.lib.models import SessionWrapper

from application.lib.validators import ValidationError, VALIDATION_ERROR

class BaseService(object):
    def __init__(self):
        self.input_contract = {}

    def input(self):
        raise NotImplementedError()

    def output(self):
        raise NotImplementedError()

    def check_input(self):
        input_contract = self.input()

        if not isinstance(input_contract, dict):
            raise RuntimeError('You must provide an input contract')

        for (k, v) in input_contract.items():
            if not isinstance(v, BaseValidator):
                error = 'The validator {validator} must be an instance of BaseValidator'.format(validator=k)
                raise ValueError(error)

        self.input_contract = input_contract

    def clean_args(self, args):
        cleaned_args = {}
        arg_errors = {}
        for (k, v) in self.input_contract.items():
            value = args.get(k)
            try:
                clean_value = v.validate(value)
                cleaned_args[k] = clean_value
            except ValidationError, e:
                arg_errors[k] = {'error': VALIDATION_ERROR, 'message': e.message}

        if arg_errors:
            raise ValidationError('Validation error', errors=arg_errors)
        return cleaned_args

    def pre_execute(self, args):
        self.check_input()
        cleaned_args = self.clean_args(args)

        output_fnx = self.output()
        if not callable(output_fnx):
            raise RuntimeError('You must provide a callable output contract')

        return cleaned_args, output_fnx

    def post_execute(self, valid):
        if not valid:
            raise ValueError('The service\'s result does not sattisfy the output contract given')

    def call(self, args):
        cleaned_args, output_fnx = self.pre_execute(args)

        result = self.execute(args)
        output_valid = output_fnx(result)

        self.post_execute(output_valid)

        return result

    def execute(self, args):
        raise NotImplementedError()


class BasePersistanceService(BaseService):

    def __init__(self):
        super(BasePersistanceService, self).__init__()
        self.session = SessionWrapper()

    def post_execute(self, valid):
        if valid:
            self.session.commit()
        else:
            super(BasePersistanceService, self).post_execute(valid)

