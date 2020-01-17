from ..User import User
from ..Storage import Storage
from ..Token import Token, OAuth2Token
from ..Service import Service


class UserExistsAlreadyError(Exception):
    def __init__(self, storage: Storage, user: User, msg=None):
        if msg is None:
            msg = f"{user} already exists in {storage}"

        super(UserExistsAlreadyError, self).__init__(msg)
        self.user = user
        self.storage = storage


class UserNotExistsError(UserExistsAlreadyError):
    def __init__(self, storage: Storage, user: User, msg=None):
        if msg is None:
            msg = f"{user} not exist in {storage}"

        super(UserNotExistsError, self).__init__(storage, user, msg)


class UserHasTokenAlreadyError(UserExistsAlreadyError):
    def __init__(self, storage: Storage, user: User, token: Token, msg=None):
        if msg is None:
            msg = f"{user} has already {token.service} in Storage"

        super(UserHasTokenAlreadyError, self).__init__(storage, user, msg)

class TokenNotForUser(Exception):
    def __init__(self, storage: Storage, user: User, token: Token, msg=None):
        if msg is None:
            msg = f"{user} not qualified for {token} in Storage"

        super(TokenNotExistsError, self).__init__(msg)
        self.user = user
        self.token = token
        self.storage = storage


class TokenNotExistsError(Exception):
    def __init__(self, storage: Storage, user: User, token: Token, msg=None):
        if msg is None:
            msg = f"{Token} not exists in {storage} for user {user}"

        super(TokenNotExistsError, self).__init__(msg)
        self.user = user
        self.token = token
        self.storage = storage
