from .Token import Token


class Service():
    """
    Represents a service, which can be used in RDS.
    Servicename needs to be unique!
    """

    _servicename = None

    def __init__(self, servicename: str):
        self._servicename = servicename

    @property
    def servicename(self):
        return self._servicename


class OAuth2Service(Service):
    """
    Represents an OAuth2 Service
    """

    _refresh_url = None
    _authorize_url = None
    _client_id = None
    _client_secret = None

    def __init__(self, servicename: str, refresh_url: str, authorize_url: str, client_id: str, client_secret: str):
        super(OAuth2Service, self).__init__(servicename)
        self._refresh_url = refresh_url
        self._authorize_url = authorize_url
        self._client_id = client_id
        self._client_secret = client_secret

    def refresh_token(self, token: Token):
        """
        Refresh the given oauth2 token.
        """

        pass

    @property
    def refresh_url(self):
        return self._refresh_url

    @property
    def authorize_url(self):
        return self._authorize_url

    @property
    def client_id(self):
        return self._client_id

    @property
    def client_secret(self):
        return self._client_secret
