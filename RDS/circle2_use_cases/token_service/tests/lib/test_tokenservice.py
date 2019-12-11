import unittest
import pytest
import os
import json
from lib.TokenService import TokenService
from pactman import Consumer, Provider
from server import bootstrap
from lib.Exceptions.ServiceExceptions import *
from lib.Token import *
from lib.Service import *
from lib.User import *


def create_app():
    # set var for mock service
    # creates a test client
    app = bootstrap().app
    # propagate the exceptions to the test client
    app.config.update({"TESTING": True})

    return app


pact = Consumer('UseCaseTokenStorage').has_pact_with(
    Provider('CentralServiceTokenStorage'), port=3000)


class Test_TokenService(unittest.TestCase):
    app = create_app()
    client = app.test_client()

    def run(self, result=None):
        # this make pact as context in every test available.
        with pact as p:
            super(Test_TokenService, self).run(result)

    def setUp(self):
        self.tokenService = TokenService(address="http://localhost:3000")

        self.url1 = "http://10.14.28.90/owncloud/index.php/apps/oauth2/authorize?response_type=code&client_id={}&redirect_uri={}".format(
            1, "http://localhost:8080")
        self.url2 = "http://zenodo.org/oauth/authorize?response_type=code&client_id={}&redirect_uri={}".format(
            2, "http://localhost:8080")

        self.servicename1 = "owncloud-local"
        self.servicename2 = "sandbox.zenodo.org"

        self.user1 = User("user")
        self.user2 = User("user_refresh")

        self.service1 = OAuth2Service(self.servicename1, self.url1,
                                      "http://10.14.28.90/owncloud/index.php/apps/oauth2/api/v1/token", "ABC", "XYZ")

        self.service2 = OAuth2Service(self.servicename2, self.url2,
                                      "https://sandbox.zenodo.org/oauth/token", "DEF", "UVW")

        self.token1 = Token(self.service1.servicename, "ABC")
        self.token2 = OAuth2Token(self.service2.servicename, "ABC", "XYZ")

    def test_get_all_service(self):
        # test to get all service, where no service is
        pact.given(
            'No services are registered.'
        ).upon_receiving(
            'a request to get all services.'
        ).with_request(
            'GET', '/service'
        ) .will_respond_with(200, body={"length": 0, "list": []})

        all_services = self.tokenService.getAllOAuthURIForService()
        self.assertEqual(all_services, [])

        # test to get all service, where one service is
        pact.given(
            'One service is registered.'
        ).upon_receiving(
            'a request to get all services.'
        ).with_request(
            'GET', '/service'
        ) .will_respond_with(200, body={"length": 1, "list": [self.service1.to_json()]})

        all_services = self.tokenService.getAllOAuthURIForService()
        self.assertEqual(all_services, [self.url1])

        # test to get all service, where two services are
        pact.given(
            'Two services are registered.'
        ).upon_receiving(
            'a request to get all services.'
        ).with_request(
            'GET', '/service'
        ) .will_respond_with(200, body={"length": 2, "list": [self.service1.to_json(), self.service2.to_json()]})

        all_services = self.tokenService.getAllOAuthURIForService()
        self.assertEqual(
            all_services, [self.url1, self.url2], msg=all_services)

    def test_get_specific_service(self):
        # test to get one specific service, where no service is
        pact.given(
            'No services are registered.'
        ).upon_receiving(
            'a request to get one specific service.'
        ).with_request(
            'GET', f"/service/{self.service1.servicename}"
        ) .will_respond_with(500, body={
            "error": "ServiceNotFoundError",
            "http_code": 500,
            "description": f"{self.service1} not found."
        })

        with self.assertRaises(ServiceNotFoundError):
            self.tokenService.getOAuthURIForService(self.service1)

        # test to get one specific service, where one different service is
        pact.given(
            'One service are registered.'
        ).upon_receiving(
            'a request to get one other specific service.'
        ).with_request(
            'GET', f"/service/{self.service1.servicename}"
        ) .will_respond_with(500, body={
            "error": "ServiceNotFoundError",
            "http_code": 500,
            "description": f"{self.service1} not found."
        })
        with self.assertRaises(ServiceNotFoundError):
            self.tokenService.getOAuthURIForService(self.service1)

        # test to get one specific service, where the same services are
        pact.given(
            'one service was registered.'
        ).upon_receiving(
            'a request to get this one specific service.'
        ).with_request(
            'GET', f"/service/{self.service1.servicename}"
        ) .will_respond_with(200, body=self.service1.to_json())

        svc = self.tokenService.getOAuthURIForService(self.service1)
        self.assertEqual(svc, self.url1)

    def test_get_services_for_user(self):
        # test to get all services from one user, with no service
        pact.given(
            'no service was registered.'
        ).upon_receiving(
            'a request to get services from one specific user.'
        ).with_request(
            'GET', f"/user/{self.user1.username}/token"
        ) .will_respond_with(200, body={"length": 0, "list": []})

        self.assertEqual(
            self.tokenService.getAllServicesForUser(self.user1), [])

        # test to get all services from one user, with one service
        pact.given(
            'one service was registered.'
        ).upon_receiving(
            'a request to get services from one specific user.'
        ).with_request(
            'GET', f"/user/{self.user1.username}/token"
        ) .will_respond_with(200, body={"length": 1, "list": [self.token1.to_json()]})

        data = self.tokenService.getAllServicesForUser(
            self.user1)
        self.assertEqual(data, [self.servicename1], msg=str(data[0]))

        # test to get all services from one user, with two services
        pact.given(
            'two services were registered.'
        ).upon_receiving(
            'a request to get services from one specific user.'
        ).with_request(
            'GET', f"/user/{self.user1.username}/token"
        ) .will_respond_with(200, body={"length": 2, "list": [self.token1.to_json(), self.token2.to_json()]})

        self.assertEqual(self.tokenService.getAllServicesForUser(
            self.user1), [self.servicename1, self.servicename2])

    # FIXME: addService not through this use case? directly to central service?
    """
    def test_add_one_service(self):

        # test to add one service, where no service is
        self.assertEqual(self.tokenService.addService(self.service), True)

        # test to add one service, where one different service is
        self.assertEqual(self.tokenService.addService(self.service), True)

        # test to add one service, where the same service is
        with self.assertRaises(ServiceAlreadyRegisteredError):
            self.tokenService.addService(self.service)
        pass


    def test_remove_one_service(self):
        with self.assertRaises(ServiceNotFoundError):
            self.tokenService.removeService(self.service1)

        # test to remove one service, where one different service is
        with self.assertRaises(ServiceNotFoundError):
            self.tokenService.removeService(self.service1)

        # test to remove one service, where the same service is
        self.assertEqual(self.tokenService.removeService(self.service1), True)
    """

    def test_add_user(self):
        # test to add one user, where no user is
        pact.given(
            'no user was registered.'
        ).upon_receiving(
            'a request to add an user.'
        ).with_request(
            'POST', f"/user"
        ) .will_respond_with(200, body={"success": True})

        self.assertEqual(self.tokenService.addUser(self.user1), True)

        # test to add one user, where one different user is
        pact.given(
            'one different user was registered.'
        ).upon_receiving(
            'a request to add an user.'
        ).with_request(
            'POST', f"/user"
        ) .will_respond_with(200, body={"success": True})
        self.assertEqual(self.tokenService.addUser(self.user1), True)

        # test to add one user, where the same user is
        pact.given(
            'the same user was registered.'
        ).upon_receiving(
            'a request to add an user.'
        ).with_request(
            'POST', f"/user"
        ) .will_respond_with(500, body={"error": "UserAlreadyRegisteredError", "http_code": 500, "description": f"{self.user1} already registered."})

        with self.assertRaises(UserAlreadyRegisteredError):
            self.tokenService.addUser(self.user1)

    def test_remove_user(self):
        # test to remove one user, where no user is
        pact.given(
            'no user was registered.'
        ).upon_receiving(
            'a request to remove an user.'
        ).with_request(
            'DELETE', f"/user/{self.user1.username}"
        ) .will_respond_with(404, body={"description": "User not found"})

        with self.assertRaises(UserNotFoundError):
            self.tokenService.removeUser(self.user1)

        # test to remove one user, where one different user is
        pact.given(
            'one different user was registered.'
        ).upon_receiving(
            'a request to remove an user.'
        ).with_request(
            'DELETE', f"/user/{self.user1.username}"
        ) .will_respond_with(404, body={"description": "User not found"})

        with self.assertRaises(UserNotFoundError):
            self.tokenService.removeUser(self.user1)

        # test to remove one user, where the same user is
        pact.given(
            'the user was registered.'
        ).upon_receiving(
            'a request to remove an user.'
        ).with_request(
            'DELETE', f"/user/{self.user1.username}"
        ) .will_respond_with(200, body={"success": True})

        self.assertEqual(self.tokenService.removeUser(self.user1), True)

    def test_add_token(self):
        # test to add one token, where no service and user is
        pact.given(
            'no service and user was registered.'
        ).upon_receiving(
            'a request to add a token.'
        ).with_request(
            'POST', f"/user/{self.user1.username}/token"
        ) .will_respond_with(500, body={"error": "ServiceNotFoundError"})

        with self.assertRaises(ServiceNotFoundError):
            self.tokenService.addTokenToUser(
                self.token1, self.user1)

        # test to add one token, where no service but user is
        pact.given(
            'no service was registered.'
        ).upon_receiving(
            'a request to add a token.'
        ).with_request(
            'POST', f"/user/{self.user1.username}/token"
        ) .will_respond_with(500, body={"error": "ServiceNotFoundError"})

        with self.assertRaises(ServiceNotFoundError):
            self.tokenService.addTokenToUser(
                self.token1, self.user1)

        # test to add one token, where service but no user is
        pact.given(
            'no user was registered.'
        ).upon_receiving(
            'a request to add a token.'
        ).with_request(
            'POST', f"/user/{self.user1.username}/token"
        ) .will_respond_with(500, body={"error": "UserNotExistsError"})

        with self.assertRaises(UserNotFoundError):
            self.tokenService.addTokenToUser(
                self.token1, self.user1)

        # test to add one token, where service and user exists
        pact.given(
            'user and service were registered.'
        ).upon_receiving(
            'a request to add a token.'
        ).with_request(
            'POST', f"/user/{self.user1.username}/token"
        ) .will_respond_with(200, body={"success": True})

        self.assertEqual(self.tokenService.addTokenToUser(
            self.token1, self.user1), True)

        # test to add one token, where service and user exists and user has token already for service
        pact.given(
            'user and service were registered, user has token for service already.'
        ).upon_receiving(
            'a request to add a token.'
        ).with_request(
            'POST', f"/user/{self.user1.username}/token"
        ) .will_respond_with(500, body={"error": "UserHasTokenAlreadyError"})

        with self.assertRaises(UserHasTokenAlreadyError):
            self.tokenService.addTokenToUser(self.token1, self.user1)

    def test_remove_token(self):
        # test to remove one token, where no user is
        pact.given(
            'no user registered.'
        ).upon_receiving(
            'a request to remove a token.'
        ).with_request(
            'DELETE', f"/user/{self.user1.username}/token/{self.token1.servicename}"
        ) .will_respond_with(500, body={"error": "UserNotExistsError"})

        with self.assertRaises(UserNotFoundError):
            self.tokenService.removeTokenFromUser(self.token1, self.user1)

        # test to remove one token, where no token is
        pact.given(
            'no token registered.'
        ).upon_receiving(
            'a request to remove a token.'
        ).with_request(
            'DELETE', f"/user/{self.user1.username}/token/{self.token1.servicename}"
        ) .will_respond_with(500, body={"error": "TokenNotExists"})

        with self.assertRaises(TokenNotFoundError):
            self.tokenService.removeTokenFromUser(self.token1, self.user1)

        # test to remove one token, where one different token is
        pact.given(
            'one different token registered.'
        ).upon_receiving(
            'a request to remove a token.'
        ).with_request(
            'DELETE', f"/user/{self.user1.username}/token/{self.token1.servicename}"
        ) .will_respond_with(500, body={"error": "TokenNotExists"})

        with self.assertRaises(TokenNotFoundError):
            self.tokenService.removeTokenFromUser(self.token1, self.user1)

        # test to remove one token, where the same token is
        pact.given(
            'the token registered.'
        ).upon_receiving(
            'a request to remove a token.'
        ).with_request(
            'DELETE', f"/user/{self.user1.username}/token/{self.token1.servicename}"
        ) .will_respond_with(200, body={"success": True})

        self.assertEqual(self.tokenService.removeTokenFromUser(
            self.token1, self.user1), True)
