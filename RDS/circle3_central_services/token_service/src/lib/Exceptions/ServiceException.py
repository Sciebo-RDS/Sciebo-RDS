from ..Service import Service
from ..Token import Token, OAuth2Token
from ..User import User


class TokenNotValidError(Exception):
    def __init__(self, service: Service, token: Token, msg=None):
        if msg is None:
            msg = f"{token} not valid for {service}"

        super(TokenNotValidError, self).__init__(msg)
        self.token = token
        self.service = service

# messages taken from https://tools.ietf.org/html/rfc6749#section-5.2


class OAuth2UnsuccessfulResponseError(Exception):
    def __init__(self, msg=None):
        if msg is None:
            msg = f"An unsuccessful response was received."

        super(OAuth2UnsuccessfulResponseError, self).__init__(msg)


class OAuth2InvalidRequestError(OAuth2UnsuccessfulResponseError):
    def __init__(self, msg=None):
        if msg is None:
            msg = """The request is missing a required parameter, includes an
               unsupported parameter value (other than grant type),
               repeats a parameter, includes multiple credentials,
               utilizes more than one mechanism for authenticating the
               client, or is otherwise malformed."""

        super(OAuth2InvalidRequestError, self).__init__(msg)


class OAuth2InvalidClientError(OAuth2UnsuccessfulResponseError):
    def __init__(self, msg=None):
        if msg is None:
            msg = """Client authentication failed(e.g., unknown client, no client authentication included, 
            or unsupported authentication method).  The authorization server MAY
            return an HTTP 401 (Unauthorized) status code to indicate which HTTP authentication schemes are supported.  If the
            client attempted to authenticate via the \"Authorization\" request header field, the authorization server MUST
            respond with an HTTP 401 (Unauthorized) status code and include the \"WWW-Authenticate\" response header field
            matching the authentication scheme used by the client."""

        super(OAuth2InvalidClientError, self).__init__(msg)


class OAuth2InvalidGrantError(OAuth2UnsuccessfulResponseError):
    def __init__(self, msg=None):
        if msg is None:
            msg = """The provided authorization grant(e.g., authorization code, resource owner credentials) 
            or refresh token is invalid, expired, revoked, does not match the redirection
            URI used in the authorization request, or was issued to another client."""

        super(OAuth2InvalidGrantError, self).__init__(msg)


class OAuth2UnauthorizedClient(OAuth2UnsuccessfulResponseError):
    def __init__(self, msg=None):
        if msg is None:
            msg = "The authenticated client is not authorized to use this authorization grant type."

        super(OAuth2UnauthorizedClient, self).__init__(msg)


class OAuth2UnsupportedGrantType(OAuth2UnsuccessfulResponseError):
    def __init__(self, msg=None):
        if msg is None:
            msg = "The authorization grant type is not supported by the authorization server."

        super(OAuth2UnsupportedGrantType, self).__init__(msg)


class ServiceExistsAlreadyError(Exception):
    def __init__(self, service: Service, msg=None):
        if msg is None:
            msg = f"{service} already in storage."

        super(ServiceExistsAlreadyError, self).__init__(msg)
        self.service = service


class ServiceNotExistsError(Exception):
    def __init__(self, service: Service, msg=None):
        if msg is None:
            msg = f"{service} not found."

        super(ServiceNotExistsError, self).__init__(msg)
        self.service = service
