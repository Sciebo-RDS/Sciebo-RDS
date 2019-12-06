import datetime
import json


class Token():
    """
    This token represents a simple password.
    """

    _access_token = None
    _servicename = None

    def __init__(self, servicename: str, access_token: str):
        self.check_string(servicename, "servicename")
        self.check_string(access_token, "access_token")

        self._servicename = servicename
        self._access_token = access_token

    def check_string(self, obj: str, string: str):
        if not obj:
            raise ValueError(f"{string} cannot be an empty string.")

    @property
    def servicename(self):
        return self._servicename

    @property
    def access_token(self):
        return self._access_token

    def __str__(self):
        return {"Servicename": self.servicename, "Access-Token": self.access_token}.__str__()

    def __eq__(self, other):
        """
        Returns True, if this object and other object have the same servicename. Otherwise false.
        """
        return (
            isinstance(other, (Token)) and
            self.servicename == other.servicename
        )

    def __json__(self):
        """
        Returns this object as a dict.
        """

        data = {
            "type": self.__class__.__name__,
            "data": self.to_dict()
        }
        data = json.dumps(data)
        return data

    def to_dict(self):
        data = {
            "servicename": self._servicename,
            "access_token": self._access_token
        }

        return data

    @classmethod
    def from_json(cls, tokenStr: str):
        """
        Returns a token object from a json string.
        """

        data = tokenStr
        while type(data) is not dict:  # FIX for bug: JSON.loads sometimes returns a string
            data = json.loads(data)

        if "type" in data and str(data["type"]).endswith("Token") and "data" in data:
            data = data["data"]
            if "access_token" in data and "servicename" in data:
                return Token(data["servicename"], data["access_token"])

        raise ValueError("not a valid token json string.")

    @classmethod
    def from_dict(cls, tokenDict: dict):
        """
        Returns a token object from a dict.
        """

        return Token(tokenDict["servicename"], tokenDict["access_token"])


class OAuth2Token(Token):
    """
    Represents a token object.
    """

    _refresh_token = None
    _expiration_date = None

    def __init__(self, servicename: str, access_token: str, refresh_token: str = "",
                 expiration_date: datetime.datetime = None):
        super(OAuth2Token, self).__init__(servicename, access_token)

        if expiration_date is None:
            expiration_date = datetime.datetime.now()

        # remove check for empty string for refresh_token, because it could be an authorization_token
        # self.check_string(refresh_token, "refresh_token")

        if refresh_token:
            self._refresh_token = refresh_token
            self._expiration_date = expiration_date

    @property
    def refresh_token(self):
        return self._refresh_token

    @property
    def expiration_date(self):
        return self._expiration_date

    def __str__(self):
        text = super(OAuth2Token, self).__str__()
        return f"{text}, Refresh-Token: {self.refresh_token}, exp-date: {self.expiration_date}"

    @classmethod
    def from_token(cls, token: Token, refresh_token: str = "", expiration_date: datetime.datetime = None):
        """
        Convert the given Token into an oauth2token.
        """
        if expiration_date is None:
            expiration_date = datetime.datetime.now()

        return cls(token.servicename, token.access_token, refresh_token, expiration_date)

    def __eq__(self, obj):
        """
        Check, if tokens are equal. You must not check if the refresh or access_tokens are equal,
        because they could be changed already. Only servicename is relevant.
        """
        return (
            super(OAuth2Token, self).__eq__(obj)
        )

    def __json__(self):
        """
        Returns this object as a json string.
        """

        data = super(OAuth2Token, self).__json__()
        data = json.loads(data)

        data["type"] = self.__class__.__name__
        data["data"].update(self.to_dict())

        return json.dumps(data)

    def to_dict(self):
        data = super(OAuth2Token, self).to_dict()
        data["refresh_token"] = self._refresh_token
        data["expiration_date"] = str(self._expiration_date)

        return data

    @classmethod
    def from_json(cls, tokenStr: str):
        """
        Returns an oauthtoken object from a json string.
        """

        data = tokenStr
        while type(data) is not dict:  # FIX for bug: JSON.loads sometimes returns a string
            data = json.loads(data)

        token = super(OAuth2Token, cls).from_json(tokenStr)

        if "type" in data and str(data["type"]).endswith("OAuth2Token"):
            data = data["data"]
            if "refresh_token" in data and "expiration_date" in data:
                return cls.from_token(token, data["refresh_token"], data["expiration_date"])

        raise ValueError("not a valid token json string.")

    @classmethod
    def from_dict(cls, tokenDict: dict):
        """
        Returns an oauthtoken object from dict.
        """
        token = super(OAuth2Token, cls).from_dict(tokenDict)

        return OAuth2Token.from_token(token, tokenDict["refresh_token"], tokenDict["expiration_date"])
