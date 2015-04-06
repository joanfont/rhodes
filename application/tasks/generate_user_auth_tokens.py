from application.lib.models import User
from common.session import manager



def generate_user_auth_token(user):
    user.auth_token = user.generate_auth_token()


if __name__ == '__main__':

    Session = manager.get('standalone')
    s = Session()

    users = s.query(User).all()
    users = map(generate_user_auth_token, users)
    s.commit()