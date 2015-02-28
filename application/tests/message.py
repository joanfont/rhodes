import os
import sys
sys.path.append(os.path.abspath('../'))

import unittest

from services.message import PutMessage 

class NumbersTest(unittest.TestCase):

  def setUp(self):
    pass

  def test_allOptions(self):

   pm = PutMessage()

   msg = pm.call({'message' : 'Lorem ipsum'})
   self.assertEquals('Lorem ipsum', msg.message)


if __name__ == '__main__':
  unittest.main()