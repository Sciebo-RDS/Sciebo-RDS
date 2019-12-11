import requests
import os
import json
from flask import jsonify
from lib.Service import Service, OAuth2Service
from lib.User import User
from lib.Token import Token
import Util
from lib.Exceptions.ServiceExceptions import *
import jwt
import datetime
import secrets

func = [Util.initialize_object_from_json, Util.initialize_object_from_dict]
load_object = Util.try_function_on_dict(func)


class TokenService():
    secret = secrets.token_urlsafe()

    def __init__(self, address=None):
        self.address = address if address is not None else os.getenv(
            "CENTRAL-SERVICE_TOKEN-STORAGE")
        if self.address is None:
            # TODO: load address from oai file
            # https://raw.githubusercontent.com/Sciebo-RDS/Sciebo-RDS/master/RDS/circle3_central_services/token_service/central-service_token-storage.yml
            pass

        secret = os.getenv("TOKENSERVICE_STATE_SECRET")
        if secret is not None:
            self.secret = secret

    def getOAuthURIForService(self, service: Service) -> str:
        """
        Returns authorize-url as `String` for the given service.
        """
        response = requests.get(
            f"{self.address}/service/{service.servicename}")

        if response.status_code is not 200:
            raise ServiceNotFoundError(service)

        data = response.text
        service = load_object(data)
        return service.authorize_url

    def getAllOAuthURIForService(self) -> list:
        """
        Returns a `list` of `String` which represents all authorize-urls for registered services.
        """
        response = requests.get(f"{self.address}/service")
        data = response.json()

        return [load_object(svc).authorize_url for svc in data["list"]]

    def getAllServices(self) -> list:
        """
        Returns a `list` of `dict` which represents all registered services.

        `dict` use struct:
        {
            "servicename": string,
            "authorize_url": string,
            "date": datetime
        }
        """
        response = requests.get(f"{self.address}/service")
        data = response.json()

        result_list = []
        for svc in data["list"]:
            new_obj = {}

            obj = load_object(svc)
            if type(obj) is not OAuth2Service:
                continue

            date = str(datetime.datetime.now())

            data = {
                "servicename": obj.servicename,
                "authorize_url": obj.authorize_url,
                "date": date
            }
            state = jwt.encode(data, self.secret, algorithm='HS256')

            new_obj["servicename"] = obj.servicename
            new_obj["authorize_url"] = obj.authorize_url
            new_obj["jwt"] = state

            result_list.append(new_obj)

        return result_list

    def getAllServicesForUser(self, user: User) -> list:
        """
        Returns a `list` for all services which the user has registered a token for.
        """
        response = requests.get(f"{self.address}/user/{user.username}/token")
        data = response.json()

        services = []
        for l in data["list"]:
            token = load_object(l)
            services.append(token.servicename)

        return services

    def removeService(self, service: Service) -> bool:
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
        response = requests.post(f"{self.address}/user", data=json.dumps(user))
        if response.status_code is not 200:
            raise UserAlreadyRegisteredError(user)

        data = response.json()
        return data["success"]

    def removeUser(self, user: User) -> bool:
        """
        Remove the given user from the token storage.

        Returns `True` for success.

        Raise an `UserNotfoundError`, if user was not found.
        """

        response = requests.delete(f"{self.address}/user/{user.username}")
        if response.status_code is not 200:
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

        response = requests.post(
            f"{self.address}/user/{user.username}/token", data=json.dumps(token))
        data = response.json()

        if response.status_code is not 200:
            if "error" in data:
                if data["error"] == "UserHasTokenAlreadyError":
                    raise UserHasTokenAlreadyError(user, token)

                if data["error"] == "UserNotExistsError":
                    raise UserNotFoundError(user)

                if data["error"] == "ServiceNotFoundError":
                    raise ServiceNotFoundError(Service(token.servicename))

            raise Exception(data)

        return data["success"]

    def removeTokenFromUser(self, token: Token, user: User) -> bool:
        """
        Removes given token from user.

        Returns `True` for success.

        Raise an `UserNotFoundError`, if user not found.
        Raise an `TokenNotFoundError`, if token not found for user.
        """

        return self.internal_removeTokenForStringFromUser(token.servicename, user)

    def internal_removeTokenForStringFromUser(self, tokenStr: str, user: User) -> bool:
        response = requests.delete(
            f"{self.address}/user/{user.username}/token/{tokenStr}")
        data = response.json()
        if response.status_code is not 200:
            if "error" in data:
                if data["error"] == "TokenNotExistsError":
                    raise TokenNotFoundError(Token(tokenStr, "NOT_USED"))
                if data["error"] == "UserNotExistsError":
                    raise UserNotFoundError(user)
                if data["error"] == "ServiceNotExistsError":
                    raise ServiceNotFoundError(Service(tokenStr))

            raise Exception(data)

        return data["success"]

    def getTokenForServiceFromUser(self, service: Service, user: User) -> bool:
        """
        Returns the token from type Token (struct: servicename: str, access_token: str) for given service from given user.

        Raise ServiceNotExistsError, if no token for service was found.
        """
        response = requests.get(
            f"{self.address}/user/{user.username}/token/{service.servicename}")
        data = response.json()

        if response.status_code is not 200:
            if "error" in data:
                if data["error"] == "TokenNotExistsError":
                    raise TokenNotFoundError(
                        Token(service.servicename, "NOT_USED"))
                if data["error"] == "UserNotExistsError":
                    raise UserNotFoundError(user)
                if data["error"] == "ServiceNotExistsError":
                    raise ServiceNotFoundError(service)
            raise Exception(data)

        # remove refresh token
        data["type"] = "Token"
        token = load_object(data)
        return token

    def removeTokenForServiceFromUser(self, service: Service, user: User) -> bool:
        """
        Remove the token for service from user.

        Raise ServiceNotFoundError, if no token for service was found.
        """
        try:
            return self.internal_removeTokenForStringFromUser(service.servicename, user)
        except TokenNotFoundError:
            raise ServiceNotFoundError(service)
