from ..User import User
from ..Storage import Storage
from ..Token import Token, OAuth2Token

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
            msg = f"{user} has already {token.servicename} in Storage"
        
        super(UserHasTokenAlreadyError, self).__init__(storage, user, msg)

class TokenNotExists(Exception):
    def __init__(self, storage: Storage, user: User, token: Token, msg=None):
        if msg is None:
            msg = f"{Token} not exists in {storage} for user {user}"
        
        super(TokenNotExists, self).__init__(msg)
        self.user = user
        self.token = token
        self.storage = storage