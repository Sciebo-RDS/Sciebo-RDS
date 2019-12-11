import requests
import os
import json
from flask import jsonify
from lib.Service import Service
from lib.User import User
from lib.Token import Token
import Util
from lib.Exceptions.ServiceExceptions import *

func = [Util.initialize_object_from_json, Util.initialize_object_from_dict]
load_object = Util.try_function_on_dict(func)


class TokenService():
    def __init__(self, address=None):
        self.address = address if address is not None else os.getenv(
            "CENTRAL-SERVICE_TOKEN-STORAGE")
        if self.address is None:
            # TODO: load address from oai file
            # https://raw.githubusercontent.com/Sciebo-RDS/Sciebo-RDS/master/RDS/circle3_central_services/token_service/central-service_token-storage.yml
            pass

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

        Raise an `UserAlreadyRegisteredError`, if user already registered.

        Returns True for succes or raise an error.
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
        response = requests.delete(
            f"{self.address}/user/{user.username}/token/{token.servicename}")
        data = response.json()
        if response.status_code is not 200:
            if "error" in data:
                if data["error"] == "TokenNotExists":
                    raise TokenNotFoundError(token)
                if data["error"] == "UserNotExistsError":
                    raise UserNotFoundError(user)

            raise Exception(data)

        return data["success"]
