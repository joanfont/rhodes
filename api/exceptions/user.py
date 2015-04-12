from api.exceptions import ObjectNotFoundError, ForbiddenActionError


class UserNotFoundError(ObjectNotFoundError):

    message = 'User not found'


class TeacherDoesNotTeachSubjectError(ForbiddenActionError):

    message = 'Teacher does not teach the subject'


class StudentIsNotEnrolledToSubjectError(ForbiddenActionError):

    message = 'Student is not enrolled to the subject'


class TeacherDoesNotTeachGroupError(ForbiddenActionError):

    message = 'Teacher does not teach the group'


class StudentIsNotEnrolledToGroupError(ForbiddenActionError):

    message = 'Student is not enrolled to the group'