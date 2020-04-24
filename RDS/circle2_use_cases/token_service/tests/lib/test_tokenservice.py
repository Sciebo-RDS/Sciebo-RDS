
import jwt
from datetime import datetime, timedelta
import unittest
import pytest
import os
import json
from lib.TokenService import TokenService
from pactman import Consumer, Provider
from server import bootstrap
from lib.Exceptions.ServiceException import *
from lib.Token import Token, OAuth2Token
from lib.Service import Service, OAuth2Service
from lib.User import User


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
        self.tokenService = TokenService(
            address="http://localhost:3000", testing=True)

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

        self.token1 = Token(self.user1, self.service1, "ABC")
        self.token2 = OAuth2Token(self.user1, self.service2, "ABC", "XYZ")

    def test_get_all_service_oauth(self):
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
        ) .will_respond_with(200, body={"length": 1, "list": [json.dumps(self.service1)]})

        all_services = self.tokenService.getAllOAuthURIForService()
        self.assertEqual(all_services, [self.url1])

        # test to get all service, where two services are
        pact.given(
            'Two services are registered.'
        ).upon_receiving(
            'a request to get all services.'
        ).with_request(
            'GET', '/service'
        ) .will_respond_with(200, body={"length": 2, "list": [json.dumps(self.service1), json.dumps(self.service2)]})

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
        ) .will_respond_with(200, body=json.dumps(self.service1))

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

        with pact:
            self.assertEqual(
                self.tokenService.getAllServicesForUser(self.user1), [])

        # test to get all services from one user, with one service
        pact.given(
            'one service was registered.'
        ).upon_receiving(
            'a request to get services from one specific user.'
        ).with_request(
            'GET', f"/user/{self.user1.username}/token"
        ) .will_respond_with(200, body={"length": 1, "list": [json.dumps(self.token1)]})

        expected_projects = []
        pact.given(
            'Given token to access port'
        ).upon_receiving(
            'projects from port taken from token with proj length {}'.format(
                len(expected_projects))
        ).with_request(
            'GET', f"/metadata/project"
        ) .will_respond_with(200, body=expected_projects)

        with pact:
            data = self.tokenService.getAllServicesForUser(self.user1)
        self.assertEqual(
            data, [{"id": 0, "servicename": self.servicename1, "access_token": self.token1.access_token, "projects": [], "implements":[]}], msg=str(data[0]))

        # test to get all services from one user, with two services
        pact.given(
            'two services were registered.'
        ).upon_receiving(
            'a request to get services from one specific user.'
        ).with_request(
            'GET', f"/user/{self.user1.username}/token"
        ) .will_respond_with(200, body={"length": 2, "list": [json.dumps(self.token1), json.dumps(self.token2)]})

        expected_projects = []
        pact.given(
            'Given token to access port'
        ).upon_receiving(
            'projects from port taken from token with proj length {}'.format(
                len(expected_projects))
        ).with_request(
            'GET', f"/metadata/project"
        ) .will_respond_with(200, body=expected_projects)

        expected_projects = []
        pact.given(
            'Given token to access port 2'
        ).upon_receiving(
            'projects from port taken from token with proj length {}'.format(
                len(expected_projects))
        ).with_request(
            'GET', f"/metadata/project"
        ) .will_respond_with(200, body=expected_projects)

        with pact:
            self.assertEqual(self.tokenService.getAllServicesForUser(
                self.user1), [{"id": 0, "servicename": self.servicename1, "access_token": self.token1.access_token, "projects": [], "implements":[]}, {"id": 1, "servicename": self.servicename2, "access_token": self.token2.access_token, "projects": [], "implements":[]}])

        pact.given(
            'two services were registered.'
        ).upon_receiving(
            'a request to get services from one specific user, which not exists.'
        ).with_request(
            'GET', f"/user/{self.user2.username}/token"
        ) .will_respond_with(404, body={})

        with self.assertRaises(UserNotFoundError):
            self.tokenService.getAllServicesForUser(self.user2)

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
        ) .will_respond_with(500, body={"error": "TokenNotExistsError"})

        with self.assertRaises(TokenNotFoundError):
            self.tokenService.removeTokenFromUser(self.token1, self.user1)

        # test to remove one token, where one different token is
        pact.given(
            'one different token registered.'
        ).upon_receiving(
            'a request to remove a token.'
        ).with_request(
            'DELETE', f"/user/{self.user1.username}/token/{self.token1.servicename}"
        ) .will_respond_with(500, body={"error": "TokenNotExistsError"})

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

    def test_get_all_service_jwt(self):
        # test, if no service was registered
        pact.given(
            'no service was registered yet.'
        ).upon_receiving(
            'a request to get all services.'
        ).with_request(
            'GET', "/service"
        ) .will_respond_with(200, body={"length": 0, "list": []})

        self.assertEqual(self.tokenService.getAllServices(), [])

        # test, if one service was registered
        pact.given(
            'one service was registered.'
        ).upon_receiving(
            'a request to get all services.'
        ).with_request(
            'GET', "/service"
        ) .will_respond_with(200, body={"length": 1, "list": [json.dumps(self.service1)]})

        key = "abc"

        req_list = self.tokenService.getAllServices()

        # should raise an invalid signature error
        from jwt.exceptions import InvalidSignatureError
        with self.assertRaises(InvalidSignatureError):
            req = jwt.decode(req_list[0]["jwt"], key, algorithms='HS256')

        """
        pact.given(
            'one service was registered.'
        ).upon_receiving(
            'a request to get all services and secret is okay.'
        ).with_request(
            'GET', "/service"
        ) .will_respond_with(200, body={"length": 1, "list": [json.dumps(self.service1)]})"""

        self.tokenService.secret = key
        req_list = self.tokenService.getAllServices()
        req = jwt.decode(req_list[0]["jwt"], key, algorithms='HS256')

        data = {
            "servicename": self.service1.servicename,
            "authorize_url": self.service1.authorize_url,
            "date": req["date"], 
            "implements": []
        }

        state = jwt.encode(data, key, algorithm='HS256')

        new_obj = {}
        new_obj["jwt"] = state.decode("utf-8")

        expected = [new_obj]

        self.assertEqual(req_list, expected)

        # test the single service getter.
        pact.given(
            'one service was registered.'
        ).upon_receiving(
            'a request to get this one service and secret is okay.'
        ).with_request(
            'GET', f"/service/{self.service1.servicename}"
        ) .will_respond_with(200, body=json.dumps(self.service1))

        self.tokenService.secret = key
        req_svc = self.tokenService.getService(self.service1)
        req = jwt.decode(req_svc["jwt"], key, algorithms='HS256')

        data = {
            "servicename": self.service1.servicename,
            "authorize_url": self.service1.authorize_url,
            "date": req["date"], 
            "implements": []
        }

        state = jwt.encode(data, key, algorithm='HS256')

        new_obj = {}
        new_obj["jwt"] = state.decode("utf-8")

        expected = new_obj

        self.assertEqual(req_svc, expected)

    def test_static_secret(self):
        # test the static secret variable for this run.
        frst = self.tokenService.secret
        scnd = self.tokenService.secret
        thrd = TokenService.secret

        self.assertEqual(frst, scnd)
        self.assertEqual(frst, thrd)

    def test_get_token_for_service_from_user(self):
        # test get token, if no token is there
        pact.given(
            'no token was registered.'
        ).upon_receiving(
            'a request to get a specific token for service from user.'
        ).with_request(
            'GET', f"/user/{self.user1.username}/token/{self.service1.servicename}"
        ) .will_respond_with(404, body={"error": "ServiceNotExistsError", "description": "Service not found."})

        with self.assertRaises(ServiceNotFoundError):
            self.tokenService.getTokenForServiceFromUser(
                self.service1, self.user1)

        # test get token, if one token, but not same is there
        pact.given(
            'one token was registered.'
        ).upon_receiving(
            'a request to get a specific token for service from user.'
        ).with_request(
            'GET', f"/user/{self.user1.username}/token/{self.service1.servicename}"
        ) .will_respond_with(404, body={"error": "ServiceNotExistsError", "description": "Service not found."})

        with self.assertRaises(ServiceNotFoundError):
            self.tokenService.getTokenForServiceFromUser(
                self.service1, self.user1)

        # test, get token successful
        pact.given(
            'one searched token was registered.'
        ).upon_receiving(
            'a request to get a specific token for service from user.'
        ).with_request(
            'GET', f"/user/{self.user1.username}/token/{self.service1.servicename}"
        ) .will_respond_with(200, body=json.dumps(self.token1))

        self.assertEqual(self.tokenService.getTokenForServiceFromUser(
            self.service1, self.user1), self.token1)

        # test, get oauthtoken successful, but it have to be reduced to token
        pact.given(
            'one searched oauthtoken was registered.'
        ).upon_receiving(
            'a request to get a specific oauthtoken for service from user.'
        ).with_request(
            'GET', f"/user/{self.user1.username}/token/{self.service1.servicename}"
        ) .will_respond_with(200, body=json.dumps(self.token2))

        reduced_token = Token(self.user1, self.token2.service,
                              self.token2.access_token)

        self.assertEqual(self.tokenService.getTokenForServiceFromUser(
            self.service1, self.user1), reduced_token)

    def test_remove_token_for_service_from_user(self):
        # remove the token, if no token for it is there
        pact.given(
            'no token was registered.'
        ).upon_receiving(
            'a request to remove a specific token for service from user.'
        ).with_request(
            'DELETE', f"/user/{self.user1.username}/token/{self.service1.servicename}"
        ) .will_respond_with(404, body={"error": "ServiceNotExistsError", "description": "Service not found."})

        with self.assertRaises(ServiceNotFoundError):
            self.tokenService.removeTokenForServiceFromUser(
                self.service1, self.user1)

        # remove the token, if one different token for it is there
        pact.given(
            'one token was registered.'
        ).upon_receiving(
            'a request to remove a specific token for service from user.'
        ).with_request(
            'DELETE', f"/user/{self.user1.username}/token/{self.service1.servicename}"
        ) .will_respond_with(404, body={"error": "ServiceNotExistsError", "description": "Service not found."})

        with self.assertRaises(ServiceNotFoundError):
            self.tokenService.removeTokenForServiceFromUser(
                self.service1, self.user1)

        # remove the token, if the searched token for it is there
        pact.given(
            'the search token was registered.'
        ).upon_receiving(
            'a request to remove a specific token for service from user.'
        ).with_request(
            'DELETE', f"/user/{self.user1.username}/token/{self.service1.servicename}"
        ) .will_respond_with(200, body={"success": True})

        self.assertEqual(self.tokenService.removeTokenForServiceFromUser(
            self.service1, self.user1), True)

    def test_exchange_code(self):
        code = "XYZABC"
        service = OAuth2Service(
            "localhost", f"{self.tokenService.address}/authorize", f"{self.tokenService.address}/oauth2/token", "ABC", "XYZ")

        with self.assertRaises(ValueError):
            self.tokenService.exchangeAuthCodeToAccessToken(
                code, Service("localhost"))

        body = {
            "access_token": "1vtnuo1NkIsbndAjVnhl7y0wJha59JyaAiFIVQDvcBY2uvKmj5EPBEhss0pauzdQ",
            "token_type": "Bearer",
            "expires_in": 3600,
            "refresh_token": "7y0wJuvKmj5E1vjVnhlPBEhha59JyaAiFIVQDvcBY2ss0pauzdQtnuo1NkIsbndA",
            "user_id": self.user1.username,
            "message_url": "https://www.example.org/owncloud/index.php/apps/oauth2/authorization-successful"
        }

        # need pact for exchange for code
        pact.given(
            'Client ID and secret was registered.'
        ).upon_receiving(
            'A request to exchange the given auth code to get access token and refresh token.'
        ).with_request(
            'POST', f"/oauth2/token"
        ) .will_respond_with(200, body=body)

        expected = OAuth2Token(self.user1, service, body["access_token"], body["refresh_token"], datetime.now(
        ) + timedelta(seconds=body["expires_in"]))

        # need pact for save the access and refresh token in Token Storage
        pact.given(
            'No token was registered for user'
        ).upon_receiving(
            'A request to add an oauthtoken.'
        ).with_request(
            'POST', f"/user/{self.user1.username}/token"
        ) .will_respond_with(200, body={"success": True})

        token = self.tokenService.exchangeAuthCodeToAccessToken(
            code, service)

        self.assertEqual(token, expected)

        # test for service object
        # need pact for exchange for code
        pact.given(
            'Client ID and secret was registered.'
        ).upon_receiving(
            'A request to exchange the given auth code to get access token and refresh token with service object.'
        ).with_request(
            'POST', f"/oauth2/token"
        ) .will_respond_with(200, body=body)

        # need pact for save the access and refresh token in Token Storage
        pact.given(
            'No token was registered for user'
        ).upon_receiving(
            'A request to add an oauthtoken with service object.'
        ).with_request(
            'POST', f"/user/{self.user1.username}/token"
        ) .will_respond_with(200, body={"success": True})

        token = self.tokenService.exchangeAuthCodeToAccessToken(
            code, service)

        self.assertEqual(token, expected)

        # test serviceNotFoundError
        pact.given(
            'no oauthservice was registered.'
        ).upon_receiving(
            'A request to get a oauthservice.'
        ).with_request(
            'GET', f"/service/{service.servicename}"
        ) .will_respond_with(500, body={"error": "ServiceNotExistsError", "http_code": 500})

        with self.assertRaises(ServiceNotFoundError):
            self.tokenService.exchangeAuthCodeToAccessToken(
                code, service.servicename)

        self.tokenService._storage = {}

        # test CodeNotExchangeableError
        pact.given(
            'An oauthservice was registered.'
        ).upon_receiving(
            'A request to get this oauthservice for exchange code.'
        ).with_request(
            'GET', f"/service/{service.servicename}"
        ) .will_respond_with(200, body=json.dumps(service))

        # need pact for exchange for code
        pact.given(
            'Client ID and secret was not registered.'
        ).upon_receiving(
            'A request to exchange the given auth code to get access token and refresh token.'
        ).with_request(
            'POST', f"/oauth2/token"
        ) .will_respond_with(500, body={"error": "Login not successful"})

        with self.assertRaises(CodeNotExchangeable):
            self.tokenService.exchangeAuthCodeToAccessToken(
                code, service.servicename)

    def test_serviceprojects(self):
        proj1 = {"projectId": 0, "projectName": "Project1"}
        proj2 = {"projectId": 1, "projectName": "Project2"}

        expected_projects = []
        pact.given(
            'Given token to access port'
        ).upon_receiving(
            'projects from port taken from token with proj length {}'.format(
                len(expected_projects))
        ).with_request(
            'GET', f"/metadata/project"
        ) .will_respond_with(200, body=expected_projects)
        with pact:
            projects = self.tokenService.getProjectsForToken(self.token1)
            self.assertEqual(projects, expected_projects)

        expected_projects = [proj1]
        pact.given(
            'Given token to access port'
        ).upon_receiving(
            'projects from port taken from token with proj length {}'.format(
                len(expected_projects))
        ).with_request(
            'GET', f"/metadata/project"
        ) .will_respond_with(200, body=expected_projects)
        with pact:
            projects = self.tokenService.getProjectsForToken(self.token1)
            self.assertEqual(projects, expected_projects)

        expected_projects = [proj1, proj2]
        pact.given(
            'Given token to access port'
        ).upon_receiving(
            'projects from port taken from token with proj length {}'.format(
                len(expected_projects))
        ).with_request(
            'GET', f"/metadata/project"
        ) .will_respond_with(200, body=expected_projects)
        with pact:
            projects = self.tokenService.getProjectsForToken(self.token1)
            self.assertEqual(projects, expected_projects)

    def test_serviceprojects_projects_not_supported(self):
        expected_projects = []
        pact.given(
            'Given token to access port'
        ).upon_receiving(
            'no projects are there or projects not supported'
        ).with_request(
            'GET', f"/metadata/project"
        ) .will_respond_with(500, body="")
        with pact:
            projects = self.tokenService.getProjectsForToken(self.token1)
            self.assertEqual(projects, expected_projects)
