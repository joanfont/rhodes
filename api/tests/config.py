# SERVER_URL = 'http://rhodes.joan-font.com'
SERVER_URL = 'http://127.0.0.1:8080'

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


