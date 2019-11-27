
class Token():
    _access_token = None
    _servicename = None

    def __init__(self, servicename: str, access_token: str):
        self._servicename = servicename
        self._access_token = access_token

    @property
    def servicename(self):
        return self._servicename

    @property
    def access_token(self):
        return self._access_token

    def __str__(self):
        return f"Token: {self}, Servicename: {self.servicename}, Access-Token: {self.access_token}"


class Oauth2Token(Token):
    """
    Represents a token object.
    """

    _refresh_token = None
    _exiration_date = None

    def __init__(self, servicename: str, access_token: str, refresh_token: str):
        super(Oauth2Token, self).__init__(servicename, access_token)
        self._refresh_token = refresh_token
        self._exiration_date = ""

    @property
    def refresh_token(self):
        return self._refresh_token

    def __str__(self):
        text = super(Oauth2Token, self).__str__()
        return f"{text}, Refresh-Token: {self.refresh_token}"

    def __eq__(self, other):
        return (
            isinstance(other, (Token)) and
            self.servicename == other.servicename and
            self.access_token == other.access_token and
            self.refresh_token == other.refresh_token
        )
