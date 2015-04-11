from api.exceptions import ObjectNotFoundError


class UserNotFoundError(ObjectNotFoundError):

    message = 'User not found'


class TeacherDoesNotTeachSubjectError(ObjectNotFoundError):

    message = 'Teacher does not teach the subject'


class StudentIsNotEnrolledToSubjectError(ObjectNotFoundError):

    message = 'Student is not enrolled to the subject'


class TeacherDoesNotTeachGroupError(ObjectNotFoundError):

    message = 'Teacher does not teach the group'


class StudentIsNotEnrolledToGroupError(ObjectNotFoundError):

    message = 'Student is not enrolled to the group'