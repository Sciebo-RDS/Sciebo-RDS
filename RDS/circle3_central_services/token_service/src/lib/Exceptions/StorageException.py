from ..User import User
from ..Storage import Storage
from ..Token import Token

class UserExistsAlreadyError(Exception):
    def __init__(self, storage: Storage, user: User, msg=None):
        if msg is None:
            msg = f"User {user} already exists in Storage {storage}"
        
        super(UserExistsAlreadyError, self).__init__(msg)
        self.user = user
        self.storage = storage

class UserNotExistsError(UserExistsAlreadyError):
    def __init__(self, storage: Storage, user: User, msg=None):
        if msg is None:
            msg = f"User {user} not exist in Storage {storage}"
        
        super(UserNotExistsError, self).__init__(msg)

class UserHasTokenAlreadyError(UserExistsAlreadyError):
    def __init__(self, storage: Storage, user: User, token: Token, msg=None):
        if msg is None:
            msg = f"User {user} has already {token} in Storage {storage}"
        
        super(UserHasTokenAlreadyError, self).__init__(msg)
