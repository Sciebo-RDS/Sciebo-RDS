from .User import User
from .Token import Token, OAuth2Token
from .Service import Service, OAuth2Service
import logging
import requests


class Storage():
    """
    Represents a Safe for Tokens
    """

    _storage = None

    def __init__(self):
        self._storage = {}

    def getUser(self, user_id: str):
        if user_id in self._storage:
            return self._storage[user_id]["data"]

        from .Exceptions.StorageException import UserNotExistsError
        raise UserNotExistsError(self, User(user_id))

    def getToken(self, user_id: str, token_id: int = None):
        if user_id in self._storage:
            tokens = self._storage[user_id]["tokens"]
            if token_id is not None:
                try:
                    tokens = tokens[token_id]
                except:
                    raise ValueError("Token_id not found")
            return tokens

        from .Exceptions.StorageException import UserNotExistsError
        raise UserNotExistsError(self, User(user_id))

    def getUsers(self):
        return [val["data"] for val in self._storage.values()]

    def getTokens(self):
        return [token for val in self._storage.values() for token in val["tokens"]]

    def addUser(self, user: User):
        """
        Add user to the storage.

        If a User with the same username already exists, it raises UserExistsAlreadyError.
        """

        if not user.username in self._storage:
            self.internal_addUser(user)

        else:
            from .Exceptions.StorageException import UserExistsAlreadyError
            raise UserExistsAlreadyError(self, user)

    def removeUser(self, user: User):
        """
        Remove given user from storage.

        If user not in storage, it raises an UserNotExistsError.
        """

        self.internal_removeUser(user)

    def internal_removeUser(self, user: User):
        """
        Remove a user to _storage.

        This is an internal function. Please look at the external one.
        """

        if not user.username in self._storage:
            from .Exceptions.StorageException import UserNotExistsError
            raise UserNotExistsError(self, user)

        del self._storage[user.username]

    def removeToken(self, user: User, token: Token):
        """
        Remove a token from user.
        """

        self.internal_removeToken(user, token)

    def internal_removeToken(self, user: User, token: Token):
        """
        Remove a token from user.

        This is an internal function. Please look at the external one.
        """

        if not user.username in self._storage:
            from .Exceptions.StorageException import UserNotExistsError
            raise UserNotExistsError(self, user)

        if not token in self._storage[user.username]["tokens"]:
            from .Exceptions.StorageException import TokenNotExists
            raise TokenNotExists(self, user, token)

        index = self._storage[user.username]["tokens"].index(token)
        del self._storage[user.username]["tokens"][index]

    def internal_addUser(self, user: User):
        """
        Add a user to the _storage.

        This is an internal function. Please take a look to the external one.
        """
        userdict = {}
        userdict["data"] = user
        userdict["tokens"] = []
        self._storage[user.username] = userdict

    def addTokenToUser(self, token: Token, user: User, Force: bool = False):
        """
        Add a token to an existing user. If user not exists already in the _storage, it raises an UserNotExistsError.
        If token was added to user specific storage, then it returns `True`.

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
            # token not found in storage, so we can add it here.
            self._storage[user.username]["tokens"].append(token)

        return True

    def refresh_service(self, service: Service):
        """
        Refresh all tokens, which corresponds to given service.

        Returns True, if one or more Tokens were found in the storage to refresh.
        """

        return self.internal_refresh_services([service])

    def refresh_services(self, services: list):
        """
        Refresh all tokens, which corresponds to given list of services.

        Returns True, if one or more Tokens were found in the storage to refresh.
        """
        return self.internal_refresh_services(services)

    def internal_refresh_services(self, services: list):
        """
        *Only for internal use. Do not use it in another class.*

        Refresh all tokens, which corresponds to given list of services.

        Returns True, if one or more Tokens were found in the storage to refresh.
        """

        found = False

        # iterate over users
        for user in self._storage.values():
            index = None

            # iterate over tokens from current user
            for token in user["tokens"]:
                # find the corresponding service
                try:
                    index = self.internal_find_service(
                        token.servicename, services)
                except ValueError as e:
                    # there was no one, so we can finish here, cause token cannot be refresh
                    continue

                # save for faster usage
                service = services[index]

                found = True
                # if service or token is not oauth, it has not any refresh mechanism, so we can finish here.
                if not isinstance(service, (OAuth2Service)) or not isinstance(token, (OAuth2Token)):
                    continue

                # refresh token
                from .Exceptions.ServiceExceptions import OAuth2UnsuccessfulResponseError, TokenNotValidError
                try:
                    service.refresh(token, user["data"])
                except TokenNotValidError as e:
                    logging.getLogger().error(e)
                except OAuth2UnsuccessfulResponseError as e:
                    logging.getLogger().error(e)
                except requests.exceptions.RequestException as e:
                    logging.getLogger().error(e)

        return found

    def internal_find_service(self, servicename: str, services: list):
        """
        Tries to find the given servicename in the list of services. 
        Returns the index of the first found service with equal servicename.

        Otherwise raise an ValueError.

        Doesn't check, if services are duplicated.
        """
        for index, service in enumerate(services):
            if service.servicename == servicename:
                return index

        raise ValueError("Servicename {} not found in services {}.".format(
            servicename, ";".join(map(str, services))))

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
