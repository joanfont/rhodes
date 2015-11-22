import os
import dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.dirname(os.path.realpath(__file__))

env_file = os.path.realpath(os.path.join(BASE_DIR, '.env'))
dotenv.read_dotenv(env_file)

from common.environment import Environment

DB_DSN = '{driver}://{user}:{passw}@{host}:{port}/{name}?charset=utf8&use_unicode=0'.format(
    driver=Environment.get('DATABASE_DRIVER'),
    user=Environment.get('DATABASE_USER'),
    passw=Environment.get('DATABASE_PASS'),
    host=Environment.get('DATABASE_HOST'),
    port=Environment.get('DATABASE_PORT'),
    name=Environment.get('DATABASE_NAME'))

print(DB_DSN)

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
