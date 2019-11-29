import unittest
from lib.Service import Service, OAuth2Service
from lib.Storage import Storage
from lib.Token import Token, OAuth2Token
from lib.User import User
from lib.Exceptions.ServiceExceptions import *
from pactman import Consumer, Provider

from datetime import datetime
from time import time

import logging, sys
logger = logging.getLogger()
logger.level = logging.DEBUG
logger.addHandler(logging.StreamHandler(sys.stdout))

pact_host_port = 3000
pact_host_fqdn = f"http://localhost:{pact_host_port}"
pact = Consumer('CentralServiceTokenStorage').has_pact_with(
    Provider('OAuth-Provider'), port=pact_host_port)


class TestStorageService(unittest.TestCase):
    def setUp(self):
        self.empty_storage = Storage()

        self.user1 = User("Max Mustermann")
        self.user2 = User("Mimi Mimikri")
        self.user3 = User("Karla Kolumda")

        self.service1 = Service("MusterService")
        self.service2 = Service("BetonService")
        self.service3 = Service("FahrService")

        self.oauthservice1 = OAuth2Service.from_service(
            self.service1, f"{pact_host_fqdn}/owncloud/index.php/apps/oauth2/authorize",
            f"{pact_host_fqdn}/owncloud/index.php/apps/oauth2/api/v1/token", "ABC", "XYZ")

        self.oauthservice2 = OAuth2Service.from_service(
            self.service2, f"{pact_host_fqdn}/oauth/authorize", f"{pact_host_fqdn}/oauth/token", "DEF", "UVW")

        self.oauthservice3 = OAuth2Service.from_service(
            self.service3, f"{pact_host_fqdn}/api/authorize", f"{pact_host_fqdn}/api/token", "GHI", "MNO")
        
        self.token1 = Token(self.service1.servicename, "ABC")
        self.token_like_token1 = Token(self.service1.servicename, "DEF")
        self.token2 = Token(self.service2.servicename, "XYZ")
        self.token3 = Token(self.service3.servicename, "GHI")

        self.oauthtoken1 = OAuth2Token.from_token(self.token1, "X_ABC")
        self.oauthtoken_like_token1 = OAuth2Token.from_token(
            self.token_like_token1, "X_DEF")
        self.oauthtoken2 = OAuth2Token.from_token(self.token2, "X_XYZ")
        self.oauthtoken3 = OAuth2Token.from_token(self.token3, "X_GHI")


        self.services = [
            self.service1, self.service2, self.service3,
            self.oauthservice1, self.oauthservice2, self.oauthservice3
        ]

        self.filled_storage_without_tokens = Storage()
        self.filled_storage_without_tokens.addUser(self.user1)
        self.filled_storage_without_tokens.addUser(self.user2)
        self.filled_storage_without_tokens.addUser(self.user3)

        self.filled_storage = Storage()
        # user1 is filled with mixed token and oauth2token
        self.filled_storage.addUser(self.user1)
        self.filled_storage.addTokenToUser(self.token1, self.user1)
        self.filled_storage.addTokenToUser(self.token3, self.user1)
        self.filled_storage.addTokenToUser(self.oauthtoken2, self.user1)

        # user2 is only filled with token
        self.filled_storage.addUser(self.user2)
        self.filled_storage.addTokenToUser(self.token2, self.user2)

        # user3 is only filled with oauth2token
        self.filled_storage.addUser(self.user3)
        self.filled_storage.addTokenToUser(self.oauthtoken1, self.user3)
        self.filled_storage.addTokenToUser(self.oauthtoken3, self.user3)

    def test_internal_find_services(self):
        self.assertEqual(self.empty_storage.internal_find_service(self.service1.servicename, [self.service1]), 0)
        self.assertEqual(self.empty_storage.internal_find_service(self.service1.servicename, [self.service1, self.service2]), 0)
        self.assertEqual(self.empty_storage.internal_find_service(self.service1.servicename, [self.service2, self.service1]), 1)
        self.assertEqual(self.empty_storage.internal_find_service(self.service2.servicename, [self.service1, self.service2]), 1)

        self.assertEqual(self.empty_storage.internal_find_service(self.oauthservice1.servicename, [self.oauthservice1]), 0)
        self.assertEqual(self.empty_storage.internal_find_service(self.oauthservice1.servicename, [self.oauthservice1, self.oauthservice2]), 0)
        self.assertEqual(self.empty_storage.internal_find_service(self.oauthservice1.servicename, [self.oauthservice2, self.oauthservice1]), 1)
        self.assertEqual(self.empty_storage.internal_find_service(self.oauthservice2.servicename, [self.oauthservice1, self.oauthservice2]), 1)

        self.assertEqual(self.empty_storage.internal_find_service(self.oauthservice2.servicename, [self.service1, self.oauthservice2]), 1)

        with self.assertRaises(ValueError):
            self.empty_storage.internal_find_service(self.service1.servicename, [self.service2])

        with self.assertRaises(ValueError):
            self.empty_storage.internal_find_service(self.service1.servicename, [self.service2, self.service3])

        with self.assertRaises(ValueError):
            self.empty_storage.internal_find_service(self.service1.servicename, [self.oauthservice2, self.oauthservice3])

        with self.assertRaises(ValueError):
            self.empty_storage.internal_find_service(self.oauthservice1.servicename, [self.service2, self.service3])

    def test_refresh_all_tokens(self):
        # works without any tokens
        self.assertFalse(self.filled_storage_without_tokens.refresh_service(self.service1))
        self.assertFalse(self.filled_storage_without_tokens.refresh_services(self.oauthservice1))
        self.assertFalse(self.filled_storage_without_tokens.refresh_services(self.services))

        self.assertTrue(self.filled_storage.refresh_service(self.service1), msg=self.filled_storage)
        
        # works with a request to a provider
        expected_user = self.user3
        expected_service = self.oauthservice1
        expires_in = 3600

        # example taken from https://github.com/owncloud/oauth2
        json_expected = {
            "access_token": "1vtnuo1NkIsbndAjVnhl7y0wJha59JyaAiFIVQDvcBY2uvKmj5EPBEhss0pauzdQ",
            "token_type": "Bearer",
            "expires_in": expires_in,
            "refresh_token": "7y0wJuvKmj5E1vjVnhlPBEhha59JyaAiFIVQDvcBY2ss0pauzdQtnuo1NkIsbndA",
            "user_id": expected_user.username,
            "message_url": f"{pact_host_fqdn}/owncloud/index.php/apps/oauth2/authorization-successful"
        }

        pact.given(
            "Username can refresh given oauth2token to service", username=expected_user.username, service=expected_service
        ).upon_receiving(
            "A valid refresh token response."
        ).with_request(
            "POST", "/owncloud/index.php/apps/oauth2/api/v1/token", headers={"Authorization": "Basic S2FybGEgS29sdW1kYTpYWVo="}
        ).will_respond_with(200, body=json_expected)

        result = None
        with pact:
           result = self.filled_storage.refresh_service(expected_service)

        self.assertTrue(result)

        # test for missing service
        self.assertFalse(self.filled_storage.refresh_services([Service("NotFoundService")]))

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
        expires_in = 3600
        expected = OAuth2Token.from_token(self.token1, "XYZ")
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

        pact.given(
            "Username can't refresh given oauth2token", username=self.user1.username
        ).upon_receiving(
            "A bad request was made."
        ).with_request(
            "POST", "/owncloud/index.php/apps/oauth2/api/v1/token"
        ).will_respond_with(400, body=json_expected)

        with self.assertRaises(OAuth2UnsuccessfulResponseError):
            with pact:
                self.oauthservice1.refresh(self.token1, self.user1)

        self.make_bad_request_for_oauth_provider(
            "invalid_request", OAuth2InvalidRequestError)
        self.make_bad_request_for_oauth_provider(
            "invalid_client", OAuth2InvalidClientError)
        self.make_bad_request_for_oauth_provider(
            "invalid_grant", OAuth2InvalidGrantError)
        self.make_bad_request_for_oauth_provider(
            "unauthorized_client", OAuth2UnauthorizedClient)
        self.make_bad_request_for_oauth_provider(
            "unsupported_grant_type", OAuth2UnsupportedGrantType)

    def make_bad_request_for_oauth_provider(self, error_code, error):
        json_expected = {
            "error": error_code
        }

        pact.given(
            "Username made a bad request", username=self.user1.username
        ).upon_receiving(
            f"A bad request with error {error_code} was made."
        ).with_request(
            "POST", "/owncloud/index.php/apps/oauth2/api/v1/token"
        ).will_respond_with(400, body=json_expected)

        with self.assertRaises(error):
            with pact:
                self.oauthservice1.refresh(self.token1, self.user1)

if __name__ == "__main__":
    unittest.main()
