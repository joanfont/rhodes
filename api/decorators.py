from flask import request
from application.lib.models import UserType

from common.exceptions import NotAuthenticatedError, TeacherDoesNotTeachSubjectError, StudentIsNotEnrolledToSubjectError, \
    InvalidParameterError, SubjectNotFoundError

from application.services.user import GetUser
from application.services.subject import CheckUserBelongsToSubject, CheckSubjectExists


def login_required(fnx):

    def wrapped_fnx(*args, **kwargs):
        user_id = request.headers.get('X-UIB-User')

        if not user_id:
            raise NotAuthenticatedError()

        get_user_srv = GetUser()
        user = get_user_srv.call({'user_id': user_id})
        kwargs['user'] = user
        return fnx(*args, **kwargs)

    return wrapped_fnx


def check_subject_exists(fnx):

    # we will assume a subject_id is in kwargs['subject_id']

    def wrapped_fnx(*args, **kwargs):

        subject_id = kwargs.get('subject_id')

        if not subject_id:
            raise InvalidParameterError()

        check_subject_exists_srv = CheckSubjectExists()
        subject_exists = check_subject_exists_srv.call({'subject_id': subject_id})

        if not subject_exists:
            raise SubjectNotFoundError()

        return fnx(*args, **kwargs)

    return wrapped_fnx


def belong_to_subject(fnx):

    # we will assume an user instance is in kwargs['user']
    # if not we can't check if a user belongs to subject
    # So this decorator must be called after @login_required
    def wrapped_fnx(*args, **kwargs):

        dispatcher = {
            UserType.TEACHER: TeacherDoesNotTeachSubjectError,
            UserType.STUDENT: StudentIsNotEnrolledToSubjectError,
        }

        subject_jd = kwargs.get('subject_id')
        user = kwargs.get('user')

        check_user_belongs_to_subject_srv = CheckUserBelongsToSubject()
        user_belongs_to_subject = check_user_belongs_to_subject_srv.call({
            'subject_id': subject_jd,
            'user_id': user.id
        })

        if not user_belongs_to_subject:
            exception_cls = dispatcher.get(user.type_id)
            raise exception_cls()

        return fnx(*args, **kwargs)

    return wrapped_fnx