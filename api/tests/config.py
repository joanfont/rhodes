from common.environment import Environment

SERVER_URL = Environment.get('TEST_URL')

USERS = {
    'student': {
        'id': 1,
        'user': 'JFR164',
        'password': 'jfr164',
        'token': Environment.get('TOKEN_1'),
        'subjects': {
            'enrolled': 1,
            'not_enrolled': 7
        },
        'groups': {
            'enrolled': [1, 1],
            'not_enrolled': [6, 8]
        },
        'peers': {
            'teacher': 5
        },
        'no_peers': {
            'teacher': 7,
        }
    },
    'teacher': {
        'id': 5,
        'user': 'RGG111',
        'password': 'rgg111',
        'token': Environment.get('TOKEN_2'),
        'subjects': {
            'enrolled': 2,
            'not_enrolled': 1
        },
        'groups': {
            'enrolled': [2, 3]
        },
        'peers': {
            'teacher': 8,
            'student': 1
        },
        'no_peers': {
            'teacher': 7,
            'student': 4,
        }
    }
}


