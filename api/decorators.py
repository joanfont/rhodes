from flask import request

from common.exceptions import NotAuthenticatedError

from application.services.user import GetUser


def login_required(fnx):

    def wrapped_fnx(*args, **kwargs):
        user_id = request.headers.get('X-UIB-User')

        if not user_id:
            raise NotAuthenticatedError()

        get_user_srv = GetUser()
        user = get_user_srv.call({'id': user_id})
        kwargs['user'] = user
        return fnx(*args, **kwargs)

    return wrapped_fnx