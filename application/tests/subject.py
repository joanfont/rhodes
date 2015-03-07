import os
import sys
import unittest

sys.path.append(os.path.abspath('../'))

from application.services.subject import GetStudentSubjects


class SubjectTest(unittest.TestCase):

    def test_dummy(self):

        s = GetStudentSubjects()
        ss = s.call({'student_id': 1})
        print ss