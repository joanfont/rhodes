import os
import sys
import unittest

from datetime import datetime

sys.path.append(os.path.abspath('../../'))

from application.services.message import PutGroupMessage


class MessageTest(unittest.TestCase):

    def test_put(self):

        srv = PutGroupMessage()
        message = srv.call({
            'sender_id': 1,
            'body': 'Lorem ipsum dolor sit amet',
            'created_at': datetime.now(),
            'recipient_id': 1,
        })

        print message



if __name__ == '__main__':

    unittest.main()