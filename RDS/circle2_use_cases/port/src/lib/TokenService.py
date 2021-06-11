import requests
import os
import json
from flask import jsonify
from RDS import BaseService, LoginService, OAuth2Service, User, LoginToken, OAuth2Token, Token, Util
from lib.Exceptions.ServiceException import *
import jwt
import datetime
import secrets
import logging
from typing import Union

logger = logging.getLogger()


def get_port_string(name):
    service = name
    if not "port-" in name:
        service = "port-{}".format(name)

    return "http://circle1-{}".format(service.lower())


class TokenService:
    # static
    secret = (
        os.getenv("TOKENSERVICE_STATE_SECRET")
        if os.getenv("TOKENSERVICE_STATE_SECRET") is not None
        else secrets.token_urlsafe()
    )
    address = os.getenv("CENTRAL_SERVICE_TOKEN_STORAGE")

    _services = None

    def __init__(self, testing=False):
        if testing:
            self.address = testing

        self._services = []

    def getOAuthURIForService(self, service: BaseService) -> str:
        """
        Returns authorize-url as `String` for the given service.
        """

        if not service in self._services:
            self.refreshService(service)

            if not service in self._services:
                raise ServiceNotFoundError(service)

        return getattr(service, "authorize_url", None)

    def refreshServices(self) -> bool:
        response = requests.get(
            f"{self.address}/service",
            verify=(os.environ.get("VERIFY_SSL", "True") == "True"),
        )
        data = response.json()
        services = [Util.getServiceObject(svc) for svc in data["list"]]

        if len(services) is not len(self._services):
            self._services = services
            return True
        return False

    def refreshService(self, service: Union[str, BaseService]) -> bool:
        try:
            servicename = service.servicename
        except:
            servicename = service

        response = requests.get(
            f"{self.address}/service/{servicename}",
            verify=(os.environ.get("VERIFY_SSL", "True") == "True"),
        )

        if response.status_code != 200:
            try:
                raise ServiceNotFoundError(service)
            except:
                raise ServiceNotFoundError(BaseService(
                    servicename=servicename, implements=["metadata"]))

        svc = Util.getServiceObject(response.json())

        if not svc in self._services:
            self._services.append(svc)

        return svc

    def getAllOAuthURIForService(self) -> list:
        """
        Returns a `list` of `String` which represents all authorize-urls for registered services.
        """

        self.refreshServices()

        return [getattr(svc, "authorize_url", None) for svc in self._services]

    def getService(self, servicename: str, clean=False, informations=False) -> BaseService:
        """
        Returns a dict like self.getAllServices, but for only a single servicename (str).

        If clean is True, it returns the service object, otherwise it returns the a state object for registration process.
        If informations is True, it returns a field "informations" which stored informations about service
        """

        svc = None

        for service in self._services:
            if servicename == service.servicename.lower():
                svc = service
                break

        if svc is None:
            svc = self.refreshService(servicename)

        if clean:
            return svc

        dictWithState = self.internal_getDictWithStateFromService(svc)

        if informations:
            dictWithState["informations"] = self.getInformations(svc)

        return dictWithState

    def getAllServices(self, clean=False, informations=False) -> list:
        """
        Returns a `list` of `dict` which represents all registered services.

        `dict` use struct:
        {
            "jwt": string (json / jwt)
        }

        jwt is base64 encoded, separated by dots, payload struct:
        {
            "servicename"
            "authorize_url"
            "date"
        }
        """

        self.refreshServices()

        services = self._services

        if clean:
            return services

        result_list = []

        for svc in services:
            dictWithState = self.internal_getDictWithStateFromService(svc)

            if informations:
                dictWithState["informations"] = self.getInformations(svc)

            result_list.append(dictWithState)

        logger.warning(result_list)

        return result_list

    def getInformations(self, svc: BaseService) -> dict:
        informations = svc.to_dict()

        try:
            del informations["client_secret"]
        except:
            pass

        return informations

    def internal_getDictWithStateFromService(self, service: BaseService) -> dict:
        """
        **Internal use only**

        Returns a service as jwt encoded dict.
        """
        new_obj = {}

        date = str(datetime.datetime.now())

        data = {
            "servicename": service.servicename,
            "authorize_url": getattr(service, "authorize_url", None),
            "date": date,
            "implements": service.implements,
        }
        state = jwt.encode(data, self.secret, algorithm="HS256")
        logger.info("state: {}, data: {}".format(state, data))

        new_obj["jwt"] = state
        logger.info("return: {}".format(new_obj))

        return new_obj

    def getAllServicesForUser(self, user: User) -> list:
        """
        Returns a `list` for all services which the user has registered a token for.
        """
        response = requests.get(
            f"{self.address}/user/{user.username}/token",
            verify=(os.environ.get("VERIFY_SSL", "True") == "True"),
        )
        data = response.json()

        # TODO: adjust to oai spec

        services = []
        try:
            for index, l in enumerate(data["list"]):
                token = Util.getTokenObject(l)
                services.append(
                    {
                        "id": index,
                        "servicename": token.servicename,
                        "access_token": token.access_token,
                        "projects": self.getProjectsForToken(token),
                        "implements": token._service.implements,
                        "informations": self.getInformations(token.service)
                    }
                )
        except Exception as e:
            logger.error(e)
            raise UserNotFoundError(user)

        return services

    def getProjectsForToken(self, token: Token) -> list:
        """
        Returns a `list` with all projects for given service and user.
        """

        if token.access_token == "---":
            return []

        port = get_port_string(token.servicename)
        if self.address.startswith("http://localhost"):
            port = self.address

        req = requests.get(
            f"{port}/metadata/project",
            json=Util.parseToken(token),
            verify=(os.environ.get("VERIFY_SSL", "True") == "True"),
        )

        if req.status_code >= 300:
            return []

        return req.json()

    def createProjectForUserInService(self, user: User, service: BaseService) -> int:
        """
        Create a project in service, which the token is for.
        Returns the id for the new created project. If something went wrong, raise an ProjectNotCreated
        """

        token = self.getTokenForServiceFromUser(service, user)
        data = Util.parseToken(token)

        port = get_port_string(service.servicename)
        if self.address.startswith("http://localhost"):
            port = self.address

        req = requests.post(
            "{}/metadata/project".format(port),
            json=data,
            verify=(os.environ.get("VERIFY_SSL", "True") == "True"),
        )

        if req.status_code < 300:
            project = req.json()
            return project.get("projectId"), project

        raise ProjectNotCreatedError(service)

    def removeProjectForUserInService(
        self, user: User, service: BaseService, project_id: int
    ) -> bool:
        """
        Remove the project with id for user in service.
        Returns True when success. Otherwise False.
        """
        token = self.getTokenForServiceFromUser(service, user)

        data = Util.parseToken(token)

        port = get_port_string(service.servicename)
        if self.address.startswith("http://localhost"):
            port = self.address

        req = requests.delete(
            "{}/metadata/project/{}".format(port, project_id),
            json=data,
            verify=(os.environ.get("VERIFY_SSL", "True") == "True"),
        )

        return req.status_code == 204

    def removeService(self, service: BaseService) -> bool:
        """
        Remove a registered service.

        Returns `True` for success.

        Raise a `ServiceNotFoundError`, if service was not found.

        **Notice**: This function is currently discussed for removal.
        """
        pass

    def addUser(self, user: User) -> bool:
        """
        Adds the given user to the token storage.

        Returns `True` for success.

        Raise an `UserAlreadyRegisteredError`, if user already registered.
        """
        response = requests.post(
            f"{self.address}/user",
            data=json.dumps(user),
            verify=(os.environ.get("VERIFY_SSL", "True") == "True"),
        )
        if response.status_code != 200:
            raise UserAlreadyRegisteredError(user)

        data = response.json()
        return data["success"]

    def removeUser(self, user: User) -> bool:
        """
        Remove the given user from the token storage.

        Returns `True` for success.

        Raise an `UserNotfoundError`, if user was not found.
        """

        response = requests.delete(
            f"{self.address}/user/{user.username}",
            verify=(os.environ.get("VERIFY_SSL", "True") == "True"),
        )
        if response.status_code != 200:
            raise UserNotFoundError(user)

        data = response.json()
        return data["success"]

    def addTokenToUser(self, token: Token, user: User) -> bool:
        """
        Adds the given token to user.

        Returns `True` for success.

        Raise an `UserNotFoundError`, if user not found.
        Raise a `ServiceNotFoundError`, if service not found.
        """

        headers = {
            'content-type': 'application/json'
        }

        response = requests.post(
            f"{self.address}/user/{user.username}/token",
            data=json.dumps(token),
            headers=headers,
            verify=(os.environ.get("VERIFY_SSL", "True") == "True"),
        )
        data = response.json()

        if response.status_code >= 300:
            if "error" in data:
                if data["error"] == "UserHasTokenAlreadyError":
                    raise UserHasTokenAlreadyError(user, token)

                if data["error"] == "UserNotExistsError":
                    raise UserNotFoundError(user)

                if data["error"] == "ServiceNotFoundError":
                    raise ServiceNotFoundError(token.service)

            raise Exception(data)

        return data["success"]

    def removeTokenFromUser(self, token: Token, user: User) -> bool:
        """
        Removes given token from user.

        Returns `True` for success.

        Raise an `UserNotFoundError`, if user not found.
        Raise an `TokenNotFoundError`, if token not found for user.
        """

        return self.internal_removeTokenForStringFromUser(token.service, user)

    def internal_removeTokenForStringFromUser(
        self, service: BaseService, user: User
    ) -> bool:
        response = requests.delete(
            f"{self.address}/user/{user.username}/token/{service.servicename}",
            verify=(os.environ.get("VERIFY_SSL", "True") == "True"),
        )
        data = response.json()
        if response.status_code != 200:
            if "error" in data:
                if data["error"] == "TokenNotExistsError":
                    raise TokenNotFoundError(Token(user, service, "NOT_USED"))
                if data["error"] == "UserNotExistsError":
                    raise UserNotFoundError(user)
                if data["error"] == "ServiceNotExistsError":
                    raise ServiceNotFoundError(service)

            raise Exception(data)

        return data["success"]

    def getTokenForServiceFromUser(self, service: BaseService, user: User) -> Token:
        """
        Returns the token from type Token (struct: servicename: str, access_token: str) for given service from given user.

        Raise ServiceNotExistsError, if no token for service was found.
        """
        response = requests.get(
            f"{self.address}/user/{user.username}/token/{service.servicename}",
            verify=(os.environ.get("VERIFY_SSL", "True") == "True"),
        )

        data = response.json()
        while type(data) is not dict:
            data = json.loads(data)

        if response.status_code != 200:
            if "error" in data:
                if data["error"] == "TokenNotExistsError":
                    raise TokenNotFoundError(Token(user, service, "NOT_USED"))
                if data["error"] == "UserNotExistsError":
                    raise UserNotFoundError(user)
                if data["error"] == "ServiceNotExistsError":
                    raise ServiceNotFoundError(service)
            raise Exception(data)

        token = Util.getTokenObject(data)

        if isinstance(token.service, OAuth2Service):
            token.service._client_secret = ""

        if isinstance(token, OAuth2Token):
            token._refresh_token = ""

        return token

    def removeTokenForServiceFromUser(self, service: BaseService, user: User) -> bool:
        """
        Remove the token for service from user.

        Raise ServiceNotFoundError, if no token for service was found.
        """
        try:
            return self.internal_removeTokenForStringFromUser(service, user)
        except TokenNotFoundError:
            raise ServiceNotFoundError(service)

    def exchangeAuthCodeToAccessToken(
        self, code: str, service: Union[str, OAuth2Service], user: str
    ) -> OAuth2Token:
        """Exchanges the given `code` by the given `service`

        Args:
            code (str): The oauth2 exchange code.
            service (Union[str, OAuth2Service]): The servicename, which the code is for.
            user (str): The username, which wants to exchange the code.

        Raises:
            ValueError: The servicename was not valid.
            ServiceNotFoundError: The servicename was not found.
            CodeNotExchangeable: Code was not exchangeable.

        Returns:
            OAuth2Token: The oauth2 token with access- and refresh-tokens.
        """

        if not isinstance(service, (str, OAuth2Service)):
            raise ValueError(
                f"Given service argument {service} is not a valid string or OAuth2Service."
            )

        if type(service) is str:
            service = self.getService(service, clean=True)

            if not isinstance(service, OAuth2Service):
                raise ServiceNotFoundError(
                    service,
                    msg=f"No oauthservice for {service} found, so we cannot exchange code.",
                )

        # FIXME: RDS_OAUTH_REDIRECT_URI needs to be set in dockerfile
        body = {
            "grant_type": "authorization_code",
            "code": code,
            "client_id": service.client_id,
            "client_secret": service.client_secret,
            "redirect_uri": os.getenv(
                "RDS_OAUTH_REDIRECT_URI", "http://localhost:3000/redirect"
            ),
        }

        logger.info(f"request body: {body}")

        response = requests.post(
            f"{service.refresh_url}",
            data=body,
            auth=(service.client_id, service.client_secret),
            verify=(os.environ.get("VERIFY_SSL", "True") == "True"),
        )

        logger.info(f"response body: {response.text}")

        if response.status_code != 200:
            raise CodeNotExchangeable(code, service, msg=response.text)

        response_with_access_token = response.json()

        # FIXME: need here some solution, where the response will be evaluated by the corresponding port
        try:
            # owncloud / oauth2 spec
            user_id = response_with_access_token["user_id"]
        except:
            # zenodo specific
            #user_id = response_with_access_token["user"]["id"]
            pass
        # TODO: add here more cloud storage provider for username

        # if no user was set, then this token will be used for superuser
        if user is None:
            user = user_id

        access_token = response_with_access_token["access_token"]
        refresh_token = response_with_access_token["refresh_token"]
        exp_date = datetime.datetime.now() + datetime.timedelta(
            seconds=response_with_access_token["expires_in"]
        )

        oauthtoken = OAuth2Token(
            User(user), service, access_token, refresh_token, exp_date
        )

        # save the access_token in tokenStorage
        logger.info(f"request oauthtoken body: {oauthtoken}")
        headers = {"Content-type": "application/json"}

        # adjustment to new model in c3 token storage

        response = requests.post(
            f"{self.address}/user/{user}/token",
            data=json.dumps(oauthtoken),
            headers=headers,
            verify=(os.environ.get("VERIFY_SSL", "True") == "True"),
        )
        logger.info(f"response oauthtoken body: {response.text}")

        if response.status_code >= 300:
            raise CodeNotExchangeable(
                response.status_code, service, msg=response.text
            )

        return oauthtoken


def addTokenToUser(
    self, token: Union[str, Token]
) -> bool:
    """Add the given Token to user.

    Args:
        token: The token, which should be added.
        user (str): The username, which sould get the token.

    Raises:
        ValueError: The servicename was not valid.
        ServiceNotFoundError: The servicename was not found.

    Returns:
        Bool: True, when everything works. Otherwise false.
    """

    # save the access_token in tokenStorage
    logger.info(f"request token body: {token}")
    headers = {"Content-type": "application/json"}

    response = requests.post(
        f"{self.address}/user/{token.user.username}/token",
        data=json.dumps(token),
        headers=headers,
        verify=(os.environ.get("VERIFY_SSL", "True") == "True"),
    )
    logger.info(f"response oauthtoken body: {response.text}")

    return (response.status_code >= 300)
