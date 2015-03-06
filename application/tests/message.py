import os
import sys
import unittest

sys.path.append(os.path.abspath('../'))

from application.services.message import PutMessage, GetMessage


class MessageTest(unittest.TestCase):

    def test_crud(self):
        pm = PutMessage()

        msg = pm.call({'message': 'Lorem ipsum'})
        self.assertEquals('Lorem ipsum', msg.message)

        gm = GetMessage()
        msg_1 = gm.call({'id': msg.id})
        self.assertEquals(msg.id, msg_1.id)


if __name__ == '__main__':
    unittest.main()