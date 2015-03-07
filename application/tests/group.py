import os
import sys
import unittest

sys.path.append(os.path.abspath('../'))

from application.services.group import GetSubjectGroups


class GroupTest(unittest.TestCase):

    def test_get_subject_groups(self):

        gsg = GetSubjectGroups()
        subject_groups = gsg.call({'subject_id': 1})
        print subject_groups
        self.assertIsNotNone(subject_groups)


