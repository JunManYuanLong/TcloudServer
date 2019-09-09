from public_config import MSG_MAP


class Error(Exception):
    """Base error class.
    Child classes should define an HTTP status code, title, and a
    message_format.
    """

    code = None
    message = None

    def __init__(self, message=None):
        if message:
            self.message = message
        else:
            self.message = MSG_MAP.get(self.code)

        super(Error, self).__init__(self.message)


class CannotFindObjectException(Error):
    code = 101


class SaveObjectException(Error):
    code = 102


class ConfilctObjectException(Error):
    code = 103


class CreateObjectException(Error):
    code = 104


class RemoveObjectException(Error):
    code = 105


class OperationFailedException(Error):
    code = 106


class PermissionDeniedException(Error):
    code = 108


class ProjectPermissionDeniedException(Error):
    code = 109


class OperationPermissionDeniedException(Error):
    code = 110


class FieldMissingException(Error):
    code = 201


class FieldLengthErrorException(Error):
    code = 202


class DataTypeErrorException(Error):
    code = 203


class PasswordWrongException(Error):
    code = 301


class PasswordOrUserNameWrongException(Error):
    code = 302


class MethodNotAllowedException(Error):
    code = 403


class AuthExpiredException(Error):
    code = 410


class AuthErrorException(Error):
    code = 411


class NotLoginException(Error):
    code = 412


class UserNotExistOrPasswordErrorException(Error):
    code = 413


class InvalidDataException(Error):
    code = 414
