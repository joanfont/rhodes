from datetime import datetime
from application.exceptions import MyValueError


class BaseValidator(object):

    def __init__(self, options):
        for (k, v) in options.items():
            if k not in self.defaults():
                error = 'The option {option} is not allowed in this validator'.format(option=k)
                raise KeyError(error)

        self.options = options
        self.errors = []

    def add_error(self, error):
        self.errors.append(error)

    def get_errors(self):
        return self.errors

    def defaults(self):
        return {'required': False, 'default': None}

    def validate(self, value):
        if self.options.get('required') and not value:
            self.add_error('The value is required')

        val = value if value is not None else self.options.get('default')
        self.check_value(val)

        if self.has_errors():
            errors = {'errors': self.get_errors()}
            raise MyValueError(payload=errors)

        return self.clean_value(val)

    def check_value(self, value):
        raise NotImplementedError()

    def clean_value(self, value):
        raise NotImplementedError()


class IntegerValidator(BaseValidator):

    def check_value(self, value):

        try:
            int(value)
        except ValueError:
            self.add_error('The value is not an integer')

    def clean_value(self, value):
        return int(value)


class StringValidator(BaseValidator):

    def defaults(self):
        _defaults = super(StringValidator, self).defaults()
        _defaults.update({'min_length': 0, 'max_length': 0})
        return _defaults

    def check_value(self, value):

        min_length = self.options.get('min_length')
        max_length = self.options.get('max_length')

        if not isinstance(value, (basestring, unicode, str)):
            self.add_error('The value is not an string')

        if min_length and len(value) < min_length:
            self.add_error('The value\'s length is lower than {min_length}'.format(min_length=min_length))

        if max_length and len(value) > max_length:
            self.add_error('The value\'s length is greater than {max_length}'.format(max_length=max_length))

    def clean_value(self, value):
        return unicode(value)


class ChoicesValidator(BaseValidator):

    def defaults(self):
        _defaults = super(ChoicesValidator, self).defaults()
        _defaults.update({'choices': []})
        return _defaults

    def check_value(self, value):

        choices = self.options.get('choices')

        if not isinstance(choices, (list, tuple)):
            self.add_eror('Choices option must be a list or a tuple')

        if value not in choices:
            self.add_error('The value is not in choices')

    def clean_value(self, value):
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

    @staticmethod
    def get_instance(value, frmat):
        return value if isinstance(value, datetime) else datetime.strptime(value, frmat)

    def check_value(self, value):

        frmat = self.options.get('format')

        dfrom = self.get_instance(self.options.get('from'), frmat) if self.options.get('from') else None
        dto = self.get_instance(self.options.get('to'), frmat) if self.options.get('to') else None
        date = self.get_instance(value, frmat)

        if dfrom and date > dfrom:
            self.add_error('Date must be more than \'from\' value provided')

        if dto and date < dto:
            self.add_error('Date must be less than \'to\' value provided')

    def clean_value(self, value):
        frmat = self.options.get('format')
        return self.get_instance(value, frmat)


class BooleanValidator(BaseValidator):

    def check_value(self, value):

        if not isinstance(value, bool):
            self.add_error('Value is not boolean')

    def clean_value(self, value):
        return bool(value)