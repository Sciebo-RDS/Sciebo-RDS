from .User import User
from .Token import Token


class Storage():
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

        if not user.username in self._storage:
            self.internal_addUser(user)

        else:
            from .Exceptions.StorageException import UserExistsAlreadyError
            raise UserExistsAlreadyError(self, user)

    def internal_addUser(self, user: User):
        userdict = {}
        userdict["data"] = user
        userdict["tokens"] = []
        self._storage[user.username] = userdict

    def addTokenToUser(self, user: User, token: Token, Force: bool = False):
        """
        Add a token to an existing user. If user not exists already in the _storage, it raises an UserNotExistsError.
        If token was added to user specific _storage, then it returns `True`.

        If a token is there for the same token provider, then a UserHasTokenAlreadyError.

        Use `Force` Parameter (boolean) to create User, if not already exists and overwrite any existing Token.
        """

        if not user.username in self._storage:
            if Force:
                self.internal_addUser(user)
            else:
                from .Exceptions.StorageException import UserNotExistsError
                raise UserNotExistsError(self, user)

        try:
            index = self._storage[user.username]["tokens"].index(token)

            if Force:
                self._storage[user.username]["tokens"][index] = token

            else:
                from .Exceptions.StorageException import UserHasTokenAlreadyError
                raise UserHasTokenAlreadyError(self, user, token)
        except ValueError:
            # token not found in storage
            print("Token not found")
            self._storage[user.username]["tokens"].append(token)

        return True

    def __str__(self):
        string = "\n"

        for key, value in self._storage.items():
            string += f'- \'User\' {key}\n'
            string += f'-- \'Data\': {value["data"]}\n'

            token_string = []

            for token in value["tokens"]:
                token_string.append(str(token))

            token_string = ",".join(token_string)
            token_string = f"[{token_string}]"

            string += f'-- \'Tokens\': {token_string}\n'

        return string
