from lib.User import User
from lib.Token import Token, OAuth2Token
from lib.Service import Service, OAuth2Service
from typing import Union
from lib.Exceptions.ServiceException import ServiceExistsAlreadyError, ServiceNotExistsError

import logging
import requests

logger = logging.getLogger()


class Storage():
    """
    Represents a Safe for Tokens.
    """

    _storage = None
    _services = None

    def __init__(self):
        self._storage = {}
        self._services = []

    def getUsers(self):
        """
        Returns a list of all registered users.
        """
        return [val["data"] for val in self._storage.values()]

    def getUser(self, user_id: str):
        """
        Returns the user with user_id.

        Raise a `UserNotExistsError`, if user not found.
        """
        if user_id in self._storage:
            return self._storage[user_id]["data"]

        from .Exceptions.StorageException import UserNotExistsError
        raise UserNotExistsError(self, User(user_id))

    def getTokens(self, user_id: Union[str, User] = None):
        """
        Returns a list of all managed tokens. 

        If user_id (String or User) was given, then the tokens are filtered to this user.

        Raise a UserNotExistsError, if the given user not exists.
        """

        if user_id is None:
            return [
                token for val in self._storage.values()
                for token in val["tokens"]
            ]

        if not isinstance(user_id, (str, User)):
            raise ValueError("user_id is not string or User.")

        if isinstance(user_id, User):
            user_id = user_id.username

        if user_id in self._storage:
            tokens = self._storage[user_id]["tokens"]
            return tokens

        from .Exceptions.StorageException import UserNotExistsError
        raise UserNotExistsError(self, User(user_id))

    def getToken(self, user_id: Union[str, User], token_id: int):
        """
        Returns only the token with token_id from user_id (String or User).

        Raise `ValueError` if token_id not found and `UserNotExistsError` if user_id was not found.
        """

        if not isinstance(user_id, (str, User)):
            raise ValueError("user_id is not string or User.")

        if isinstance(user_id, User):
            user_id = user_id.username

        if user_id in self._storage:
            tokens = self._storage[user_id]["tokens"]
            try:
                tokens = tokens[token_id]
            except:
                raise ValueError("Token_id not found")

            return tokens

        from .Exceptions.StorageException import UserNotExistsError
        raise UserNotExistsError(self, User(user_id))

    def getServices(self):
        """
        Returns a list of all registered services.
        """
        return self._services

    def getService(self, service: Union[str, Service], index: bool = False):
        """
        Returns the service object with the given servicename. If not found, returns None

        This function can be used to check, if an object is already a member of the list of services.

        Set parameter `index` to True to get the index as the second return value in tuple.
        """

        if not isinstance(service, (str, Service)):
            raise ValueError("given parameter not string or service.")

        serviceStr = service.servicename if isinstance(service,
                                                       (Service)) else service

        logger.debug("Start searching service {}".format(service))
        for k, svc in enumerate(self._services):
            if svc.servicename == serviceStr:
                logger.debug("Found service {}".format(svc))
                logger.debug("Return index? {}, index: {}".format(
                    index is not None, k))

                return (svc, k) if index is True else svc

        return (None, None) if index is True else None

    def addService(self, service: Service, Force=False):
        """
        Add the given service to the list of services.

        Returns True if success.
        Otherwise raises a `ServiceExistsAlreadyError` if there is already a service with the same name.

        To force an update, you have to set the parameter `Force` to True.

        Raise an error, if parameter not a service object.
        """
        if not isinstance(service, (Service, OAuth2Service)):
            raise ValueError("parameter not a service object.")

        svc, index = self.getService(service, index=True)
        if svc is not None:
            if Force is True:
                self._services[index] = service
                return True

            from lib.Exceptions.ServiceException import ServiceExistsAlreadyError
            raise ServiceExistsAlreadyError(service)

        self._services.append(service)
        return True

    def removeService(self, service: Union[str, Service]):
        """
        Removes the service with servicename.

        Returns True if a service was found and removed. Otherwise false.
        """

        if not isinstance(service, str) and not isinstance(service, Service):
            raise ValueError("given parameter not string or service.")

        _, index = self.getService(service, index=True)

        if index is not None and isinstance(index, int):
            del self._services[index]
            return True

        return False

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

        try:
            self.internal_find_service(token.servicename, self._services)
        except ValueError:
            raise ServiceNotExistsError(Service(token.servicename))

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

    def refresh_services(self, services: list = None):
        """
        Refresh all tokens, which corresponds to given list of services.

        If no services were given, it will be used the stored one.

        Returns True, if one or more Tokens were found in the storage to refresh.
        """

        if services is None:
            return self.internal_refresh_services(self._services)

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
                    index = self.internal_find_service(token.servicename,
                                                       services)
                except ValueError as e:
                    # there was no one, so we can finish here, cause token cannot be refresh
                    continue

                # save for faster usage
                service = services[index]

                found = True
                # if service or token is not oauth, it has not any refresh mechanism, so we can finish here.
                if not isinstance(service, (OAuth2Service)) or not isinstance(
                        token, (OAuth2Token)):
                    continue

                # refresh token
                from .Exceptions.ServiceException import OAuth2UnsuccessfulResponseError, TokenNotValidError
                try:
                    new_token = service.refresh(token)
                    self.addTokenToUser(new_token, user["data"], Force=True)
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

        Returns the index of the *first* found service with equal servicename.

        Otherwise raise an ValueError.
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
