
import unittest, sys, os
from pactman import Consumer, Provider
from src.server import bootstrap


def create_app():
    # set var for mock service
    os.environ["ZENODO_ADDRESS"] = "http://localhost:5000"
    # creates a test client
    app = bootstrap(executes=False).app
    # propagate the exceptions to the test client
    app.config.update({"TESTING": True})

    return app


pact = Consumer('PortZenodo').has_pact_with(Provider('Zenodo'), port=5000)

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

    @unittest.skip
    def test_home_status_code(self):
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
        
        self.assertEqual(result.json, expected)

if __name__ == '__main__':
    unittest.main()