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

    _tokens = None
    _services = None
    _users = None

    def __init__(self):
        self._tokens = []
        self._services = []
        self._users = []

    @property
    def _storage(self):
        """
        This method generates a dict from the new data model for older code.
        """

        storage = {}
        for u in self._users:
            storage[u.username] = {
                "data": u,
                "tokens": self.getTokens(u)
            }

        return storage

    def getUsers(self):
        """
        Returns a list of all registered users.
        """
        return self._users

    def getUser(self, user_id: str):
        """
        Returns the user with user_id.

        Raise a `UserNotExistsError`, if user not found.
        """
        for u in self._users:
            if u.username == user_id:
                return u

        from .Exceptions.StorageException import UserNotExistsError
        raise UserNotExistsError(self, User(user_id))

    def getTokens(self, user: Union[str, User] = None):
        """
        Returns a list of all managed tokens. 

        If user_id (String or User) was given, then the tokens are filtered to this user.

        Raise a UserNotExistsError, if the given user not exists.
        """

        if user is None:
            return self._tokens

        if not isinstance(user, (str, User)):
            raise ValueError("paremeter user is not string or User.")

        if not isinstance(user, User):
            for u in self._users:
                if u.username == user:
                    user = u
                    break

        if user in self._users:
            tokens = [
                token for token in self._tokens if token.user is user
            ]
            return tokens

        from .Exceptions.StorageException import UserNotExistsError
        raise UserNotExistsError(self, user)

    def getToken(self, user_id: Union[str, User], token_id: Union[str, int]):
        """
        Returns only the token with token_id (str or int) from user_id (String or User).

        token_id should be the servicename or the id for token in list.

        Raise `ValueError` if token_id not found and `UserNotExistsError` if user_id was not found.
        """

        if not isinstance(user_id, (str, User)):
            raise ValueError("user_id is not string or User.")

        if isinstance(user_id, User):
            user = user_id
        else:
            user = self.getUser(user_id)

        try:
            token_id = int(token_id)
        except:
            for i, t in enumerate(self._tokens):
                if t.servicename == token_id:
                    token_id = i
                    break


        if len(self._tokens) > token_id:
            return self._tokens[token_id]

        from .Exceptions.StorageException import UserNotExistsError
        raise UserNotExistsError(self, user)

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

        if not isinstance(service, (str, Service)):
            raise ValueError("given parameter not string or service.")

        if isinstance(service, Service):
            service = service.servicename

        index = None
        for i, val in enumerate(self._services):
            if val.servicename == service:
                index = i
                break

        if index is None:
            return False

        self._services.pop(index)
        # remove all corresponding tokens
        self._tokens = [
            token for token in self._tokens if token.service.servicename is not service
        ]
        return True

    def addUser(self, user: User):
        """
        Add user to the storage.

        If a User with the same username already exists, it raises UserExistsAlreadyError.
        """

        if not user in self._users:
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
        Remove a user to _tokens.

        This is an internal function. Please look at the external one.
        """

        if not user in self._users:
            from .Exceptions.StorageException import UserNotExistsError
            raise UserNotExistsError(self, user)

        self._users.remove(user)

        self._tokens = [
            token for token in self._tokens if token.user is not user
        ]

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

        if not user in self._users:
            from .Exceptions.StorageException import UserNotExistsError
            raise UserNotExistsError(self, user)

        try:
            index = self._tokens.index(token)
        except ValueError:
            from .Exceptions.StorageException import TokenNotExists
            raise TokenNotExists(self, user, token)

        del self._tokens[index]

    def internal_addUser(self, user: User):
        """
        Add a user to the _tokens.

        This is an internal function. Please take a look to the external one.
        """
        self._users.append(user)

    def addTokenToUser(self, token: Token, user: User = None, Force: bool = False):
        """
        Add a token to an existing user. If user not exists already in the _tokens, it raises an UserNotExistsError.
        If token was added to user specific storage, then it returns `True`.

        If a token is there for the same token provider, then a UserHasTokenAlreadyError.

        Use `Force` Parameter (boolean) to create User, if not already exists and overwrite any existing Token, too.
        """

        logger.info(f"Try to find service {token.servicename}")
        try:
            self.internal_find_service(token.servicename, self._services)
        except ValueError:
            raise ServiceNotExistsError(Service(token.servicename))
        logger.debug("service found")

        # ignore user parameter
        user = token.user

        logger.debug(f"user {user}")

        if user is not None and not user in self._users:
            logger.debug("user not found")
            if Force:
                self.internal_addUser(user)
                logger.debug(
                    f"add user {user} with force, because he does not exist in storage already.")
            else:
                from .Exceptions.StorageException import UserNotExistsError
                raise UserNotExistsError(self, user)

        try:
            index = self._tokens.index(token)

            """
            obsolete since model update
            if user is not None:
                from .Exceptions.StorageException import TokenNotForUser
                raise TokenNotForUser(self, user, token)
            """

            if Force:
                self._tokens[index] = token
                logger.debug(f"overwrite token for user {user}")

            else:
                from .Exceptions.StorageException import UserHasTokenAlreadyError
                raise UserHasTokenAlreadyError(self, user, token)

        except ValueError:
            # token not found in storage, so we can add it here.
            self._tokens.append(token)

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

        # iterate over tokens
        for token in self._tokens:
            if not isinstance(token, OAuth2Token) or not isinstance(token.service, OAuth2Service):
                continue

            # refresh token
            from .Exceptions.ServiceException import OAuth2UnsuccessfulResponseError, TokenNotValidError
            try:
                new_token = token.service.refresh(token)
                self.addTokenToUser(new_token, token.user, Force=True)
                found = True
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
        if not isinstance(services, list):
            raise ValueError("Services is not of type list.")

        for index, service in enumerate(services):
            if service.servicename == servicename:
                return index

        raise ValueError("Service {} not found in services {}.".format(
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

        """
        def __str__(self):
        string = "\n"

        for index, value in enumerate(self._tokens):
            string += f'- \'User\' {value.user}\n'
            string += f'-- \'Data\': {value}\n'

            token_string = self.getTokens(value.user)

            token_string = ",".join(map(str, token_string))
            token_string = f"[{token_string}]"

            string += f'-- \'Tokens\': {token_string}\n'

        return string
        """
