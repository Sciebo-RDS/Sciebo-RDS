from lib.Service import Service
from lib.User import User
from lib.Token import Token


class ServiceNotFoundError(Exception):
    """
    Represents an error, when a service was not found.
    """

    def __init__(self, service: Service, msg=None):
        if msg is None:
            msg = f"{service} not found"

        super(ServiceNotFoundError, self).__init__(msg)
        self.service = service

class ProjectNotCreatedError(Exception):
    """
    Represents an error, when a project in service could not created.
    """

    def __init__(self, service: Service, msg=None):
        if msg is None:
            msg = f"project in {service} could not be created."

        super(ProjectNotCreatedError, self).__init__(msg)
        self.service = service


class TokenNotFoundError(Exception):
    """
    Represents an error, when a token was not found.
    """

    def __init__(self, token: Token, msg=None):
        if msg is None:
            msg = f"{token} not found"

        super(TokenNotFoundError, self).__init__(msg)
        self.token = token


class UserNotFoundError(Exception):
    """
    Represents an error, when an user was not found.
    """

    def __init__(self, user: User, msg=None):
        if msg is None:
            msg = f"{user} not found"

        super(UserNotFoundError, self).__init__(msg)
        self.user = user


class UserHasTokenAlreadyError(Exception):
    """
    Represents an error, when a user has already a token for the service.
    """

    def __init__(self, user: User, token: Token, msg=None):
        if msg is None:
            msg = f"{user} has {token} already."

        super(UserHasTokenAlreadyError, self).__init__(msg)
        self.user = user
        self.token = token


class UserAlreadyRegisteredError(UserNotFoundError):
    """
    Represents an error, when a user-id is already registered.
    """

    def __init__(self, user: User, msg=None):
        if msg is None:
            msg = f"{user} already registered."

        super(UserAlreadyRegisteredError, self).__init__(msg)
        self.user = user


class CodeNotExchangeable(Exception):
    """
    Represents an error, when a given code for the oauth workflow could not be exchanged against an access_token.
    """

    def __init__(self, code, service, msg=None):
        if msg is None:
            msg = f"Code {code} coult not be exchanged for {service}"

        super(CodeNotExchangeable, self).__init__(msg)
        self.code = code
        self.service = service
