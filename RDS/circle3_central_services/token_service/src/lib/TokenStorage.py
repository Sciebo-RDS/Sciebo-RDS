from Exceptions._StorageException import UserExistsAlreadyError, UserNotExistsError, UserHasTokenAlreadyError
from .User import User
from .Token import Token


class TokenStorage():
    """
    Represents a Safe for Tokens
    """

    _storage = None
    
    def __init__(self):
        self._storage = {}

    def addUser(self, user: User):
        """
        Add user to the _storage. 

        If a User with the same username already exists, it raises UserExistsAlreadyError.
        """

        if not user in self._storage:
            userdict = {}
            userdict["user"] = user
            userdict["tokens"] = []
            self._storage[user.username] = userdict

        else:
            raise UserExistsAlreadyError(self, user)

    def addTokenToUser(self, user: User, token: Token, Force: bool = False):
        """
        Add a token to an existing user. If user not exists already in the _storage, it raises an UserNotExistsError.
        If token was added to user specific _storage, then it returns `True`.

        If a token is there for the same token provider, then a UserHasTokenAlreadyError.

        Use `Force` Parameter (boolean) to create User, if not already exists and overwrite any existing Token.
        """

        if not user in self._storage:
            if Force:
                self._storage[user.username] = user
            else:
                raise UserNotExistsError(self, user)

        if token in self._storage[user]["tokens"] and not Force:
            raise UserHasTokenAlreadyError(self, user, token)

        self._storage[user.username]["tokens"].append(token)
        return True

    def __str__(self):
        string = "Storage:\n"

        for user in self._storage:
            string += f'- User {user["user"]}'

            for token in user["tokens"]:
                string += f"-- Token {token}"

        return string
