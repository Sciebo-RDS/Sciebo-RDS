
import unittest
import sys
import os
from pactman import Consumer, Provider

api_key = os.getenv("ZENODO_API_KEY", default=None)


def create_app():
    from src import bootstrap
    # creates a test client
    app = bootstrap(use_default_error=True,
                    address="http://localhost:3000").app
    # propagate the exceptions to the test client
    app.config.update({"TESTING": True})

    return app


pact = Consumer('PortZenodo').has_pact_with(Provider('Zenodo'), port=3000)


class TestPortZenodo(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    @classmethod
    def tearDownClass(cls):
        pass

    def tearDown(self):
        pass

    def test_home_status_code(self):
        expected = []

        pact.given(
            'user admin has a token in rds'
        ).upon_receiving(
            'the currently available token'
        ).with_request(
            'GET', '/user/admin/service/Zenodo'
        ) .will_respond_with(200, body={"data": {"access_token": "ASD123GANZSICHA", "service": {"data": {"servicename": "Zenodo"}}}})

        pact.given(
            'user admin exists in zenodo'
        ).upon_receiving(
            'user has no deposit'
        ).with_request(
            'GET', '/api/deposit/depositions'
        ) .will_respond_with(200, body=expected)

        result = None
        with pact:
            data = {"userId": "admin"}
            result = self.client.get("/use_case/deposition", data=data)

        self.assertEqual(result.json, expected)

    def test_get_token_for_userid(self):
        result = None
        with pact:
            result = self.client.get("/use_case/deposition")

        self.assertEqual(result.status_code, 401)

        pact.given(
            'user "user" has no token in rds'
        ).upon_receiving(
            'error message, no user found'
        ).with_request(
            'GET', '/user/user/service/Zenodo'
        ) .will_respond_with(500, body={"error": "Exception", "http_code": 500})

        result = None
        with pact:
            data = {"userId": "user"}
            result = self.client.get("/use_case/deposition", data=data)

        self.assertEqual(result.status_code, 401)

    @unittest.skipIf(api_key is None, "no api key were given")
    @unittest.skip
    def test_create_deposition_and_upload_file(self):

        pact.given(
            'user admin has a token in rds'
        ).upon_receiving(
            'the currently available token'
        ).with_request(
            'GET', '/user/admin/service/Zenodo'
        ) .will_respond_with(200, body={"data": {"access_token": api_key, "service": {"data": {"servicename": "Zenodo"}}}})

        result = None
        with pact:
            data = {"userId": "admin"}
            result = self.client.get("/use_case/deposition", data=data)

        self.assertEqual(result.json, {"success": True})


if __name__ == '__main__':
    unittest.main()
