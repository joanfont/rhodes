import unittest
from application.tests.base import BaseTest


class ProfileViewTest(BaseTest):

    status_code = 200
    endpoint = '/user/'

    def test(self):
        url = self.build_url(self.endpoint)
        response = self.get(url)

        parses_json = self.valid_json(response.text)

        self.assertEqual(self.status_code, response.status_code)
        self.assertTrue(parses_json)


if __name__ == '__main__':
    unittest.main()

