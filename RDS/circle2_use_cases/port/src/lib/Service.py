from lib.Token import Token, OAuth2Token
from lib.User import User
from urllib.parse import urlparse, urlunparse
import requests
import json
from datetime import datetime, timedelta
from typing import Union
import logging

logger = logging.getLogger()


class Service:
    """
    Represents a service, which can be used in RDS.
    This service only allows username:password authentication.
    """

    _servicename = None
    _implements = None

    def __init__(self, servicename: str, implements: list = None):
        self.check_string(servicename, "servicename")

        self._servicename = servicename

        self._implements = implements
        if implements is None:
            self._implements = []

    @property
    def servicename(self):
        return self._servicename

    @property
    def implements(self):
        return self._implements

    def check_string(self, obj: str, string: str):
        if not obj:
            raise ValueError(f"{string} cannot be an empty string.")

    def is_valid(self, token: Token, user: User):
        pass

    def __eq__(self, obj):
        return isinstance(obj, (Service)) and self.servicename == obj.servicename

    def __str__(self):
        return json.dumps(self)

    def to_json(self):
        """
        Returns this object as a json string.
        """

        data = {"type": self.__class__.__name__, "data": self.to_dict()}
        return data

    def to_dict(self):
        """
        Returns this object as a dict.
        """

        data = {"servicename": self._servicename, "implements": self._implements}

        return data

    @classmethod
    def from_json(cls, serviceStr: str):
        """
        Returns an service object from a json string.
        """

        data = serviceStr
        while (
            type(data) is not dict
        ):  # FIX for bug: JSON.loads sometimes returns a string
            data = json.loads(data)

        if "type" in data and str(data["type"]).endswith("Service") and "data" in data:
            data = data["data"]
            if "servicename" in data:
                return Service(data["servicename"], data.get("implements"))

        raise ValueError("not a valid service json string.")

    @classmethod
    def from_dict(cls, serviceDict: dict):
        """
        Returns an service object from a dict string.
        """

        try:
            return Service(serviceDict["servicename"], serviceDict.get("implements"))
        except:
            raise ValueError("not a valid service dict")

    @staticmethod
    def init(obj: Union[str, dict]):
        """
        Returns a Service or oauthService object for json String or dict.
        """
        if isinstance(obj, (Service, OAuth2Service)):
            return obj

        if not isinstance(obj, (str, dict)):
            raise ValueError("Given object not from type str or dict.")

        from Util import try_function_on_dict

        load = try_function_on_dict(
            [
                OAuth2Service.from_json,
                Service.from_json,
                OAuth2Service.from_dict,
                Service.from_dict,
            ]
        )
        return load(obj)


class OAuth2Service(Service):
    """
    Represents an OAuth2 service, which can be used in RDS.
    This service enables the oauth2 workflow.
    """

    _authorize_url = None
    _refresh_url = None
    _client_id = None
    _client_secret = None

    def __init__(
        self,
        servicename: str,
        authorize_url: str,
        refresh_url: str,
        client_id: str,
        client_secret: str,
        implements: list = None,
    ):
        super(OAuth2Service, self).__init__(servicename, implements)

        self.check_string(authorize_url, "authorize_url")
        self.check_string(refresh_url, "refresh_url")
        self.check_string(client_id, "client_id")
        self.check_string(client_secret, "client_secret")

        self._authorize_url = self.parse_url(authorize_url)
        self._refresh_url = self.parse_url(refresh_url)

        self._client_id = client_id
        self._client_secret = client_secret

    def parse_url(self, url: str):
        u = urlparse(url)
        if not u.netloc:
            raise ValueError("URL needs a protocoll")

        # check for trailing slash for url
        if u.path and u.path[-1] == "/":
            u = u._replace(path=u.path[:-1])

        return u

    def refresh(self, token: OAuth2Token):
        """
        Refresh the given oauth2 token for specified user.
        """

        if not isinstance(token, OAuth2Token):
            logger.debug("call refresh on non oauth token.")
            raise ValueError("parameter token is not an oauthtoken.")

        import os

        data = {
            "grant_type": "refresh_token",
            "refresh_token": token.refresh_token,
            "redirect_uri": "{}/redirect".format(
                os.getenv("FLASK_HOST_ADDRESS", "http://localhost:8080")
            ),
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }

        logger.debug(f"send data {data}")

        req = requests.post(
            self.refresh_url,
            data=data,
            auth=(self.client_id, self.client_secret),
            verify=(os.environ.get("VERIFY_SSL", "True") == "True"),
        )

        logger.debug(f"status code: {req.status_code}")

        if req.status_code >= 400:
            data = json.loads(req.text)

            if "error" in data:
                error_type = data["error"]

                if error_type == "invalid_request":
                    from .Exceptions.ServiceException import OAuth2InvalidRequestError

                    raise OAuth2InvalidRequestError()
                elif error_type == "invalid_client":
                    from .Exceptions.ServiceException import OAuth2InvalidClientError

                    raise OAuth2InvalidClientError()
                elif error_type == "invalid_grant":
                    from .Exceptions.ServiceException import OAuth2InvalidGrantError

                    raise OAuth2InvalidGrantError()
                elif error_type == "unauthorized_client":
                    from .Exceptions.ServiceException import OAuth2UnauthorizedClient

                    raise OAuth2UnauthorizedClient()
                elif error_type == "unsupported_grant_type":
                    from .Exceptions.ServiceException import OAuth2UnsupportedGrantType

                    raise OAuth2UnsupportedGrantType()

            from .Exceptions.ServiceException import OAuth2UnsuccessfulResponseError

            raise OAuth2UnsuccessfulResponseError()

        data = json.loads(req.text)

        logger.debug(f"response data {data}")

        """ obsolete
        if not data["user_id"] == self.client_id:
            from .Exceptions.ServiceException import Token.TokenNotValidError
            raise Token.TokenNotValidError(
                self, token, "User-ID in refresh response not equal to authenticated user.")
        """

        date = datetime.now() + timedelta(seconds=data["expires_in"])
        new_token = OAuth2Token(
            token.user, token.service, data["access_token"], data["refresh_token"], date
        )
        logger.debug(f"new token {new_token}")
        return new_token

    @property
    def refresh_url(self):
        return urlunparse(self._refresh_url)

    @property
    def authorize_url(self):
        return urlunparse(self._authorize_url)

    @property
    def client_id(self):
        return self._client_id

    @property
    def client_secret(self):
        return self._client_secret

    @classmethod
    def from_service(
        cls,
        service: Service,
        authorize_url: str,
        refresh_url: str,
        client_id: str,
        client_secret: str,
    ):
        """
        Converts the given Service to an oauth2service.
        """
        return cls(
            service.servicename,
            authorize_url,
            refresh_url,
            client_id,
            client_secret,
            service.implements,
        )

    def __eq__(self, obj):
        return super(OAuth2Service, self).__eq__(obj) or (
            isinstance(obj, (OAuth2Service))
            and self.refresh_url == obj.refresh_url
            and self.authorize_url == obj.authorize_url
            and self.client_id == obj.client_id
            and self.client_secret == obj.client_secret
        )

    def to_json(self):
        """
        Returns this object as a json string.
        """

        data = super(OAuth2Service, self).to_json()

        data["type"] = self.__class__.__name__
        data["data"].update(self.to_dict())

        return data

    def to_dict(self):
        """
        Returns this object as a dict.
        """
        data = super(OAuth2Service, self).to_dict()
        data["authorize_url"] = self.authorize_url
        data["refresh_url"] = self.refresh_url
        data["client_id"] = self._client_id
        data["client_secret"] = self._client_secret

        return data

    @classmethod
    def from_json(cls, serviceStr: str):
        """
        Returns an oauthservice object from a json string.
        """

        data = serviceStr
        while (
            type(data) is not dict
        ):  # FIX for bug: JSON.loads sometimes returns a string
            data = json.loads(data)

        service = super(OAuth2Service, cls).from_json(serviceStr)

        try:
            data = data["data"]
            return cls.from_service(
                service,
                data["authorize_url"],
                data["refresh_url"],
                data["client_id"],
                data["client_secret"],
            )
        except:
            raise ValueError("not a valid oauthservice json string.")

    @classmethod
    def from_dict(cls, serviceDict: dict):
        """
        Returns an oauthservice object from a dict.
        """

        service = super(OAuth2Service, cls).from_dict(serviceDict)

        try:
            return OAuth2Service.from_service(
                service,
                serviceDict["authorize_url"],
                serviceDict["refresh_url"],
                serviceDict["client_id"],
                serviceDict["client_secret"],
            )
        except:
            raise ValueError("not a valid oauthservice dict.")
