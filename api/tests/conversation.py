import unittest
from api.tests import config as tests_config
from api.tests.base import TestUtil
from common import status


test_util = TestUtil()


class ListConversationsViewTest(unittest.TestCase):

    endpoint = '/user/chats/'

    def test(self):

        url = TestUtil.build_url(self.endpoint)
        response = test_util.session('student').get(url)

        parses_json = TestUtil.valid_json(response.text)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertTrue(parses_json)


class ConversationDetailViewTest(unittest.TestCase):

    endpoint = '/user/chats/{peer_id}/'

    def test(self):
        peer_id = tests_config.USERS.get('student').get('peers').get('teacher')
        url = TestUtil.build_url(self.endpoint.format(peer_id=peer_id))
        response = test_util.session('student').get(url)

        parses_json = TestUtil.valid_json(response.text)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertTrue(parses_json)