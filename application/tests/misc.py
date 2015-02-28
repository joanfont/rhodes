import os
import sys
sys.path.append(os.path.abspath('../'))

import unittest

from services.misc import Pow 

class NumbersTest(unittest.TestCase):

  def setUp(self):
    pass

  def test_allOptions(self):

    p = Pow()
    r1 = p.call({'base' : 2})
    self.assertEqual(r1, 4)

    r2 = p.call({'base': 2, 'exponent': 3})
    self.assertEqual(r2, 8)


if __name__ == '__main__':
  unittest.main()