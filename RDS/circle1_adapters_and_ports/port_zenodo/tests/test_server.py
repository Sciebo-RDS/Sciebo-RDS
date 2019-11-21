
import unittest, sys, os
from src.server import bootstrap
from pactman import Consumer, Provider
sys.path.append(f"{sys.path[0]}/src")

# set var for mock service
os.environ["ZENODO_ADDRESS"] = "http://localhost:5000"
def create_app():

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


