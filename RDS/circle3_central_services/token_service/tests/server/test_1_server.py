
import unittest
import sys
import os
import json
from pactman import Consumer, Provider
from server import bootstrap
from lib.Storage import Storage
from lib.Token import Token, OAuth2Token
from lib.User import User
from lib.Service import Service, OAuth2Service
import Util


def create_app():
    # set var for mock service
    os.environ["address"] = "http://localhost:5000"
    # creates a test client
    app = bootstrap(use_default_error=True).app
    # propagate the exceptions to the test client
    app.config.update({"TESTING": True})

    return app


pact_host_port = 3000
pact_host_fqdn = f"http://localhost:{pact_host_port}"
pact = Consumer('CentralServiceTokenStorage').has_pact_with(
    Provider('OAuth-Provider'), port=pact_host_port)


class TestTokenService(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

        self.empty_storage = Storage()

        self.success = {"success": True}

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
        expected = {
            "length": 0,
            "list": []
        }

        self.assertEqual(self.client.get("/token").json, expected)
        self.assertEqual(self.client.get("/user").json, expected)
        self.assertEqual(self.client.get("/service").json, expected)

    def get(self, endpoint):
        """
        For convenience in this test suite.
        """
        data_result = []
        data = self.client.get(endpoint).json
        for d in data["list"]:
            data_result.append(Util.initialize_object_from_json(d))

        return data_result

    def test_list_service(self):
        expected = {
            "length": 0,
            "list": []
        }

        # no service should be there
        self.assertEqual(self.client.get("/service").json, expected)
        #self.assertEqual(self.client.post("/service", data=vars(self.service1)), self.service1)

        # add one simple service and try to get them
        expected = {
            "length": 1,
            "list": [self.service1]
        }

        result = self.client.post(
            "/service", data=json.dumps(self.service1.to_dict()), content_type='application/json')
        self.assertEqual(result.status_code, 200, msg=f"{result.json}")

        for k, v in enumerate(self.get("/service")):
            self.assertEqual(v, expected["list"][k], msg="{} {}".format(
                v, expected["list"][k]))

        # add the same service as oauth, should be an update
        expected = {
            "length": 1,
            "list": [self.oauthservice1]
        }

        result = self.client.post(
            "/service", data=json.dumps(self.oauthservice1.to_dict()), content_type='application/json')
        self.assertEqual(result.status_code, 204)

        for k, v in enumerate(self.get("/service")):
            self.assertEqual(v, expected["list"][k], msg="{} {}".format(
                v, expected["list"][k]))

        # add a simple service, there should be 2 services now
        expected = {
            "length": 2,
            "list": [self.oauthservice1, self.service2]
        }

        self.client.post("/service", data=json.dumps(self.service2.to_dict()),
                         content_type='application/json')

        for k, v in enumerate(self.get("/service")):
            self.assertEqual(v, expected["list"][k], msg="{} {}".format(
                v, expected["list"][k]))

    def test_list_user(self):
        expected = {
            "length": 0,
            "list": []
        }

        # no user should be there
        self.assertEqual(self.client.get("/user").json, expected)
        req = self.client.get(f"/user/{self.user1.username}")
        self.assertEqual(req.status_code, 404)
        self.assertEqual(req.json["error"], "NotFound")
        self.assertEqual(req.json["http_code"], 404)

        expected = {
            "length": 1,
            "list": [self.user1]
        }

        # add a user, then there should be a user
        result = self.client.post("/user", data=json.dumps(self.user1.to_dict()),
                                  content_type='application/json')

        self.assertEqual(result.status_code, 200, msg=result.json)
        self.assertEqual(result.json, {"success": True})
        self.assertEqual(self.client.get("/user").json, expected)

        req = self.client.get(f"/user/{self.user1.username}")
        self.assertEqual(req.status_code, 200)

        # get the added user
        self.assertEqual(self.client.get(
            f"/user/{self.user1.username}").json, self.user1)

        # add a new user and check
        expected = {
            "length": 2,
            "list": [self.user1, self.user2]
        }

        self.client.post("/user", data=json.dumps(self.user2.to_dict()),
                         content_type='application/json')
        self.assertEqual(self.client.get("/user").json, expected)
        # the first user should be there
        self.assertEqual(self.client.get(
            f"/user/{self.user1.username}").json, self.user1)

        # remove a user
        expected = {
            "length": 1,
            "list": [self.user2]
        }

        result = self.client.delete(f"/user/{self.user1.username}")
        self.assertEqual(result.status_code, 200)
        self.assertEqual(self.client.get("/user").json, expected)
        self.assertEqual(self.client.get(
            f"/user/{self.user1.username}").status_code, 404)

        result = self.client.delete(f"/user/{self.user1.username}")
        self.assertEqual(result.status_code, 404)

    def test_user_tokens(self):
        req = self.client.get(f"/user/{self.user1.username}")
        self.assertEqual(req.status_code, 404)
        self.assertEqual(req.json["error"], "NotFound")
        self.assertEqual(req.json["http_code"], 404)

        req = self.client.get(f"/user/{self.user1.username}/token")
        self.assertEqual(req.status_code, 404, msg=req.data)
        self.assertEqual(req.json["error"], "NotFound")
        self.assertEqual(req.json["http_code"], 404)

        req = self.client.get(f"/user/{self.user1.username}/token/0")
        self.assertEqual(req.status_code, 404)
        self.assertEqual(req.json["error"], "NotFound")
        self.assertEqual(req.json["http_code"], 404)

        result = self.client.post("/user", data=json.dumps(self.user1.to_dict()),
                                  content_type='application/json')
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.json, self.success)

        # we do not have to check here, if user is there, because it was checked in test_list_user.

        req = self.client.get(f"/user/{self.user1.username}/token/0")
        self.assertEqual(req.status_code, 404)
        self.assertEqual(req.json["error"], "NotFound")
        self.assertEqual(req.json["http_code"], 404)

        result = self.client.post(f"/user/{self.user1.username}/token",
                                  data=json.dumps(self.token1.to_dict()), content_type='application/json')
        self.assertEqual(result.status_code, 200, msg=result.json)
        self.assertEqual(result.json, self.success)

    def test_list_tokens(self):
        # there have to be a user
        self.client.post("/user", data=json.dumps(self.user1.to_dict()),
                         content_type='application/json')

        # no tokens there
        expected = {
            "length": 0,
            "list": []
        }

        self.assertEqual(self.client.get("/token").json, expected)

        # add a token to user
        expected = {
            "length": 1,
            "list": [self.token1]
        }

        result = self.client.post(f"/user/{self.user1.username}/token",
                                  data=json.dumps(self.token1.to_dict()), content_type='application/json')
        self.assertEqual(result.status_code, 200, msg=result.json)

        # list compare doesn't work properly, so we have to iterate.
        for k, v in enumerate(self.get("/token")):
            self.assertEqual(v, expected["list"][k], msg="{} {}".format(
                v, expected["list"][k]))

        # should response with http code not equal to 200, because user has already a token for this service
        response = self.client.post(f"/user/{self.user1.username}/token",
                                    data=json.dumps(self.oauthtoken1.to_dict()), content_type='application/json')
        self.assertNotEqual(response.status_code, 200)

        # add an oauthtoken to user
        expected = {
            "length": 2,
            "list": [self.token1, self.token2]
        }

        self.client.post(f"/user/{self.user1.username}/token",
                         data=json.dumps(self.oauthtoken2.to_dict()), content_type='application/json')

        for k, v in enumerate(self.get("/token")):
            self.assertEqual(v, expected["list"][k], msg="{} {}".format(
                v, expected["list"][k]))

        # remove a token
        index = 0

        result = self.client.get(f"/user/{self.user1.username}/token/{index}")
        self.assertEqual(result.status_code, 200,
                         msg=f"token id: {index} - {result.json}")
        token = Util.initialize_object_from_json(result.json)
        self.assertEqual(token, self.token1)

        expected = {
            "length": 1,
            "list": [self.token2]
        }

        result = self.client.delete(
            f"/user/{self.user1.username}/token/{index}")
        self.assertEqual(result.status_code, 200, msg=f"{result.json}")

        for k, v in enumerate(self.get("/token")):
            self.assertEqual(v, expected["list"][k], msg="{} {}".format(
                v, expected["list"][k]))


if __name__ == '__main__':
    unittest.main()
