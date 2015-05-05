import unittest
from api.tests import config as tests_config
from api.tests.base import TestUtil
from common import status


test_util = TestUtil()


class ListSubjectMessagesViewTest(unittest.TestCase):

    endpoint = '/user/subjects/{subject_id}/messages/'

    def test(self):

        subject_id = tests_config.USERS.get('student').get('subjects').get('enrolled')

        url = TestUtil.build_url(self.endpoint.format(subject_id=subject_id))
        response = test_util.session('student').get(url)

        parses_json = TestUtil.valid_json(response.text)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertTrue(parses_json)


class PostSubjectMessageViewTest(unittest.TestCase):

    endpoint = '/user/subjects/{subject_id}/messages/'

    def test_success(self):

        data = {
            'body': 'Lorem ipsum dolor sit amet'
        }

        subject_id = tests_config.USERS.get('student').get('subjects').get('enrolled')
        url = TestUtil.build_url(self.endpoint.format(subject_id=subject_id))
        response = test_util.session('student').post(url, data)

        parses_json = TestUtil.valid_json(response.text)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertTrue(parses_json)

        if parses_json:
            json = response.json()
            self.assertEqual(data.get('body'), json.get('body'))

    def test_validation(self):

        data = {
            'body': ''
        }

        subject_id = tests_config.USERS.get('student').get('subjects').get('enrolled')
        url = TestUtil.build_url(self.endpoint.format(subject_id=subject_id))
        response = test_util.session('student').post(url, data)

        parses_json = TestUtil.valid_json(response.text)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertTrue(parses_json)


class ListGroupMessagesViewTest(unittest.TestCase):

    endpoint = '/user/subjects/{subject_id}/groups/{group_id}/messages/'

    def test(self):

        subject_id, group_id = tests_config.USERS.get('student').get('groups').get('enrolled')

        url = TestUtil.build_url(self.endpoint.format(subject_id=subject_id, group_id=group_id))
        response = test_util.session('student').get(url)

        parses_json = TestUtil.valid_json(response.text)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertTrue(parses_json)


class PostGroupMessageViewTest(unittest.TestCase):

    endpoint = '/user/subjects/{subject_id}/groups/{group_id}/messages/'

    def test_success(self):

        data = {
            'body': 'Lorem ipsum dolor sit amet'
        }

        subject_id, group_id = tests_config.USERS.get('student').get('groups').get('enrolled')
        url = TestUtil.build_url(self.endpoint.format(subject_id=subject_id, group_id=group_id))
        response = test_util.session('student').post(url, data)

        parses_json = TestUtil.valid_json(response.text)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertTrue(parses_json)

        if parses_json:
            json = response.json()
            self.assertEqual(data.get('body'), json.get('body'))

    def test_validation(self):

        data = {
            'body': ''
        }

        subject_id, group_id = tests_config.USERS.get('student').get('groups').get('enrolled')
        url = TestUtil.build_url(self.endpoint.format(subject_id=subject_id, group_id=group_id))
        response = test_util.session('student').post(url, data)

        parses_json = TestUtil.valid_json(response.text)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertTrue(parses_json)


class ListDirectMessagesViewTest(unittest.TestCase):

    endpoint = '/user/chats/{peer_id}/messages/'

    def test(self):

        peer_id = tests_config.USERS.get('student').get('peers').get('teacher')

        url = TestUtil.build_url(self.endpoint.format(peer_id=peer_id))
        response = test_util.session('student').get(url)

        parses_json = TestUtil.valid_json(response.text)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertTrue(parses_json)


class PostDirectMessageViewTest(unittest.TestCase):

    endpoint = '/user/chats/{peer_id}/messages/'

    def test_success(self):

        data = {
            'body': 'Lorem ipsum dolor sit amet'
        }

        peer_id = tests_config.USERS.get('student').get('peers').get('teacher')

        url = TestUtil.build_url(self.endpoint.format(peer_id=peer_id))
        response = test_util.session('student').post(url, data)

        parses_json = TestUtil.valid_json(response.text)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertTrue(parses_json)

        if parses_json:
            json = response.json()
            self.assertEqual(data.get('body'), json.get('body'))

    def test_validation(self):

        data = {
            'body': ''
        }

        peer_id = tests_config.USERS.get('student').get('peers').get('teacher')

        url = TestUtil.build_url(self.endpoint.format(peer_id=peer_id))
        response = test_util.session('student').post(url, data)

        parses_json = TestUtil.valid_json(response.text)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertTrue(parses_json)


class SubjectMessageDetailViewTest(unittest.TestCase):

    endpoint = '/user/subjects/{subject_id}/messages/{message_id}/'

    def test_success(self):

        data = {
            'body': 'Lorem ipsum dolor sit amet'
        }

        subject_id = tests_config.USERS.get('student').get('subjects').get('enrolled')

        url = TestUtil.build_url(PostSubjectMessageViewTest.endpoint.format(subject_id=subject_id))
        response = test_util.session('student').post(url, data)

        parses_json = TestUtil.valid_json(response.text)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertTrue(parses_json)

        json = response.json()
        message_id = json.get('id')

        url = TestUtil.build_url(self.endpoint.format(subject_id=subject_id, message_id=message_id))
        response = test_util.session('student').get(url)

        parses_json = TestUtil.valid_json(response.text)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertTrue(parses_json)

    def test_not_found(self):

        subject_id = tests_config.USERS.get('student').get('subjects').get('enrolled')

        url = TestUtil.build_url(self.endpoint.format(subject_id=subject_id, message_id=0))
        response = test_util.session('student').get(url)

        parses_json = TestUtil.valid_json(response.text)

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertTrue(parses_json)


class GroupMessageDetailViewTest(unittest.TestCase):

    endpoint = '/user/subjects/{subject_id}/groups/{group_id}/messages/{message_id}/'

    def test_success(self):
        data = {
            'body': 'Lorem ipsum dolor sit amet'
        }

        subject_id, group_id = tests_config.USERS.get('student').get('groups').get('enrolled')
        url = TestUtil.build_url(PostGroupMessageViewTest.endpoint.format(subject_id=subject_id, group_id=group_id))
        response = test_util.session('student').post(url, data)

        parses_json = TestUtil.valid_json(response.text)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertTrue(parses_json)

        json = response.json()
        message_id = json.get('id')

        url = TestUtil.build_url(self.endpoint.format(subject_id=subject_id, group_id=group_id, message_id=message_id))
        response = test_util.session('student').get(url)

        parses_json = TestUtil.valid_json(response.text)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertTrue(parses_json)

    def test_not_found(self):

        subject_id, group_id = tests_config.USERS.get('student').get('groups').get('enrolled')
        url = TestUtil.build_url(self.endpoint.format(subject_id=subject_id, group_id=group_id, message_id=0))

        response = test_util.session('student').get(url)

        parses_json = TestUtil.valid_json(response.text)

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertTrue(parses_json)
