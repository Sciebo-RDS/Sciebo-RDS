import unittest
import os
from lib.TokenService import TokenService
from lib.Service import OAuth2Service
from pactman import Consumer, Provider
from server import bootstrap


def create_app():
    # set var for mock service
    os.environ["CENTRAL-SERVICE_TOKEN-STORAGE"] = "http://localhost:3000"
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

    def setUp(self):
        self.tokenService = TokenService()

        self.url1 = "http://10.14.28.90/owncloud/index.php/apps/oauth2/authorize?response_type=code&client_id={}&redirect_uri={}".format(
            1, "http://localhost:8080")
        self.url1 = "http://zenodo.org/oauth/authorize?response_type=code&client_id={}&redirect_uri={}".format(
            2, "http://localhost:8080")

        self.servicename1 = "owncloud-local"
        self.servicename2 = "sandbox.zenodo.org"

        self.user1 = "user"
        self.user2 = "user_refresh"

        self.service1 = OAuth2Service(self.servicename1, self.url1,
                                      "http://10.14.28.90/owncloud/index.php/apps/oauth2/api/v1/token", "ABC", "XYZ")

        pact.setup()

    def tearDown(self):
        pact.verify()

    def test_get_service(self):
        pact.given("some data exists").upon_receiving("a request") \
            .with_request("get", "/", query={"foo": ["bar"]}).will_respond_with(200)

        # test to get all service, where no service is
        all_services = self.tokenService.getAllOAuthURIForService()
        self.assertEqual(all_services, [])

        # test to get all service, where one service is
        all_services = self.tokenService.getAllOAuthURIForService()
        self.assertEqual(all_services, [self.url1])

        # test to get all service, where two services are
        all_services = self.tokenService.getAllOAuthURIForService()
        self.assertEqual(all_services, [self.url1, self.url2])

        # test to get one specific service, where no service is
        with self.assertRaises(ServiceNotRegisteredError):
            self.tokenService.getOAuthURIForService(self.servicename1)

        # test to get one specific service, where one different service is
        with self.assertRaises(ServiceNotRegisteredError):
            self.tokenService.getOAuthURIForService(self.servicename1)

        # test to get one specific service, where the same services are
        svc = self.tokenService.getOAuthURIForService(self.servicename1)
        self.assertEqual(svc, self.url1)

    def test_get_services_for_user(self):
        # test to get all services from one user, with no service
        self.assertEqual(
            self.tokenService.getAllServicesForUser(self.user1), [])

        # test to get all services from one user, with one service
        self.assertEqual(self.tokenService.getAllServicesForUser(
            self.user1), [self.servicename1])

        # test to get all services from one user, with two services
        self.assertEqual(self.tokenService.getAllServicesForUser(
            self.user1), [self.servicename1, self.servicename2])

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
        # test to remove one service, where no service is
        with self.assertRaises(ServiceNotFoundError):
            self.tokenService.removeService(self.service1)

        # test to remove one service, where one different service is
        with self.assertRaises(ServiceNotFoundError):
            self.tokenService.removeService(self.service1)

        # test to remove one service, where the same service is
        self.assertEqual(self.tokenService.removeService(self.service1), True)

    def test_add_user(self):
        # test to add one user, where no user is
        self.assertEqual(self.tokenService.addUser(self.user1), True)

        # test to add one user, where one different user is
        self.assertEqual(self.tokenService.addUser(self.user1), True)

        # test to add one user, where the same user is
        with self.assertRaises(UserAlreadyRegisteredError):
            self.tokenService.addUser(self.user1)

    def test_remove_user(self):
        # test to remove one user, where no user is
        with self.assertRaises(UserNotFoundError):
            self.tokenService.removeUser(self.user1)

        # test to remove one user, where one different user is
        with self.assertRaises(UserNotFoundError):
            self.tokenService.removeUser(self.user1)

        # test to remove one user, where the same user is
        self.assertEqual(self.tokenService.removeUser(self.user1), True)

    def test_add_token(self):
        # test to add one token, where no service and user is
        with self.assertRaises(ServiceNotFoundError):
            self.tokenService.addToken(
                self.servicename1, self.user1, self.token1)

        # test to add one token, where no service and but user is
        with self.assertRaises(ServiceNotFoundError):
            self.tokenService.addToken(
                self.servicename1, self.user1, self.token1)

        # test to add one token, where service and but no user is
        with self.assertRaises(UserNotFoundError):
            self.tokenService.addToken(
                self.servicename1, self.user1, self.token1)

        # test to add one token, where service and user exists
        self.assertRaises(self.tokenService.addToken(
            self.servicename1, self.user1, self.token1), True)

    def test_remove_token(self):
        # test to remove one token, where no token is
        with self.assertRaises(TokenNotFoundError):
            self.tokenService.removeToken(self.user1, self.token1)

        # test to remove one token, where one different token is
        with self.assertRaises(TokenNotFoundError):
            self.tokenService.removeToken(self.user1, self.token1)

        # test to remove one token, where the same token is
        self.assertEqual(self.tokenService.removeToken(
            self.user1, self.token1), True)
