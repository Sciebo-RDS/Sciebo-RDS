
import unittest, sys, os, json
from pactman import Consumer, Provider
from src.server import bootstrap


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


class TestPortZenodo(unittest.TestCase):
    app = create_app()
    client = app.test_client()

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def tearDown(self):
        pass

    def test_get_all(self):
        pass

if __name__ == '__main__':
    unittest.main()
