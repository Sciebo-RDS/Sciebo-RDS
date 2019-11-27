
import unittest, sys, os, json
from pactman import Consumer, Provider
from src.server import bootstrap


def create_app():
    # set var for mock service
    os.environ["CENTRAL-SERVICE_TOKEN-STORAGE"] = "http://localhost:3000"
    # creates a test client
    app = bootstrap(executes=False).app
    # propagate the exceptions to the test client
    app.config.update({"TESTING": True})

    return app


pact = Consumer('UseCaseTokenStorage').has_pact_with(
    Provider('CentralServiceTokenStorage'), port=3000)


class TestPortZenodo(unittest.TestCase):
    app = create_app()
    client = app.test_client()

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def tearDown(self):
        pass

    def test_service_authorize(self):
        expected = {
            "redirect_uri_full": "http://10.14.28.90/owncloud/index.php/apps/oauth2/authorize?response_type=code&client_id=S4MQ9MjTqb2sV47noTsQJ6REijG0u0LkScWJA2VG3LHkq7ue5t3CQPlu4ypX7RkS&redirect_uri=http://sciebords-dev.uni-muenster.de/oauth2/redirect",
            "redirect_uri": "http://sciebords-dev.uni-muenster.de/oauth2/redirect",
            "authorize_uri": "http://10.14.28.90/owncloud/index.php/apps/oauth2/authorize",
            "client_id": "S4MQ9MjTqb2sV47noTsQJ6REijG0u0LkScWJA2VG3LHkq7ue5t3CQPlu4ypX7RkS",
            "response_type": "code"
        }

        pact.given(
            "User can make a valid ownCloud oauth request."
        ).upon_receiving(
            "a valid response from UseCase-TokenStorage"
        ).with_request(
            "GET", "/service/owncloud"
        ).will_respond_with(200, body=expected)

        result = None
        with pact:
            result = self.client.get("/service/owncloud")

        self.assertEqual(result.json, expected)

        pact.given(
            "User can make a valid ownCloud oauth request for short."
        ).upon_receiving(
            "a valid response from UseCase-TokenStorage"
        ).with_request(
            "GET", "/service/owncloud/redirect_uri_full"
        ).will_respond_with(200, body=expected["redirect_uri_full"])

        with pact:
            result = self.client.get("/service/owncloud/redirect_uri_full")

        self.assertEqual(result.json, expected["redirect_uri_full"])


if __name__ == '__main__':
    unittest.main()
