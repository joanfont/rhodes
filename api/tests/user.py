import unittest

from api.tests.base import TestUtil
from api.tests import config as tests_config
from common import status


test_util = TestUtil()


class ProfileViewTest(unittest.TestCase):

    endpoint = '/user/'

    def test(self):
        url = TestUtil.build_url(self.endpoint)
        response = test_util.session('student').get(url)

        parses_json = TestUtil.valid_json(response.text)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertTrue(parses_json)


class LoginViewTest(unittest.TestCase):

    endpoint = '/login/'

    def test_success(self):
        params = {
            'user': tests_config.USERS.get('student').get('user'),
            'password': tests_config.USERS.get('student').get('password')}

        url = TestUtil.build_url(self.endpoint, params)
        response = test_util.session(None).get(url)
        parses_json = TestUtil.valid_json(response.text)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertTrue(parses_json)

        if parses_json:
            data = response.json()
            token = data.get('token')
            self.assertEqual(tests_config.USERS.get('student').get('token'), token)

    def test_failure(self):
        params = {'user': 'JFR143', 'password': 'asdfg'}
        url = TestUtil.build_url(self.endpoint, params)
        response = test_util.session(None).get(url)
        parses_json = TestUtil.valid_json(response.text)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertTrue(parses_json)

    def test_bad_request(self):
        params = {'user': 'JFR165'}
        url = TestUtil.build_url(self.endpoint, params)
        response = test_util.session(None).get(url)
        parses_json = TestUtil.valid_json(response.text)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertTrue(parses_json)


class SubjectTeachersViewTest(unittest.TestCase):

    endpoint = '/user/subjects/{subject_id}/teachers/'

    def test_success(self):

        student = tests_config.USERS.get('student')
        subject_id = student.get('subjects').get('enrolled')

        url = TestUtil.build_url(self.endpoint.format(subject_id=subject_id))

        response = test_util.session('student').get(url)
        parses_json = TestUtil.valid_json(response.text)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertTrue(parses_json)

    def test_user_not_enrolled(self):
        student = tests_config.USERS.get('student')
        subject_id = student.get('subjects').get('not_enrolled')

        url = TestUtil.build_url(self.endpoint.format(subject_id=subject_id))

        response = test_util.session('student').get(url)
        parses_json = TestUtil.valid_json(response.text)

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertTrue(parses_json)


class SubjectStudentsViewTest(unittest.TestCase):

    endpoint = '/user/subjects/{subject_id}/students/'

    def test_success(self):

        teacher = tests_config.USERS.get('teacher')
        subject_id = teacher.get('subjects').get('enrolled')

        url = TestUtil.build_url(self.endpoint.format(subject_id=subject_id))

        response = test_util.session('teacher').get(url)
        parses_json = TestUtil.valid_json(response.text)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertTrue(parses_json)

    def test_student(self):

        student = tests_config.USERS.get('student')
        subject_id = student.get('subjects').get('enrolled')

        url = TestUtil.build_url(self.endpoint.format(subject_id=subject_id))

        response = test_util.session('student').get(url)
        parses_json = TestUtil.valid_json(response.text)

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertTrue(parses_json)

    def test_user_not_enrolled(self):

        teacher = tests_config.USERS.get('teacher')
        subject_id = teacher.get('subjects').get('not_enrolled')

        url = TestUtil.build_url(self.endpoint.format(subject_id=subject_id))

        response = test_util.session('teacher').get(url)
        parses_json = TestUtil.valid_json(response.text)

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertTrue(parses_json)


class GroupStudentsViewTest(unittest.TestCase):

    endpoint = '/user/subjects/{subject_id}/groups/{group_id}/students/'

    def test_success(self):

        teacher = tests_config.USERS.get('teacher')
        subject_id, group_id = teacher.get('groups').get('enrolled')

        url = TestUtil.build_url(self.endpoint.format(subject_id=subject_id, group_id=group_id))

        response = test_util.session('teacher').get(url)
        parses_json = TestUtil.valid_json(response.text)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertTrue(parses_json)

    def test_student(self):

        student = tests_config.USERS.get('student')
        subject_id, group_id = student.get('groups').get('enrolled')

        url = TestUtil.build_url(self.endpoint.format(subject_id=subject_id, group_id=group_id))

        response = test_util.session('student').get(url)
        parses_json = TestUtil.valid_json(response.text)

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertTrue(parses_json)


class TeachersListViewTest(unittest.TestCase):

    endpoint = '/user/teachers/'

    def test_success(self):
        url = TestUtil.build_url(self.endpoint)
        response = test_util.session('student').get(url)
        parses_json = TestUtil.valid_json(response.text)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertTrue(parses_json)


class StudentsListViewTest(unittest.TestCase):

    endpoint = '/user/students/'

    def test_success(self):
        url = TestUtil.build_url(self.endpoint)
        response = test_util.session('teacher').get(url)
        parses_json = TestUtil.valid_json(response.text)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertTrue(parses_json)

    def test_student(self):

        url = TestUtil.build_url(self.endpoint)

        response = test_util.session('student').get(url)
        parses_json = TestUtil.valid_json(response.text)

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertTrue(parses_json)


class PeerDetailViewSuccess(unittest.TestCase):

    endpoint = '/user/{user_type}/{peer_id}/'

    def test_student_success(self):

        user_type = 'teachers'
        peer_id = tests_config.USERS.get('student').get('peers').get('teacher')
        url = TestUtil.build_url(self.endpoint.format(user_type=user_type, peer_id=peer_id))
        response = test_util.session('student').get(url)
        parses_json = TestUtil.valid_json(response.text)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertTrue(parses_json)

    def test_student_failure(self):
        user_type = 'students'
        peer_id = tests_config.USERS.get('student').get('peers').get('teacher')

        url = TestUtil.build_url(self.endpoint.format(user_type=user_type, peer_id=peer_id))
        response = test_util.session('student').get(url)
        parses_json = TestUtil.valid_json(response.text)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertTrue(parses_json)

    def test_teacher_success_teacher(self):
        user_type = 'teachers'
        peer_id = tests_config.USERS.get('teacher').get('peers').get('teacher')

        url = TestUtil.build_url(self.endpoint.format(user_type=user_type, peer_id=peer_id))
        response = test_util.session('teacher').get(url)
        parses_json = TestUtil.valid_json(response.text)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertTrue(parses_json)

    def test_teacher_success_student(self):
        user_type = 'students'
        peer_id = tests_config.USERS.get('teacher').get('peers').get('student')

        url = TestUtil.build_url(self.endpoint.format(user_type=user_type, peer_id=peer_id))
        response = test_util.session('teacher').get(url)
        parses_json = TestUtil.valid_json(response.text)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertTrue(parses_json)

    def test_teacher_failure_teacher(self):
        user_type = 'teachers'
        peer_id = tests_config.USERS.get('teacher').get('no_peers').get('teacher')

        url = TestUtil.build_url(self.endpoint.format(user_type=user_type, peer_id=peer_id))
        response = test_util.session('teacher').get(url)
        parses_json = TestUtil.valid_json(response.text)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertTrue(parses_json)

    def test_teacher_failure_student(self):
        user_type = 'students'
        peer_id = tests_config.USERS.get('teacher').get('no_peers').get('student')

        url = TestUtil.build_url(self.endpoint.format(user_type=user_type, peer_id=peer_id))

        print url
        response = test_util.session('teacher').get(url)
        parses_json = TestUtil.valid_json(response.text)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertTrue(parses_json)


if __name__ == '__main__':
    unittest.main()

