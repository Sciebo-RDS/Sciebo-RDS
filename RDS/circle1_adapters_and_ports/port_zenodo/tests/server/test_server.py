
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

    @unittest.skip("skip")
    def test_home_status_code_json(self):
        expected = []

        user = "admin"
        admintoken = {
            "type": "OAuth2Token",
            "data": {
                "access_token": "ASD123GANZSICHA",
                "user": user,
                "service": {
                    "data": {
                        "servicename": "Zenodo"
                    }
                }
            }
        }

        projectId = 5

        pact.given(
            'user admin has a token in rds'
        ).upon_receiving(
            'the currently available token'
        ).with_request(
            'GET', '/user/admin/service/Zenodo'
        ) .will_respond_with(200, body=admintoken)

        pact.given(
            'user admin exists in zenodo'
        ).upon_receiving(
            'user has no deposit'
        ).with_request(
            'GET', '/api/deposit/depositions'
        ) .will_respond_with(200, body=expected)

        result = None
        with pact:
            data = {"apiKey": "ASD123GANZSICHA"}
            result = self.client.get(
                "/metadata/project", json=data)

        self.assertEqual(result.json, expected)

        expected = []

        pact.given(
            'user admin has a token in rds'
        ).upon_receiving(
            'the currently available token'
        ).with_request(
            'GET', '/user/admin/service/Zenodo'
        ) .will_respond_with(200, body=admintoken)

        pact.given(
            'user admin exists in zenodo'
        ).upon_receiving(
            'user has no deposit'
        ).with_request(
            'GET', '/api/deposit/depositions'
        ) .will_respond_with(200, body=expected)

        result = None
        with pact:
            data = {"apiKey": "ASD123GANZSICHA"}
            result = self.client.get(
                f"/metadata/project/{projectId}", json=data)

        self.assertEqual(result.json, expected)

    def test_without_apikey(self):
        """
        This test try to get something without apiKey, but this should be a Bad request.
        """

        expected = {'message': 'The server could not verify that you are authorized to '
                    'access the URL requested.  You either supplied the wrong '
                    'credentials (e.g. a bad password), or your browser '
                    "doesn't understand how to supply the credentials "
                    'required.',
                    'status': 401}

        pact.given(
            'user admin not exists in zenodo'
        ).upon_receiving(
            'user has no deposit'
        ).with_request(
            'GET', '/api/deposit/depositions'
        ) .will_respond_with(401, body=expected)

        with pact:
            result = self.client.get("/metadata/project")
            self.assertEqual(result.status_code, 400, msg=result.json)

    def test_with_invalid_apikey(self):
        expected = {'message': 'The server could not verify that you are authorized to '
                    'access the URL requested.  You either supplied the wrong '
                    'credentials (e.g. a bad password), or your browser '
                    "doesn't understand how to supply the credentials "
                    'required.',
                    'status': 401}

        pact.given(
            'user admin not exists in zenodo'
        ).upon_receiving(
            'user has no deposit'
        ).with_request(
            'GET', '/api/deposit/depositions'
        ) .will_respond_with(401, body=expected)

        with pact:
            data = {"apiKey": "ASD123GANZSICHA"}
            result = self.client.get("/metadata/project", json=data)
            self.assertEqual(result.status_code, 401, msg=result.json)

    def test_projectId_not_found(self):
        expected = {
            "message": "Deposition not found",
            "status": 404
        }

        projectId = 5

        pact.given(
            'projectId not exists in zenodo'
        ).upon_receiving(
            'user has no deposit'
        ).with_request(
            'GET', f'/api/deposit/depositions/{projectId}'
        ) .will_respond_with(404, body=expected)

        with pact:
            data = {"apiKey": "ASD123GANZSICHA"}
            result = self.client.get(
                f"/metadata/project/{projectId}", json=data)
            self.assertEqual(result.status_code, 404, msg=result.json)

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
            result = self.client.get("/metadata/project", data=data)

        self.assertEqual(result.json, {"success": True})


if __name__ == '__main__':
    unittest.main()
