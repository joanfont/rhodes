from api.exceptions import ObjectNotFoundError, ForbiddenActionError, ConflictError


class UserNotFoundError(ObjectNotFoundError):

    message = 'User not found'


class TeacherNotFoundError(ObjectNotFoundError):

    message = 'Teacher not found'


class StudentNotFoundError(ObjectNotFoundError):

    message = 'Student not found'


class TeacherDoesNotTeachSubjectError(ForbiddenActionError):

    message = 'Teacher does not teach the subject'


class StudentIsNotEnrolledToSubjectError(ForbiddenActionError):

    message = 'Student is not enrolled to the subject'


class TeacherDoesNotTeachGroupError(ForbiddenActionError):

    message = 'Teacher does not teach the group'


class StudentIsNotEnrolledToGroupError(ForbiddenActionError):

    message = 'Student is not enrolled to the group'


class PeerIsNotTeacherError(ConflictError):

    message = 'The requested peer is not a teacher'


class PeerIsNotStudentError(ConflictError):

    message = 'The requested peer is not a student'