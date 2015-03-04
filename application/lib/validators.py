
VALIDATION_ERROR = 'validation_error'


class ValidationError(Exception):

    def __init__(self, *args, **kwargs):
        super(ValidationError, self).__init__(*args)
        self.errors = kwargs.get('errors')

    def get_errors(self):
        return self.errors


class BaseValidator(object):
    def __init__(self, options):
        for (k, v) in options.items():
            if k not in self.defaults():
                error = 'The option {option} is not allowed in this validator'.format(option=k)
                raise KeyError(error)

        self.options = options

    def defaults(self):
        return {'required': False, 'default': None}

    def validate(self, value):
        if self.options.get('required') and not value:
            raise ValidationError('The value is required for this validator')

        val = value if value != None else self.options.get('default')
        return self.check_value(val)

    def check_value(self, value):
        raise NotImplementedError()


class IntegerValidator(BaseValidator):
    def check_value(self, value):
        try:
            value = int(value)
        except ValueError:
            raise ValidationError('The value is not an integer')

        return value


class StringValidator(BaseValidator):
    def defaults(self):
        _defaults = super(StringValidator, self).defaults()
        _defaults.update({'min_length': 0, 'max_length': 0})
        return _defaults

    def check_value(self, value):
        if not isinstance(value, (basestring, unicode)):
            raise ValidationError('The value is not an string')

        if self.options.get('min_length') and len(value) < self.options.get('min_length'):
            raise ValidationError('The value\'s length is lower than the min_length provided')

        if self.options.get('max_length') and len(value) > self.options.get('max_length'):
            raise ValidationError('The value\'s length is greater than the min_length provided')

        return value



