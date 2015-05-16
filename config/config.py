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

PRIVATE_KEY = 'ZMsgjYbXyzHog7AtPvfiI2OW3cDTvycuYYztbYpT9tX3xsmgJMvSrtd3HtqOl9Okf2sBaSAKvfY2Fz76T9pr9BnEh5SPxt81f7mO' \
              'nfmtWiXBKGVCP8aBZqWNEl0jGMfR9qd30CoL2mNxIQZGS5l6BZQpt5fztPD7Mi5VFv5CrsGucW6ts3rQhZZ7usZLAX1Y60ltqfwS' \
              'uj822aqQtfSd5mazrJIcHBeHLA0a60W80zPxT8mfJAotg6xPZAJ0H0J71AATDgP0jlKtNCMil7AHcdkMSTH7UlQyv8mCu8KsVFm8' \
              'MKaPYF3kB1XozdtzjFbjhEyGxOYquViw4jFAklSGWW2gzJulzHNylABrWKm7HtYvKXdGsMnfymOueWMKkfYSgivWII331Qp8HlPI' \
              'xe8ZyPWdNhyx50ISLgyENWwc88Dde7rOaOw6NAFTdpprmW6CmA77FDEM2PwW5cXxNCohY7UWUVSCNLiDOsLs1TLwwE5f2mHiJSUi' \
              'vQYG2bzbAEG4rlRgBX1oDn08FC8Rx6rMaAYOQlnlQMTsKCBpM7IgIUcClldr7jn85H2uVeRwqUjp4LwiV5B7l7ZO2CDooFTCQiHK' \
              'PDayDRjaz9GOl7fqX1NB4jNhK77hphad5nYPokmMfMCGjPr4MXDAx7qT348UBUMmRVESOBJloFAlnDIviezcRfZY85QWW0Z8PZpF' \
              '7uIv6JF8lyoTO0KwIpoQRHJ52VwTBefVpPDdqLk9qSHq1xeSODSo0hJCUckJ3AvgID6JLeHLNAa3UVkbvVDxruBGd6I233KQqqB0' \
              'ksqzLnanasppbC7DtXv2RYpbj5clUm7a7LaxzRkigklXqCgN0apDVwAm4wNglAVQ4NkCdEhxHpQWZ6ztm7MPm1uQbL2VMNyx1B7s' \
              'zyW8J0mtlAE6nx9Xk79bBU7lj9uXM2DFcZWWlPph6XsDpFQgGdmMJV7KX1Fd474B3xqhfFNHPtguo4TugaAOTP9NGGx5zEgDfa9S' \
              'YtRASZBDjIxYlCMUfusVs5g54eeVUACI4iJ29fU4FL1XzrxtpxMhI3hsJ94ksIqUx14kggG6rc72isFc1aCBdtBAAreSLbmJ1Pim' \
              'PF1Ujo5i1bXqRx6mznutHvnzfc8UTHe97AZus8KCcSGiXJ9xN1UHPkiXIOqgAKZBTieA9tkj27O1a9Tg4SE4OgzlrfeuZCFpfe6q' \
              'gdBpDvj0kR5PnRHdish9pHsnzNStiZCvVhZ1oJafmjGesKyQlcVVe8hLKIch5ciFCdbRr12i7OvZ85bYnKN5EhMiC5Mchc5vn07B' \
              'XGQ5d0n2iO2OpNMyfjY7NqWqmcFDVbKmBVPz3JLAUgVTHG2isyMSSOCZYZ4oFky2Qn9zx5R6EntYWPw6utiq2CR1R8u0FEUiGuJI' \
              'vJg14u1Y9A0PCa2mDUDSeeemdTPzMDcUDSAGBSRtQULEElv1WTHulm7R3lvRl9AEF0y8ex35lhtZCZJmHepCh1wWIBJkctqXKhbr' \
              'IqUkEgVRBxyJlp0zUzwY9iFeDQNTNponA6Ng9eAsI3vkFTg3fitDJJZsRBSkqFWiCvaLA8kv3Ci0d5oArD8ABSVxN2RRZ2puE0zc' \
              '84oJnDDryGKdGfCTNcLSGMbJxn5NFH2s33pAiwRZJ5Sntf4y1E99d2YREtzRmbZPAl2PzgRFdF3OadsCiEJV9qSDQrzLm3GIGKo9' \
              'oJ1aclUHwzMYxpOQhi9iaa2mSk7qFEXTQ7tFKLzXf9cx0TE8804yr53pxgxZqrqRrDzXasi7HcckPOhpSuXr0lMhmHwf8IoxIgbq' \
              'mjA4kNQzLbfloU7xbD35bu7rUMOFB3YPigzTMtl0xCK1P5V8QGgpj2eQOt5YQeZKS5T1Vb2lRAo2zUTMRp55hYyX885ry3kzsA2g' \
              'FfBxXSeO8NqKEwdp1XEuHgSanAzo54DM9vbHGr4yXSiZhuQABZLkXEZO6fG1W1eUNDLfbDsWkMaYzXmZ4yYNcwqlH1XddmvtUzXX' \
              'JUIy0vhqKw01gUdmtuhL5BnSYWUFdGhKgLyM3lKP5SNiMZCo'

ALLOWED_MIME_TYPES = [
    'image/png',
    'image/jpeg',
    'image/pjpeg'
    'image/gif',
    'image/bmp',
]

MAX_FILE_SIZE = 2 * 1024 * 1024

MEDIA_FOLDER = 'media/'
