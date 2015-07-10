import os
from common.environment import Environment

DB_DSN = '{driver}://{user}:{passw}@{host}/{name}?charset=utf8&use_unicode=0'.format(
    driver=Environment.get('DB_DRIVER'),
    user=Environment.get('DB_USER'),
    passw=Environment.get('DB_PASS'),
    host=Environment.get('DB_HOST'),
    name=Environment.get('DB_NAME'))

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

MESSAGE_MAX_LENGTH = 400

ITEMS_PER_PAGE = 15

LOG_FILE = os.path.realpath('log/rhodes.log')

PRIVATE_KEY = Environment.get('PRIVATE_KEY')

ALLOWED_MIME_TYPES = [
    'image/png',
    'image/jpeg',
    'image/pjpeg',
    'image/gif',
    'image/bmp'
]

MAX_FILE_SIZE = 2 * 1024 * 1024

MAX_MESSAGE_FILES = 5
MEDIA_FOLDER = 'media/'
MESSAGE_INTERVAL = 15
