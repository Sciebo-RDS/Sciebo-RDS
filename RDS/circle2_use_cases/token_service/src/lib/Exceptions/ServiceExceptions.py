from lib.Service import Service
from lib.User import User
from lib.Token import Token


class ServiceNotFoundError(Exception):
    def __init__(self, service: Service, msg=None):
        if msg is None:
            msg = f"{service} not found"

        super(ServiceNotFoundError, self).__init__(msg)
        self.service = service


class TokenNotFoundError(Exception):
    def __init__(self, token: Token, msg=None):
        if msg is None:
            msg = f"{token} not found"

        super(TokenNotFoundError, self).__init__(msg)
        self.token = token


class UserNotFoundError(Exception):
    def __init__(self, user: User, msg=None):
        if msg is None:
            msg = f"{user} not found"

        super(UserNotFoundError, self).__init__(msg)
        self.user = user


class UserHasTokenAlreadyError(Exception):
    def __init__(self, user: User, token: Token, msg=None):
        if msg is None:
            msg = f"{user} has {token} already."

        super(UserHasTokenAlreadyError, self).__init__(msg)
        self.user = user
        self.token = token


class UserAlreadyRegisteredError(UserNotFoundError):
    def __init__(self, user: User, msg=None):
        if msg is None:
            msg = f"{user} already registered."

        super(UserAlreadyRegisteredError, self).__init__(msg)
        self.user = user
