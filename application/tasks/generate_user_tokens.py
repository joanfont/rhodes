from flask.ext.script import Command
from application.lib.models import User
from common.session import manager
from common.auth import encode_auth_token
from common.auth import encode_password


class GenerateUserTokens(Command):

    @staticmethod
    def generate_user_token(u):

        token = u.generate_auth_token()
        b64t = encode_auth_token(token)
        u.auth_token = b64t

        if not u.password:
            password = u.user.lower()
            md5passwd = encode_password(password)
            u.password = md5passwd

    def run(self):
        session = manager.get('standalone')

        users = session.query(User).all()

        for user in users:
            print 'Generating token for user {user}'.format(user=user.user)
            self.generate_user_token(user)

        session.commit()







