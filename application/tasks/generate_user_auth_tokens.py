import sys
sys.path.append('/root/rhodes/')

from application.lib.models import User
from common.session import manager
from common.auth import encode_auth_token
from common.auth import encode_password


def generate_user_auth_token(user):
    token = user.generate_auth_token()
    password = user.user.lower()
    md5passwd = encode_password(password)
    b64t = encode_auth_token(token)
    user.auth_token = b64t
    user.password = md5passwd


if __name__ == '__main__':

    Session = manager.get('standalone')
    s = Session()

    users = s.query(User).all()
    users = map(generate_user_auth_token, users)
    s.commit()