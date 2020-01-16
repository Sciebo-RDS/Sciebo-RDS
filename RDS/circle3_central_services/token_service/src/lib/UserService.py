from lib.User import User
from lib.Service import Service, OAuth2Service
from Util import try_function_on_dict
from typing import Union
import json


class UserService():
    """
    Represents an association for an user object with a service object.
    """

    def __init__(self, user: User, service: Service, service_user_id: str, service_access_token: str, service_refresh_token: str):
        if not isinstance(user, User):
            raise ValueError("invalid parameter user")
        if not isinstance(service, (OAuth2Service, Service)):
            raise ValueError("invalid parameter service")
        if not isinstance(service_user_id, str):
            raise ValueError("invalid parameter service_user_id")
        if not isinstance(service_access_token, str):
            raise ValueError("invalid parameter service_access_token")
        if not isinstance(service_refresh_token, str):
            raise ValueError("invalid parameter service_refresh_token")

        if not service_user_id or not service_access_token or not service_refresh_token:
            raise ValueError("some parameter were empty")

        self._user = user
        self._service = service
        self._service_user_id = service_user_id
        self._service_access_token = service_access_token
        self._service_refresh_token = service_refresh_token

    @property
    def user(self):
        return self._user

    @property
    def service(self):
        return self._service

    @property
    def service_user_id(self): pass

    @property
    def service_access_token(self):
        return self._service_access_token

    @property
    def service_refresh_token(self):
        return self._service_refresh_token

    def to_json(self):
        data = {
            "type": self.__class__.__name__,
            "data": self.to_dict()
        }

        return data

    def to_dict(self):
        data = {
            "user": self._user,
            "service": self._service,
            "service_user_id": self._service_user_id,
            "service_access_token": self._service_access_token,
            "service_refresh_token": self._service_refresh_token
        }

        return data

    @classmethod
    def from_json(cls, jsonStr: str):
        data = jsonStr
        while type(data) is not dict:  # FIX for bug: JSON.loads sometimes returns a string
            data = json.loads(data)

        if "type" in data and str(data["type"]).endswith("UserService"):
            data = data["data"]
            return cls.from_dict(data)

        raise ValueError("not a valid UserService object json string.")

    @classmethod
    def from_dict(cls, userServiceDict: dict):
        if "user" in userServiceDict and "service" in userServiceDict and \
                "service_user_id" in userServiceDict and "service_access_token" in userServiceDict and "service_refresh_token" in userServiceDict:
            return cls(
                User.init(userServiceDict.get("user")),
                Service.init(userServiceDict.get("service")),
                userServiceDict.get("service_user_id"),
                userServiceDict.get("service_access_token"),
                userServiceDict.get("service_refresh_token")
            )

        raise ValueError("Given an invalid dict.")

    @staticmethod
    def init(obj: Union[str, dict]):
        if isinstance(obj, (UserService)):
            return obj

        if not isinstance(obj, (str, dict)):
            raise ValueError("Given object not from type str or dict.")

        from Util import try_function_on_dict

        if isinstance(obj, str):
            load = try_function_on_dict([UserService.from_json])
            return load(obj)

        load = try_function_on_dict([UserService.from_dict])
        return load(obj)

    def __eq__(self, obj):
        if not isinstance(obj, (UserService)):
            return False

        return (
            self._user is obj._user and
            self._service is obj._service and
            self._service_user_id is obj._service_user_id and
            self._service_access_token is obj._service_access_token and
            self._service_refresh_token is obj._service_refresh_token
        )
