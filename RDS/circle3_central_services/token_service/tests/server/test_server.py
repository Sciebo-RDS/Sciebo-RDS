
import unittest
import sys
import os
import json
from pactman import Consumer, Provider
from src.server import bootstrap
from src.lib.Storage import Storage
from src.lib.Token import Token, OAuth2Token
from src.lib.User import User
from src.lib.Service import Service, OAuth2Service


def create_app():
    # set var for mock service
    os.environ["address"] = "http://localhost:5000"
    # creates a test client
    app = bootstrap(executes=False).app
    # propagate the exceptions to the test client
    app.config.update({"TESTING": True})

    return app


pact_host_port = 3000
pact_host_fqdn = f"http://localhost:{pact_host_port}"
pact = Consumer('CentralServiceTokenStorage').has_pact_with(
    Provider('OAuth-Provider'), port=pact_host_port)


class TestTokenService(unittest.TestCase):
    app = create_app()
    client = app.test_client()

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

    def test_empty_storage(self):
        expected = []

        self.assertEqual(self.client.get("/token").json, expected)
        self.assertEqual(self.client.get("/user").json, expected)
        self.assertEqual(self.client.get("/service").json, expected)

    def test_list_service(self):
        expected = []

        self.assertEqual(self.client.get("/service").json, expected)
        #self.assertEqual(self.client.post("/service", data=vars(self.service1)), self.service1)

    def test_list_tokens(self):
        expected = []

        self.assertEqual(self.client.get("/token").json, expected)

    def test_list_user(self):
        expected = []

        self.assertEqual(self.client.get("/user").json, expected)

        expected.append(self.user1)

        self.client.post("/user", data=json.dumps(self.user1), content_type='application/json')
        self.assertEqual(self.client.get("/user").json, expected)

    """def test_home_status_code(self):
        expected = []

        pact.given(
            'UserA exists and is not an administrator'
        ).upon_receiving(
            'a request for UserA'
        ).with_request(
            'GET', '/api/deposit/depositions'
        ) .will_respond_with(200, body=expected)

        result = None
        with pact:
            result = self.client.get("/c2/deposition")
        
        self.assertEqual(result.json, expected)"""


if __name__ == '__main__':
    unittest.main()
