import sys
import os

sys.path.insert(0, os.path.realpath('../../'))

print sys.path

import requests
import json
import urllib
from requests.packages import urllib3

from application.tests import config as tests_config


class TestUtil(object):

    endpoint = None

    def __init__(self):
        super(TestUtil, self).__init__()

        urllib3.disable_warnings()

        teacher_session = requests.Session()
        teacher_session.headers.update({
            'Authorization': tests_config.USERS.get('teacher').get('token')
        })

        teacher_session.verify = tests_config.CERT_FILE

        student_session = requests.Session()
        student_session.headers.update({
            'Authorization': tests_config.USERS.get('student').get('token')
        })

        student_session.verify = tests_config.CERT_FILE

        raw_session = requests.Session()
        raw_session.verify = tests_config.CERT_FILE

        self.sessions = {
            'teacher': teacher_session,
            'student': student_session,
            'raw': raw_session
        }

    def session(self, kind):
        return self.sessions.get(kind) or self.sessions.get('raw')

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
            query_string = TestUtil.build_querystring(params)
            base_url = '{base_url}?{query_string}'.format(base_url=base_url, query_string=query_string)

        return base_url

    @staticmethod
    def build_querystring(params):
        return urllib.urlencode(params)



