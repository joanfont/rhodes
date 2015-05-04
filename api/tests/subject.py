import unittest
from api.tests import config as tests_config
from api.tests.base import TestUtil
from common import status


test_util = TestUtil()


class SubjectsViewTest(unittest.TestCase):

    endpoint = '/user/subjects/'

    def test(self):
        url = TestUtil.build_url(self.endpoint)
        response = test_util.session('student').get(url)

        parses_json = TestUtil.valid_json(response.text)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertTrue(parses_json)


class SubjectDetailViewTest(unittest.TestCase):

    endpoint = '/user/subjects/{subject_id}/'

    def test_success(self):
        subject_id = tests_config.USERS.get('student').get('subjects').get('enrolled')
        url = TestUtil.build_url(self.endpoint.format(subject_id=subject_id))
        response = test_util.session('student').get(url)

        parses_json = TestUtil.valid_json(response.text)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertTrue(parses_json)

    def test_not_enrolled(self):

        subject_id = tests_config.USERS.get('student').get('subjects').get('not_enrolled')
        url = TestUtil.build_url(self.endpoint.format(subject_id=subject_id))
        response = test_util.session('student').get(url)

        parses_json = TestUtil.valid_json(response.text)

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertTrue(parses_json)