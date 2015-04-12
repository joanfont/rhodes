from application.lib.validators import BaseValidator
from application.lib.models import SessionWrapper
from application.exceptions import ValidationError, MyValueError


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
        validation_errors = []

        for (k, v) in self.input_contract.items():
            value = args.get(k)

            try:
                cleaned_args[k] = v.validate(value)
            except MyValueError, e:
                validation_error = {
                    'field': k,
                    'errors': e.get_errors()}

                validation_errors.append(validation_error)

        if validation_errors:
            payload = {'errors': validation_errors}
            e = ValidationError(payload=payload)
            raise e
        return cleaned_args

    def pre_execute(self, args):
        self.check_input()
        cleaned_args = self.clean_args(args)

        output_fnx = self.output()
        if not callable(output_fnx):
            raise RuntimeError('You must provide a callable output contract')

        return cleaned_args, output_fnx

    @staticmethod
    def post_execute(valid):
        if not valid:
            raise ValueError('The service\'s result does not satisfy the output contract given')

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

    def input(self):
        raise NotImplementedError()

    def output(self):
        raise NotImplementedError()

    def execute(self, args):
        raise NotImplementedError()

