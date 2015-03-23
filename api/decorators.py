from flask import request
from application.lib.models import UserType
from application.services.group import CheckUserBelongsToGroup, GroupBelongsToSubject, CheckGroupExists

from common.exceptions import NotAuthenticatedError, TeacherDoesNotTeachSubjectError, StudentIsNotEnrolledToSubjectError, \
    InvalidParameterError, SubjectNotFoundError, TeacherDoesNotTeachGroupError, StudentIsNotEnrolledToGroupError, \
    GroupDoesNotBelongToSubjectError, GroupNotFoundError, NotEnoughPermissionError

from application.services.user import GetUser
from application.services.subject import CheckUserBelongsToSubject, CheckSubjectExists


def login_required(fnx):

    def wrapped_fnx(*args, **kwargs):
        user_id = request.headers.get('Authorization')

        if not user_id:
            raise NotAuthenticatedError()

        get_user_srv = GetUser()
        user = get_user_srv.call({'user_id': user_id})
        kwargs['user'] = user
        return fnx(*args, **kwargs)

    return wrapped_fnx


def is_teacher(fnx):

    # we will assume an instance of User is in kwargs['user']

    def wrapped_fnx(*args, **kwargs):

        user = kwargs.get('user')

        if not user.is_teacher():
            raise NotEnoughPermissionError()

        return fnx(*args, **kwargs)

    return wrapped_fnx


def subject_exists(fnx):

    # we will assume a subject_id is in kwargs['subject_id']

    def wrapped_fnx(*args, **kwargs):

        subject_id = kwargs.get('subject_id')

        if not subject_id:
            raise InvalidParameterError()

        check_subject_exists_srv = CheckSubjectExists()
        exists = check_subject_exists_srv.call({'subject_id': subject_id})

        if not exists:
            raise SubjectNotFoundError()

        return fnx(*args, **kwargs)

    return wrapped_fnx


def user_belongs_to_subject(fnx):

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
        user_belongs = check_user_belongs_to_subject_srv.call({
            'subject_id': subject_jd,
            'user_id': user.id
        })

        if not user_belongs:
            exception_cls = dispatcher.get(user.type_id)
            raise exception_cls()

        return fnx(*args, **kwargs)

    return wrapped_fnx


def group_exists(fnx):

    def wrapped_fnx(*args, **kwargs):

        group_id = kwargs.get('group_id')

        check_group_exists_srv = CheckGroupExists()
        exists = check_group_exists_srv.call({'group_id': group_id})

        if not exists:
            raise GroupNotFoundError()

        return fnx(*args, **kwargs)

    return wrapped_fnx


def user_belongs_to_group(fnx):

    def wrapped_fnx(*args, **kwargs):

        dispatcher = {
            UserType.TEACHER: TeacherDoesNotTeachGroupError,
            UserType.STUDENT: StudentIsNotEnrolledToGroupError,
        }

        user = kwargs.get('user')
        group_id = kwargs.get('group_id')

        check_user_belongs_to_group_srv = CheckUserBelongsToGroup()
        user_belongs = check_user_belongs_to_group_srv.call({
            'group_id': group_id,
            'user_id': user.id
        })

        if not user_belongs:
            exception_cls = dispatcher.get(user.type.id)
            raise exception_cls()

        return fnx(*args, **kwargs)

    return wrapped_fnx


def group_belongs_to_subject(fnx):

    def wrapped_fnx(*args, **kwargs):

        subject_id = kwargs.get('subject_id')
        group_id = kwargs.get('group_id')

        group_belongs_to_subject_srv = GroupBelongsToSubject()

        group_belongs = group_belongs_to_subject_srv.call({
            'group_id': group_id,
            'subject_id': subject_id
        })

        if not group_belongs:
            raise GroupDoesNotBelongToSubjectError()

        return fnx(*args, **kwargs)

    return wrapped_fnx