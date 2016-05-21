from common.environment import Environment

SERVER_HOST = Environment.get('GUNICORN_HOST')
SERVER_PORT = Environment.get('GUNICORN_PORT')

SERVER_URL = 'http://{host}:{port}'.format(host=SERVER_HOST, port=SERVER_PORT)

USERS = {
    'student': {
        'id': 1,
        'user': 'JFR164',
        'password': 'jfr164',
        'token': 'OLlmxXLkS2vdi1zEWy44W1vFj02gCFbv76JSI3Q6cS8=',
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
        'token': 'KchqozGR6JsZkB0VO1tojMAWMhIsQcDr3/TVwl/vLO4=',
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


