from api import app
from config import config

from api.lib.error_handlers import handlers
from api.routing import routing


def setup_config(application):
    application.config['JSON_SORT_KEYS'] = False
    application.config['SQLALCHEMY_DATABASE_URI'] = config.DB_DSN

    return application


def setup_logging(application):

    from logging.handlers import RotatingFileHandler
    import logging

    formatter = logging.Formatter('[%(asctime)s] [%(pathname)s:%(lineno)d] %(levelname)s - %(message)s')

    file_handler = RotatingFileHandler(config.LOG_FILE, maxBytes=10000000, backupCount=5)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    application.logger.addHandler(file_handler)

    return application


def setup_routing(application):

    def _add_routing(p, o):

        view_class = o.get('class')
        view_name = o.get('name')
        view_methods = o.get('methods')
        view_func = view_class.as_view(view_name)

        application.add_url_rule(p, view_func=view_func, methods=view_methods)

    for (pattern, options) in routing.iteritems():

        if isinstance(options, list):
            for option in options:
                _add_routing(pattern, option)
        else:
            _add_routing(pattern, options)

    return application


def setup_error_handlers(application):

    for (exceptions, handler) in handlers.iteritems():
        if isinstance(exceptions, tuple):
            for exception in exceptions:
                application.register_error_handler(exception, handler)
        else:
            application.register_error_handler(exceptions, handler)

    return application


def configure(application):

    application = setup_config(application)
    application = setup_logging(application)
    application = setup_routing(application)
    application = setup_error_handlers(application)

    return application


app = configure(app)
