import unittest
from api.tests.base import TestUtil
from common import status


test_util = TestUtil()


class MessageNotificationsViewTest(unittest.TestCase):

    endpoint = '/user/notifications/'

    def test(self):

        url = TestUtil.build_url(self.endpoint)
        response = test_util.session('student').get(url)

        parses_json = TestUtil.valid_json(response.text)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertTrue(parses_json)


class SubjectNotificationsViewTest(unittest.TestCase):

    endpoint = '/user/notifications/subject/'

    def test(self):

        url = TestUtil.build_url(self.endpoint)
        response = test_util.session('student').get(url)

        parses_json = TestUtil.valid_json(response.text)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertTrue(parses_json)


class GroupNotificationsViewTest(unittest.TestCase):

    endpoint = '/user/notifications/group/'

    def test(self):

        url = TestUtil.build_url(self.endpoint)
        response = test_util.session('student').get(url)

        parses_json = TestUtil.valid_json(response.text)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertTrue(parses_json)


class ChatNotificationsViewTest(unittest.TestCase):

    endpoint = '/user/notifications/chat/'

    def test(self):

        url = TestUtil.build_url(self.endpoint)
        response = test_util.session('student').get(url)

        parses_json = TestUtil.valid_json(response.text)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertTrue(parses_json)