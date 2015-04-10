from application.exceptions import ObjectNotFoundError


class UserNotFoundError(ObjectNotFoundError):

    MESSAGE = 'User not found'


# TODO: fix
class TeacherDoesNotTeachSubjectError(ObjectNotFoundError):

    MESSAGE = 'Teacher does not teach the subject'


# TODO: fix
class StudentIsNotEnrolledToSubjectError(ObjectNotFoundError):

    MESSAGE = 'Student is not enrolled to the subject'


# TODO: fix
class TeacherDoesNotTeachGroupError(ObjectNotFoundError):

    MESSAGE = 'Teacher does not teach the group'


# TODO: fix
class StudentIsNotEnrolledToGroupError(ObjectNotFoundError):

    MESSAGE = 'Student is not enrolled to the group'