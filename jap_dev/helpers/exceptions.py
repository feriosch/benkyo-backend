class GeneralException(Exception):
    def __init__(self, message, code):
        self._message = message
        self._code = code

    @property
    def message(self):
        return self._message

    @property
    def code(self):
        return self._code


class UnauthorizedException(GeneralException):
    def __init__(self, message):
        super().__init__(message, 401)


class BadRequestException(GeneralException):
    def __init__(self, message):
        super().__init__(message, 400)
