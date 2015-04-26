from flask import request
from api.exceptions.auth import NotAuthenticatedError, NotEnoughPermissionError
from api.exceptions.group import GroupNotFoundError, GroupDoesNotBelongToSubjectError
from api.exceptions.message import MessageNotFoundErorr, MessageDoesNotBelongToSubjectError, \
    MessageKindIsNotSubjectMessageErrror, MessageDoesNotBelongToGroupError, MessageKindIsNotGroupMessageErrror, \
    ConversationDoesNotExistsBetweenUsersError
from api.exceptions.subject import SubjectNotFoundError
from api.exceptions.user import UserNotFoundError, TeacherDoesNotTeachSubjectError, StudentIsNotEnrolledToSubjectError, \
    TeacherDoesNotTeachGroupError, StudentIsNotEnrolledToGroupError, TeacherNotFoundError, StudentNotFoundError
from api.exceptions.validation import ValidationError
from application.exceptions import MyValueError
from application.lib.models import UserType, SubjectMessage, GroupMessage
from application.services.group import GroupBelongsToSubject, CheckGroupExists
from application.services.message import CheckMessageExists, GetMessage
from common.auth import encode_password

from application.services.user import CheckUserExistsByUserAndPassword, GetUserByAuthToken, UserCanSeeTeacher, GetUser, \
    TeacherCanSeeStudent, CheckConversationExistsBetweenUsers
from application.services.subject import CheckSubjectExists


def copy_params(fnx):

    def wrapped_fnx(*args, **kwargs):

        self = args[0]

        get_params = self.get_data()
        post_params = self.post_data()
        url_params = kwargs

        get = {}
        post = {}
        url = {}

        for (k, v) in get_params.iteritems():
            get[k] = v

        for (k, v) in post_params.iteritems():
            post[k] = v

        for (k, v) in url_params.iteritems():
            url[k] = v

        kwargs['get'] = get
        kwargs['post'] = post
        kwargs['url'] = url

        return fnx(*args, **kwargs)

    return wrapped_fnx


def validate(fnx):
    def wrapped_fnx(*args, **kwargs):

        self = args[0]

        dispatcher = {
            self.PARAM_URL: kwargs.get('url'),
            self.PARAM_GET: kwargs.get('get'),
            self.PARAM_POST: kwargs.get('post'),

        }

        params = self.params()
        validation_errors = []

        for (name, v) in params.iteritems():

            source, validator = v

            dictionary = dispatcher.get(source)
            value = dictionary.get(name)

            try:
                dictionary[name] = validator.validate(value)
            except MyValueError, e:
                validation_error = {
                    'field': name,
                    'errors': e.get_errors()}
                validation_errors.append(validation_error)
        if validation_errors:
            payload = {'errors': validation_errors}
            e = ValidationError(payload=payload)
            raise e

        return fnx(*args, **kwargs)

    return wrapped_fnx


def login_required(fnx):
    def wrapped_fnx(*args, **kwargs):
        user = kwargs.get('get').get('user')
        password = kwargs.get('get').get('password')
        password_encoded = encode_password(password)

        get_user_srv = CheckUserExistsByUserAndPassword()
        exists = get_user_srv.call({
            'user': user,
            'password': password_encoded
        })

        if not exists:
            raise UserNotFoundError()

        return fnx(*args, **kwargs)

    return wrapped_fnx


def auth_token_required(fnx):
    def wrapped_fnx(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            raise NotAuthenticatedError()

        get_user_by_token = GetUserByAuthToken()
        user = get_user_by_token.call({
            'auth_token': token
        })

        if not user:
            raise NotAuthenticatedError()

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


def is_student(fnx):
    # we will assume an instance of User is in kwargs['user']

    def wrapped_fnx(*args, **kwargs):
        user = kwargs.get('user')

        if not user.is_student():
            raise NotEnoughPermissionError()

        return fnx(*args, **kwargs)

    return wrapped_fnx


def subject_exists(fnx):

    # we will assume a subject_id is in kwargs['subject_id']
    def wrapped_fnx(*args, **kwargs):
        subject_id = kwargs.get('url').get('subject_id')

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
        user = kwargs.get('user')

        exception_dispatcher = {
            UserType.TEACHER: TeacherDoesNotTeachSubjectError,
            UserType.STUDENT: StudentIsNotEnrolledToSubjectError,
        }

        subject_id = kwargs.get('url').get('subject_id')
        user_subjects = user.get_subject_ids()
        user_belongs = subject_id in user_subjects

        # check_user_belongs_to_subject_srv = CheckUserBelongsToSubject()
        # user_belongs = check_user_belongs_to_subject_srv.call({
        # 'subject_id': subject_jd,
        #     'user_id': user.id
        # })

        if not user_belongs:
            exception_cls = exception_dispatcher.get(user.type_id)
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
        group_id = kwargs.get('url').get('group_id')

        user_groups = user.get_groups_ids()
        user_belongs = group_id in user_groups

        # check_user_belongs_to_group_srv = CheckUserBelongsToGroup()
        # user_belongs = check_user_belongs_to_group_srv.call({
        # 'group_id': group_id,
        #     'user_id': user.id
        # })

        if not user_belongs:
            exception_cls = dispatcher.get(user.type.id)
            raise exception_cls()

        return fnx(*args, **kwargs)

    return wrapped_fnx


def group_belongs_to_subject(fnx):

    def wrapped_fnx(*args, **kwargs):
        subject_id = kwargs.get('url').get('subject_id')
        group_id = kwargs.get('url').get('group_id')

        group_belongs_to_subject_srv = GroupBelongsToSubject()

        group_belongs = group_belongs_to_subject_srv.call({
            'group_id': group_id,
            'subject_id': subject_id
        })

        if not group_belongs:
            raise GroupDoesNotBelongToSubjectError()

        return fnx(*args, **kwargs)

    return wrapped_fnx


def message_exists(fnx):

    def wrapped_fnx(*args, **kwargs):

        message_id = kwargs.get('url').get('from_message_id')

        if message_id:
            # check_message_exists_srv = CheckMessageExists()
            # exists = check_message_exists_srv.call({'message_id': message_id})

            check_message_exists = CheckMessageExists()
            exists = check_message_exists.call({'message_id': message_id})

            if not exists:
                raise MessageNotFoundErorr()

        return fnx(*args, **kwargs)

    return wrapped_fnx


def message_belongs_to_subject(fnx):

    def wrapped_fnx(*args, **kwargs):

        subject_id = kwargs.get('url').get('subject_id')
        message_id = kwargs.get('get').get('from_message_id')

        if message_id:
            get_message_srv = GetMessage()
            message = get_message_srv.call({'message_id': message_id})

            if not message:
                raise MessageNotFoundErorr()

            if isinstance(message, SubjectMessage):

                if not message.subject_id == subject_id:
                    raise MessageDoesNotBelongToSubjectError()
            else:
                raise MessageKindIsNotSubjectMessageErrror()

        return fnx(*args, **kwargs)

    return wrapped_fnx


def message_belongs_to_group(fnx):

    def wrapped_fnx(*args, **kwargs):

        group_id = kwargs.get('url').get('group_id')
        message_id = kwargs.get('get').get('from_message_id')

        if message_id:
            get_message_srv = GetMessage()
            message = get_message_srv.call({'message_id': message_id})

            if not message:
                raise MessageNotFoundErorr()

            if isinstance(message, GroupMessage):
                if not message.group_id == group_id:
                    raise MessageDoesNotBelongToGroupError()
            else:
                raise MessageKindIsNotGroupMessageErrror()

        return fnx(*args, **kwargs)

    return wrapped_fnx

def message_belongs_to_peers(fnx):

    def wrapped_fnx(*args, **kwargs):

        user = kwargs.get('user')
        peer_id = kwargs.get('url').get('teacher_id') or kwargs.get('url').get('student_id')

        message_id = kwargs.get('get').get('from_message_id')


def teacher_exists(fnx):

    def wrapped_fnx(*args, **kwargs):

        teacher_id = kwargs.get('url').get('teacher_id')

        get_user_srv = GetUser()
        user = get_user_srv.call({'user_id': teacher_id})

        if not user or not user.is_teacher():
            raise TeacherNotFoundError()

        return fnx(*args, **kwargs)

    return wrapped_fnx


def student_exists(fnx):

    def wrapped_fnx(*args, **kwargs):

        student_id = kwargs.get('url').get('student_id')

        get_user_srv = GetUser()
        user = get_user_srv.call({'user_id': student_id})

        if not user or not user.is_student():
            raise StudentNotFoundError()

        return fnx(*args, **kwargs)

    return wrapped_fnx


def user_can_see_teacher(fnx):

    def wrapped_fnx(*args, **kwargs):

        teacher_id = kwargs.get('url').get('teacher_id')
        user = kwargs.get('user')

        user_can_see_teacher_srv = UserCanSeeTeacher()
        can_see = user_can_see_teacher_srv.call({
            'teacher_id': teacher_id,
            'user_id': user.id
        })

        if not can_see:
            raise NotEnoughPermissionError()

        return fnx(*args, **kwargs)

    return wrapped_fnx


def teacher_can_see_student(fnx):

    def wrapped_fnx(*args, **kwargs):

        student_id = kwargs.get('url').get('student_id')
        user = kwargs.get('user')

        teacher_can_see_student_srv = TeacherCanSeeStudent()
        can_see = teacher_can_see_student_srv.call({
            'student_id': student_id,
            'user_id': user.id
        })

        if not can_see:
            raise NotEnoughPermissionError()

        return fnx(*args, **kwargs)

    return wrapped_fnx


def check_conversation_exists_between_users(fnx):

    def wrapped_fnx(*args, **kwargs):

        user = kwargs.get('user')
        peer_id = kwargs.get('url').get('peer_id')

        check_conversation_exists_between_users_srv = CheckConversationExistsBetweenUsers()
        exists = check_conversation_exists_between_users_srv.call({
            'user_id_1': user.id,
            'user_id_2': peer_id
        })

        if not exists:
            raise ConversationDoesNotExistsBetweenUsersError()

        return fnx(*args, **kwargs)

    return wrapped_fnx
