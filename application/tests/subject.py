import os
import sys
import unittest

sys.path.append(os.path.abspath('../'))

from application.services.subject import GetSubjects


class SubjectTest(unittest.TestCase):

    def test_get(self):

        gs = GetSubjects()
        subjects = gs.call({})
        dicts = map(lambda x: x.to_dict(), subjects)
        print dicts
        self.assertIsNotNone(subjects)

if __name__ == '__main__':
    unittest.main()