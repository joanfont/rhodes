import unittest
import requests
import json
import urllib

from application.tests import config as tests_config


class BaseTest(unittest.TestCase):

    status_code = 200
    endpoint = None

    OFF = "\033[0;0m"
    GREEN = "\033[92m"
    RED = "\033[91m"

    def __init__(self, method_name='runTest'):
        super(BaseTest, self).__init__(method_name)

        session = requests.Session()
        session.headers.update({
            'Authorization': tests_config.TOKEN
        })

        self.session = session

    def ok(self):
        print '{color}OK{off}'.format(color=self.GREEN, off=self.OFF)

    def error(self):
        print '{color}ERROR{off}'.format(color=self.RED, off=self.OFF)

    @staticmethod
    def valid_json(text):
        try:
            json.loads(text)
            return True
        except Exception, e:
            return False

    @staticmethod
    def build_url(endpoint, params={}):
        base_url = '{host}{endpoint}'.format(host=tests_config.SERVER_URL, endpoint=endpoint)
        if params:
            query_string = BaseTest.build_querystring(params)
            base_url = '{base_url}?{query_string}'.format(base_url=base_url, query_string=query_string)

        return base_url

    @staticmethod
    def build_querystring(params):
        return urllib.urlencode(params)



