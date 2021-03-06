from flask import request
from api.exceptions.auth import NotAuthenticatedError, NotEnoughPermissionError
from api.exceptions.group import GroupNotFoundError, GroupDoesNotBelongToSubjectError
from api.exceptions.media import MediaNotFoundError, UserCanNotSeeMediaError, LimitOfMessageFilesReachedError, \
    CantAttachMediaToMessageError, FileTooLargeError
from api.exceptions.message import MessageNotFoundErorr, MessageDoesNotBelongToSubjectError, \
    MessageKindIsNotSubjectMessageErrror, MessageDoesNotBelongToGroupError, MessageKindIsNotGroupMessageErrror, \
    MessageDoesNotBelongToConversationError, MessageKindIsNotDirectMessageError, DuplicateMessageWithinIntervalError

from api.exceptions.subject import SubjectNotFoundError
from api.exceptions.user import UserNotFoundError, TeacherDoesNotTeachSubjectError, StudentIsNotEnrolledToSubjectError, \
    TeacherDoesNotTeachGroupError, StudentIsNotEnrolledToGroupError, TeacherNotFoundError, StudentNotFoundError, \
    PeerIsNotTeacherError, PeerIsNotStudentError
from api.exceptions.validation import ValidationError
from application.exceptions import MyValueError
from application.lib.models import UserType, SubjectMessage, GroupMessage, DirectMessage, MediaType, MessageType
from application.services.group import GetGroup
from application.services.media import GetMedia
from application.services.message import GetMessage, GetUserMessagesWithinTimestamps
from common.auth import encode_password

from application.services.user import CheckUserExistsByUserAndPassword, GetUserByAuthToken, UserCanSeeTeacher, GetUser, \
    TeacherCanSeeStudent, GetUserTeacherPeers, GetUserStudentPeers
from application.services.subject import GetSubject
from common.helper import Helper
from config import config
from datetime import datetime
from datetime import timedelta

def copy_params(fnx):

    def wrapped_fnx(*args, **kwargs):

        self = args[0]

        get_params = self.get_data()
        post_params = self.post_data()
        url_params = kwargs
        files_params = self.files_data()

        get = {}
        post = {}
        url = {}
        files = {}

        for (k, v) in get_params.iteritems():
            get[k] = v

        for (k, v) in post_params.iteritems():
            post[k] = v

        for (k, v) in url_params.iteritems():
            url[k] = v

        for(k, v) in files_params.iteritems():
            files[k] = v

        kwargs['get'] = get
        kwargs['post'] = post
        kwargs['url'] = url
        kwargs['files'] = files
        kwargs['streams'] = {}

        return fnx(*args, **kwargs)

    return wrapped_fnx


def validate(fnx):
    def wrapped_fnx(*args, **kwargs):

        self = args[0]

        dispatcher = {
            self.PARAM_URL: kwargs.get('url'),
            self.PARAM_GET: kwargs.get('get'),
            self.PARAM_POST: kwargs.get('post'),
            self.PARAM_FILES: kwargs.get('files'),

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

        user = kwargs.get('post').get('user')
        password = kwargs.get('post').get('password')

        password_encoded = encode_password(password) if password is not None else None

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

        if user.is_teacher():
            return fnx(*args, **kwargs)
        else:
            raise NotEnoughPermissionError()

    return wrapped_fnx


def is_student(fnx):

    # we will assume an instance of User is in kwargs['user']

    def wrapped_fnx(*args, **kwargs):
        user = kwargs.get('user')

        if user.is_student():
            return fnx(*args, **kwargs)
        else:
            raise NotEnoughPermissionError()

    return wrapped_fnx


def subject_exists(fnx):

    # we will assume a subject_id is in kwargs['subject_id']
    def wrapped_fnx(*args, **kwargs):

        subject_id = kwargs.get('url').get('subject_id')

        get_subject_srv = GetSubject()
        subject = get_subject_srv.call({
            'subject_id': subject_id,
        })

        if not subject:
            raise SubjectNotFoundError()
        else:
            kwargs['subject'] = subject

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

        subject_id = kwargs.get('subject').id
        user_subjects = user.get_subject_ids()
        user_belongs = subject_id in user_subjects

        if not user_belongs:
            exception_cls = exception_dispatcher.get(user.type_id)
            raise exception_cls()

        return fnx(*args, **kwargs)

    return wrapped_fnx


def group_exists(fnx):

    def wrapped_fnx(*args, **kwargs):

        group_id = kwargs.get('group_id')

        get_group_srv = GetGroup()
        group = get_group_srv.call({'group_id': group_id})

        if not group:
            raise GroupNotFoundError()
        else:
            kwargs['group'] = group

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

        if not user_belongs:
            exception_cls = dispatcher.get(user.type.id)
            raise exception_cls()

        return fnx(*args, **kwargs)

    return wrapped_fnx


def group_belongs_to_subject(fnx):

    def wrapped_fnx(*args, **kwargs):

        subject = kwargs.get('subject')
        group = kwargs.get('group')

        group_subject_id = int(group.subject_id)
        subject_id = int(subject.id)

        if group_subject_id != subject_id:
            raise GroupDoesNotBelongToSubjectError()

        return fnx(*args, **kwargs)

    return wrapped_fnx


def message_exists(fnx):

    def wrapped_fnx(*args, **kwargs):

        message_id = kwargs.get('url').get('message_id')
        get_message_srv = GetMessage()
        message = get_message_srv.call({'message_id': message_id})
        if not message:
            raise MessageNotFoundErorr()
        else:
            kwargs['message'] = message

        return fnx(*args, **kwargs)

    return wrapped_fnx


def message_belongs_to_subject(fnx):

    def wrapped_fnx(*args, **kwargs):

        subject = kwargs.get('subject')
        message = kwargs.get('message')

        if isinstance(message, SubjectMessage):
            if not message.subject_id == subject.id:
                raise MessageDoesNotBelongToSubjectError()
        else:
            raise MessageKindIsNotSubjectMessageErrror()

        return fnx(*args, **kwargs)

    return wrapped_fnx


def message_belongs_to_group(fnx):

    def wrapped_fnx(*args, **kwargs):

        group = kwargs.get('group')
        message = kwargs.get('message')

        if isinstance(message, GroupMessage):
            if not message.group_id == group.id:
                raise MessageDoesNotBelongToGroupError()
        else:
            raise MessageKindIsNotGroupMessageErrror()

        return fnx(*args, **kwargs)

    return wrapped_fnx


def message_belongs_to_peers(fnx):

    def wrapped_fnx(*args, **kwargs):

        user = kwargs.get('user')
        peer = kwargs.get('peer')
        message = kwargs.get('message')
        if isinstance(message, DirectMessage):
            user_id = int(user.id)
            peer_id = int(peer.id)

            sender_id = int(message.sender_id)
            recipient_id = int(message.user_id)

            cond1 = sender_id == user_id and recipient_id == peer_id
            cond2 = sender_id == peer_id and recipient_id == user_id

            if not cond1 and not cond2:
                raise MessageDoesNotBelongToConversationError()
        else:
            raise MessageKindIsNotDirectMessageError()

        return fnx(*args, **kwargs)

    return wrapped_fnx


def teacher_exists(fnx):

    def wrapped_fnx(*args, **kwargs):

        teacher_id = kwargs.get('url').get('teacher_id')

        get_user_srv = GetUser()
        user = get_user_srv.call({'user_id': teacher_id})

        if not user or not user.is_teacher():
            raise TeacherNotFoundError()
        else:
            kwargs['teacher'] = user

        return fnx(*args, **kwargs)

    return wrapped_fnx


def student_exists(fnx):

    def wrapped_fnx(*args, **kwargs):

        student_id = kwargs.get('url').get('student_id')

        get_user_srv = GetUser()
        user = get_user_srv.call({'user_id': student_id})

        if not user or not user.is_student():
            raise StudentNotFoundError()
        else:
            kwargs['student'] = user

        return fnx(*args, **kwargs)

    return wrapped_fnx


def peer_exists(fnx):

    def wrapped_fnx(*args, **kwargs):

        peer_id = kwargs.get('url').get('peer_id')
        get_user_srv = GetUser()
        user = get_user_srv.call({'user_id': peer_id})
        if not user:
            raise UserNotFoundError()
        else:
            kwargs['peer'] = user

        return fnx(*args, **kwargs)

    return wrapped_fnx


def peer_is_teacher(fnx):

    def wrapped_fnx(*args, **kwargs):
        peer = kwargs.get('peer')
        if peer.is_teacher():
            return fnx(*args, **kwargs)
        else:
            raise PeerIsNotTeacherError()

    return wrapped_fnx


def peer_is_student(fnx):

    def wrapped_fnx(*args, **kwargs):
        peer = kwargs.get('peer')
        if peer.is_student():
            return fnx(*args, **kwargs)
        else:
            raise PeerIsNotStudentError()

    return wrapped_fnx


def user_is_related_to_peer(fnx):

    def wrapped_fnx(*args, **kwargs):

        user = kwargs.get('user')
        peer = kwargs.get('peer')

        if peer.is_teacher():
            srv_class = UserCanSeeTeacher
            key = 'teacher_id'
        elif peer.is_student():
            if user.is_teacher():
                srv_class = TeacherCanSeeStudent
                key = 'student_id'
            else:
                raise NotEnoughPermissionError()

        srv_instance = srv_class()
        is_related = srv_instance.call({
            'user_id': user.id,
            key: peer.id
        })

        if not is_related:
            raise NotEnoughPermissionError()

        return fnx(*args, **kwargs)

    return wrapped_fnx


def users_can_conversate(fnx):

    def wrapped_fnx(*args, **kwargs):

        user = kwargs.get('user')
        peer = kwargs.get('peer')

        if peer.is_teacher():
            srv_class = UserCanSeeTeacher
            param = 'teacher_id'
        elif peer.is_student():
            if user.is_student():
                raise NotEnoughPermissionError()
            elif user.is_teacher():
                srv_class = TeacherCanSeeStudent
                param = 'student_id'

        srv_instance = srv_class()
        can_see = srv_instance.call({
            'user_id': user.id,
            param: peer.id
        })

        if not can_see:
            raise NotEnoughPermissionError()

        return fnx(*args, **kwargs)

    return wrapped_fnx


def user_can_see_teacher(fnx):

    def wrapped_fnx(*args, **kwargs):

        teacher = kwargs.get('teacher')
        user = kwargs.get('user')

        user_can_see_teacher_srv = UserCanSeeTeacher()
        can_see = user_can_see_teacher_srv.call({
            'teacher_id': teacher.id,
            'user_id': user.id
        })

        if not can_see:
            raise NotEnoughPermissionError()

        return fnx(*args, **kwargs)

    return wrapped_fnx


def teacher_can_see_student(fnx):

    def wrapped_fnx(*args, **kwargs):

        student = kwargs.get('student')
        user = kwargs.get('user')

        teacher_can_see_student_srv = TeacherCanSeeStudent()
        can_see = teacher_can_see_student_srv.call({
            'student_id': student.id,
            'user_id': user.id
        })

        if not can_see:
            raise NotEnoughPermissionError()

        return fnx(*args, **kwargs)

    return wrapped_fnx


def can_add_file_to_message(fnx):

    def wrapped_fnx(*args, **kwargs):

        user = kwargs.get('user')
        message = kwargs.get('message')

        if len(message.media) > config.MAX_MESSAGE_FILES:
            raise LimitOfMessageFilesReachedError()

        if message.sender_id != user.id:
            raise CantAttachMediaToMessageError()

        return fnx(*args, **kwargs)

    return wrapped_fnx


def media_exists(fnx):

    def wrapped_fnx(*args, **kwargs):

        media_id = kwargs.get('url').get('media_id')

        get_media_srv = GetMedia()
        media = get_media_srv.call({
            'id': media_id
        })

        if not media:
            raise MediaNotFoundError()

        kwargs['media'] = media
        return fnx(*args, **kwargs)

    return wrapped_fnx


def user_can_see_media(fnx):

    def wrapped_fnx(*args, **kwargs):

        def check_avatar_media():

            peer = media.user

            srv_dispatcher = {
                UserType.TEACHER: GetUserTeacherPeers,
                UserType.STUDENT: GetUserStudentPeers
            }

            get_peers_cls = srv_dispatcher.get(peer.type_id)
            get_peers_srv = get_peers_cls()

            peers = get_peers_srv.call({
                'user_id': user.id
            })

            peer_ids = map(lambda x: int(x.id), peers)

            return int(peer.id) in peer_ids or int(peer.id) == int(user.id)

        def check_message_media():
            message = media.message
            message_type = message.type

            if message_type == MessageType.DIRECT_MESSAGE:
                can_see_message = message.sender_id == user.id or message.user_id == user.id
            elif message_type == MessageType.GROUP_MESSAGE:
                can_see_message = message.group_id in user.get_groups_ids()
            elif message_type == MessageType.SUBJECT_MESSAGE:
                can_see_message = message.subject_id in user.get_subject_ids()

            return can_see_message

        dispatcher = {
            MediaType.AVATAR: check_avatar_media,
            MediaType.MESSAGE_FILE: check_message_media
        }

        user = kwargs.get('user')
        media = kwargs.get('media')

        check_fnx = dispatcher.get(media.type)

        can_see = check_fnx()

        if not can_see:
            raise UserCanNotSeeMediaError()

        return fnx(*args, **kwargs)

    return wrapped_fnx


def file_to_stream(field):

    def file_to_stream_decorator(fnx):

        def wrapped_fnx(*args, **kwargs):

            f = kwargs.get('files').get(field)
            bio = Helper.werkzeug_to_stream(f)

            kwargs['streams'][field] = bio

            return fnx(*args, **kwargs)

        return wrapped_fnx

    return file_to_stream_decorator

def file_max_length(field):

    def file_max_length_decorator(fnx):

        def wrapped_fnx(*args, **kwargs):

            f = kwargs.get('streams').get(field)

            if len(f.getvalue()) > config.MAX_FILE_SIZE:
                raise FileTooLargeError()

            return fnx(*args, **kwargs)

        return wrapped_fnx

    return file_max_length_decorator

def check_message_interval(fnx):

    def wrapped_fnx(*args, **kwargs):

        def _filter_with_same_body(message):
            return message.body.content == body

        body = kwargs.get('post').get('body')
        user = kwargs.get('user')

        to = datetime.now()
        _from = to - timedelta(seconds=config.MESSAGE_INTERVAL)

        get_messages_srv = GetUserMessagesWithinTimestamps()
        messages = get_messages_srv.call({
            'user_id': user.id,
            'from': _from,
            'to': to
        })

        messages_with_same_body = filter(_filter_with_same_body, messages)

        if len(messages_with_same_body) > 0:
            raise DuplicateMessageWithinIntervalError()
        else:
            return fnx(*args, **kwargs)

    return wrapped_fnx


