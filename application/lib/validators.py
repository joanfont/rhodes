from datetime import datetime

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
            raise ValueError('The value is required for this validator')

        val = value if value is not None else self.options.get('default')
        return self.check_value(val)

    def check_value(self, value):
        raise NotImplementedError()


class IntegerValidator(BaseValidator):

    def check_value(self, value):
        try:
            value = int(value)
        except ValueError:
            raise ValueError('The value is not an integer')

        return value


class StringValidator(BaseValidator):

    def defaults(self):
        _defaults = super(StringValidator, self).defaults()
        _defaults.update({'min_length': 0, 'max_length': 0})
        return _defaults

    def check_value(self, value):
        if not isinstance(value, (basestring, unicode)):
            raise ValueError('The value is not an string')

        if self.options.get('min_length') and len(value) < self.options.get('min_length'):
            raise ValueError('The value\'s length is lower than the min_length provided')

        if self.options.get('max_length') and len(value) > self.options.get('max_length'):
            raise ValueError('The value\'s length is greater than the min_length provided')

        return value


class ChoicesValidator(BaseValidator):

    def defaults(self):
        _defaults = super(ChoicesValidator, self).defaults()
        _defaults.update({'choices': []})
        return _defaults

    def check_value(self, value):

        choices = self.options.get('choices')

        if not isinstance(choices, (list, tuple)):
            raise ValueError('Choices option must be a list or a tuple')

        if value not in choices:
            raise ValueError('The value is not in choices')

        return value


class DateValidator(BaseValidator):

    def defaults(self):
        _defaults = super(DateValidator, self).defaults()
        _defaults.update({
            'from': None,
            'to': None,
            'format': 'Y-m-d H:i:s'
        })
        return _defaults

    def check_value(self, value):

        def _get_instance(v, f):
            return v if isinstance(v, datetime) else datetime.strptime(v, f)

        fmt = self.options.get('format')

        dfrom = _get_instance(self.options.get('from'), fmt) if self.options.get('from') else None
        dto = _get_instance(self.options.get('to'), fmt) if self.options.get('to') else None
        date = _get_instance(value, fmt)

        if dfrom and date > dfrom:
            raise ValueError('Date must be more than \'from\' value provided')

        if dto and date < dto:
            raise ValueError('Date must be less than \'to\' value provided')

        return date



