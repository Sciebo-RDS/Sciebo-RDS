from lib.User import User
from lib.Token import Token, OAuth2Token
from lib.Service import Service, OAuth2Service
from typing import Union
from lib.Exceptions.ServiceException import ServiceExistsAlreadyError, ServiceNotExistsError

import logging
import requests
import os

logger = logging.getLogger()


class Storage():
    """
    Represents a Safe for Tokens.
    """

    _storage = None
    _services = None

    def __init__(self):
        if os.getenv("RDS_OAUTH_REDIRECT_URI") is not None:
            from redis_pubsub_dict import RedisDict
            from rediscluster import StrictRedisCluster
            # runs in RDS ecosystem, use redis as backend
            rc = StrictRedisCluster(startup_nodes=[{"host": "redis", "port": "6379"}])
            self._storage = RedisDict(rc, 'tokenstorage_storage')
            self._services = RedisDict(rc, 'tokenstorage_services')

            def append(self, value):
                self[self.size] = value

            self._services.append = append
        else:
            self._storage = {}
            self._services = []

    @property
    def users(self):
        return [val["data"] for val in self.storage.values()]

    @property
    def storage(self):
        return self._storage
    
    @property
    def services(self):
        try:
            return self._services.values()
        except:
            return self._services

    @property
    def tokens(self):
        return [token for val in self.storage.values() for token in val["tokens"]]

    def getUsers(self):
        """
        Returns a list of all registered users.
        """
        return self.users

    def getUser(self, user_id: str):
        """
        Returns the user with user_id.

        Raise a `UserNotExistsError`, if user not found.
        """

        if user_id in self._storage:
            return self._storage[user_id]["data"]

        from .Exceptions.StorageException import UserNotExistsError
        raise UserNotExistsError(self, User(user_id))

    def getTokens(self, user: Union[str, User] = None):
        """
        Returns a list of all managed tokens. 

        If user_id (String or User) was given, then the tokens are filtered to this user.

        Raise a UserNotExistsError, if the given user not exists.
        """

        if user is None:
            return self.tokens

        if not isinstance(user, (str, User)):
            raise ValueError("paremeter user is not string or User.")

        if not isinstance(user, User):
            for u in self.users:
                if u.username == user:
                    user = u
                    break

        if user in self.users:
            tokens = self._storage[user.username]["tokens"]
            return tokens

        from .Exceptions.StorageException import UserNotExistsError
        raise UserNotExistsError(self, user)

    def getToken(self, user_id: Union[str, User], token_id: Union[str, int]):
        """
        Returns only the token with token_id (str or int) from user_id (Username as string or User).

        token_id should be the servicename or the id for token in list.

        Raise `ValueError` if token_id not found and `UserNotExistsError` if user_id was not found.
        """

        if not isinstance(user_id, (str, User)):
            raise ValueError("user_id is not string or User.")

        logger.debug("got user {}, token {}".format(user_id, token_id))

        if isinstance(user_id, User):
            user = user_id
        else:
            user = self.getUser(user_id)

        try:
            logger.debug("try to convert")
            token_id = int(token_id)

            logger.debug("use user {}, token {}".format(user, token_id))
            logger.debug("length token {}".format(len(self.tokens)))

            if len(self.tokens) > token_id:
                token = self.storage[user.username]["tokens"][token_id]
                logger.debug("found token {}".format(token))
                return token

        except:
            logger.debug("try to find id by bruteforce")
            for key, val in self.storage.items():
                if not key == user.username:
                    continue

                for token in val["tokens"]:
                    if token.servicename == token_id:
                        logger.debug("found token {}".format(token))
                        return token

        from .Exceptions.StorageException import UserNotExistsError
        raise UserNotExistsError(self, user)

    def getServices(self):
        """
        Returns a list of all registered services.
        """
        return self.services

    def getService(self, service: Union[str, Service], index: bool = False):
        """
        Returns the service object with the given servicename. If not found, returns None

        This function can be used to check, if an object is already a member of the list of services.

        Set parameter `index` to True to get the index as the second return value in tuple.
        """

        if not isinstance(service, (str, Service)):
            raise ValueError("given parameter not string or service.")

        if not isinstance(service, (Service)):
            service = Service(service)

        try:
            k = self.internal_find_service(service.servicename, self.services)
            svc = self._services[k]
            return (svc, k) if index is True else svc
        except:
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
        for i, val in enumerate(self.services):
            if val.servicename == service:
                index = i
                break

        if index is None:
            return False

        del self._services[index]

        for val in self._storage.values():
            for token in reversed(val.get("tokens")):
                if token.service is service:
                    val.get("tokens").remove(token)

        return True

    def addUser(self, user: User):
        """
        Add user to the storage.

        If a User with the same username already exists, it raises UserExistsAlreadyError.
        """

        if not user in self.users:
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
        Remove a user to tokens.

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

        If the first token will be deleted, it is the master token / login token, 
        which was used to enable and RDS use this token for frontend actions. 
        So we can assume, that the user wants to revoke all access through RDS.
        To accomplish this, we remove all data for this user in token storage.
        """

        logger.debug("remove token: user {}, token {}".format(user, token))

        if not user.username in self._storage:
            from .Exceptions.StorageException import UserNotExistsError
            raise UserNotExistsError(self, user)

        try:
            for index, crnt in enumerate(self._storage[user.username]["tokens"]):
                if token.servicename == crnt.servicename:
                    logger.debug("found")
                    if index == 0:
                        del self._storage[user.username]
                    else:
                        del self._storage[user.username]["tokens"][index]
                    break
        except ValueError:
            from .Exceptions.StorageException import TokenNotExistsError
            raise TokenNotExistsError(self, user, token)

    def internal_addUser(self, user: User):
        """
        Add a user to storage as superuser.

        This is an internal function. Please take a look to the external one.
        """

        # check if this id is a superuser
        if not user.username in self._storage:
            self._storage[user.username] = {
                "data": user,
                "tokens": []
            }

        else:
            from lib.Exceptions.StorageException import UserExistsAlreadyError
            raise UserExistsAlreadyError(self, user)

    def addTokenToUser(self, token: Token, user: User = None, Force: bool = False):
        """
        Add a token to an existing user. If user not exists already in the tokens, it raises an UserNotExistsError.
        If token was added to user specific storage, then it returns `True`.

        If a token is there for the same token provider, then a UserHasTokenAlreadyError.

        Use `Force` Parameter (boolean) to create User, if not already exists and overwrite any existing Token, too.

        If user parameter not provided, it takes the user from token as superuser.
        """

        logger.info(f"Try to find service {token.servicename}")
        try:
            self.internal_find_service(token.servicename, self.services)
        except ValueError:
            raise ServiceNotExistsError(Service(token.servicename))
        logger.debug("service found")

        # if user is None, user wants to add a superuser or refresh its token
        if user is None:
            user = token.user

        if not user.username in self._storage:
            logger.debug("user not found")
            if Force:
                self.internal_addUser(user)
                logger.debug(
                    f"add user {user} with force, because it does not exist in storage already.")
            else:
                from lib.Exceptions.StorageException import UserNotExistsError
                raise UserNotExistsError(self, user)

        try:
            index = self._storage[user.username]["tokens"].index(token)

            """
            obsolete since model update
            if user is not None:
                from .Exceptions.StorageException import TokenNotForUser
                raise TokenNotForUser(self, user, token)
            """

            if Force:
                self._storage[user.username]["tokens"][index] = token
                logger.debug(f"overwrite token for user {user}")

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
            return self.internal_refresh_services(self.services)

        return self.internal_refresh_services(services)

    def internal_refresh_services(self, services: list):
        """
        *Only for internal use. Do not use it in another class.*

        Refresh all tokens, which corresponds to given list of services.

        Returns True, if one or more Tokens were found in the storage to refresh.
        """

        found = False

        # iterate over tokens
        tokens = [
            (userdata["data"],  token)
            for userdata in self._storage.values()
            for token in userdata["tokens"]
        ]

        for user, token in tokens:
            if not isinstance(token, OAuth2Token) or not isinstance(token.service, OAuth2Service):
                continue

            # refresh token
            from .Exceptions.ServiceException import OAuth2UnsuccessfulResponseError, TokenNotValidError
            try:
                new_token = token.refresh()
                self.addTokenToUser(new_token, user, Force=True)
                found = True

            except TokenNotValidError as e:
                logging.getLogger().error(e)
            except OAuth2UnsuccessfulResponseError as e:
                logging.getLogger().error(e)
            except requests.exceptions.RequestException as e:
                logging.getLogger().error(e)
            except Exception as e:
                return False

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
        import json
        return json.dumps(self.storage)

        """
        def __str__(self):
        string = "\n"

        for index, value in enumerate(self.tokens):
            string += f'- \'User\' {value.user}\n'
            string += f'-- \'Data\': {value}\n'

            token_string = self.getTokens(value.user)

            token_string = ",".join(map(str, token_string))
            token_string = f"[{token_string}]"

            string += f'-- \'Tokens\': {token_string}\n'

        return string
        """
