import unittest
from application.tests.base import BaseTest
from application.tests import config as tests_config


class ProfileViewTest(BaseTest):

    status_code = 200
    endpoint = '/user/'

    def test(self):
        url = self.build_url(self.endpoint)
        response = self.session.get(url)

        parses_json = self.valid_json(response.text)

        self.assertEqual(self.status_code, response.status_code)
        self.assertTrue(parses_json)


class LoginViewTest(BaseTest):

    status_code = 200
    endpoint = '/login/'

    def test(self):
        params = {'user': 'JFR164', 'password': 'jfr164'}
        url = self.build_url(self.endpoint, params)
        response = self.session.get(url)
        parses_json = self.valid_json(response.text)
        self.assertEqual(self.status_code, response.status_code)
        self.assertTrue(parses_json)

        if parses_json:
            data = response.json()
            token = data.get('token')
            self.assertEqual(tests_config.TOKEN, token)


if __name__ == '__main__':
    unittest.main()

