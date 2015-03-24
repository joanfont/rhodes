from flask import Flask
from api.app import app as api
from web.app import app as web

from threading import Lock
from werkzeug.wsgi import pop_path_info, peek_path_info


class Dispatcher(object):

    def __init__(self, api_app, web_app):
        self.api = api_app
        self.web = web_app
        self.lock = Lock()
        self.instances = {}

    def create_app(self, prefix, environ):
        if prefix.startswith('docs'):
            pop_path_info(environ)
            app_cls = self.web
        else:
            app_cls = self.api

        return app_cls

    def get_application(self, environ):
        prefix = peek_path_info(environ)
        with self.lock:
            app_cls = self.instances.get(prefix)
            if not app_cls:
                app_cls = self.create_app(prefix, environ)
            return app_cls

    def __call__(self, environ, start_response):
        app_instance = self.get_application(environ)

        return app_instance(environ, start_response)

app = api

if __name__ == '__main__':
    app.run(debug=True, port=8080)