import unittest
from lib.Service import Service, OAuth2Service
from lib.Storage import Storage
from lib.Token import Token, Oauth2Token
from lib.User import User
from lib.Exceptions.ServiceExceptions import TokenNotValidError
from pactman import Consumer, Provider


pact_host_port = 3000
pact_host_fqdn = f"http://localhost:{pact_host_port}"
pact = Consumer('CentralServiceTokenStorage').has_pact_with(
    Provider('OAuth-Provider'), port=pact_host_port)


class TestStorageService(unittest.TestCase):
    def setUp(self):
        self.empty_storage = Storage()

        self.user1 = User("Max Mustermann")
        self.user2 = User("Mimi Mimikri")

        self.token1 = Token("MusterService", "ABC")
        self.token_like_token1 = Token("MusterService", "DEF")
        self.token2 = Token("BetonService", "XYZ")

        self.oauthtoken1 = Oauth2Token.from_token(self.token1, "X_ABC")
        self.oauthtoken_like_token1 = Oauth2Token.from_token(
            self.token_like_token1, "X_DEF")
        self.oauthtoken2 = Oauth2Token.from_token(self.token2, "X_XYZ")

        self.service1 = Service("MusterService")
        self.service2 = Service("BetonService")

        self.oauthservice1 = OAuth2Service.from_service(
            self.service1, f"{pact_host_fqdn}/owncloud/index.php/apps/oauth2/authorize",
            f"{pact_host_fqdn}/owncloud/index.php/apps/oauth2/api/v1/token", "ABC", "XYZ")

        self.oauthservice2 = OAuth2Service.from_service(
            self.service2, "http://localhost:5001/oauth/authorize", "http://localhost:5001/oauth/token", "DEF", "UVW")

    """ Currently not implemented and no idea how to solve.
    def test_valid_token(self):
        # Test, if token can be used in service
        self.assertTrue(self.service1.is_valid(self.token1, self.user1))
        self.assertTrue(self.oauthservice1.is_valid(
            self.oauthtoken1, self.user1))

        self.assertFalse(self.service1.is_valid(self.token2, self.user2))
        self.assertFalse(self.oauthservice1.is_valid(
            self.oauthtoken2, self.user2))

        # try to use the token to raise an exception
        with self.assertRaises(TokenNotValidError):
            self.oauthservice1.status(self.token1)"""

    def test_refresh_oauth2token(self):
        from datetime import datetime
        from time import time

        expires_in = 3600
        expected = Oauth2Token.from_token(self.token1, "XYZ")
        expected._exiration_date = datetime.fromtimestamp(time() + expires_in)

        # example taken from https://github.com/owncloud/oauth2
        json_expected = {
            "access_token": "1vtnuo1NkIsbndAjVnhl7y0wJha59JyaAiFIVQDvcBY2uvKmj5EPBEhss0pauzdQ",
            "token_type": "Bearer",
            "expires_in": expires_in,
            "refresh_token": "7y0wJuvKmj5E1vjVnhlPBEhha59JyaAiFIVQDvcBY2ss0pauzdQtnuo1NkIsbndA",
            "user_id": self.user1.username,
            "message_url": f"{pact_host_fqdn}/owncloud/index.php/apps/oauth2/authorization-successful"
        }

        pact.given(
            "Username can refresh given oauth2token", username=self.user1.username
        ).upon_receiving(
            "A valid refresh token response."
        ).with_request(
            "POST", "/owncloud/index.php/apps/oauth2/api/v1/token"
        ).will_respond_with(200, body=json_expected)

        result = None
        with pact:
            result = self.oauthservice1.refresh(self.token1, self.user1)
            self.assertEqual(result, expected,
                             msg=f"\nresult: {result}\nexpected: {expected}")

        # this needs to be here, because it counts the given interactions, 
        # so if this is missing, you get an error, when you do the following assertion.
        pact.given(
            "Username can refresh given oauth2token", username=self.user1.username
        ).upon_receiving(
            "A valid refresh token response."
        ).with_request(
            "POST", "/owncloud/index.php/apps/oauth2/api/v1/token"
        ).will_respond_with(200, body=json_expected)

        with self.assertRaises(TokenNotValidError):
            with pact:
                self.oauthservice1.refresh(self.token1, self.user2)
