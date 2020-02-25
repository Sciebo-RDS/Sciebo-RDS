import unittest
from src.lib.ExporterService import ExporterService
from pactman import Consumer, Provider


def create_app():
    from src import bootstrap
    # creates a test client
    app = bootstrap(use_default_error=True).app
    # propagate the exceptions to the test client
    app.config.update({"TESTING": True, "TESTSERVER": "http://localhost:3000"})

    return app


pact = Consumer('PortZenodo').has_pact_with(Provider('Zenodo'), port=3000)


class Test_ExporterService(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    @unittest.skip
    def test_export_zenodo_from_owncloud_working(self):
        exporter = ExporterService(testing=True, testing_address=self.app.config.get("TESTSERVER"))

        # call to get file from owncloud
        pact.given(
            'file and userid are valid'
        ).upon_receiving(
            'the wanted file content'
        ).with_request(
            'GET', '/file/testfile.txt'
        ) .will_respond_with(200, body="Lorem Ipsum")

        # call to create depo in zenodo
        pact.given(
            'userId is valid'
        ).upon_receiving(
            'create a new deposition'
        ).with_request(
            'POST', '/deposition'
        ) .will_respond_with(200, body={"depositionId": 1234})

        # call to push file to zenodo
        pact.given(
            'userId is valid'
        ).upon_receiving(
            'push the file to the new deposition successfully'
        ).with_request(
            'POST', '/deposition/1234/actions/upload',
            headers={'Content-Type': 'application/form-data'}
        ) .will_respond_with(200, body={"success": True})

        with pact:
            result = exporter.export(
                "Owncloud", "Zenodo", "testfile.txt", "admin")
        self.assertTrue(result)

    def test_export_zenodo_from_owncloud_unknown(self):
        exporter = ExporterService(testing=True)

        with self.assertRaises(ValueError):
            exporter.export(
                "not-known", "Zenodo", "testfile.txt", "admin")

        with self.assertRaises(ValueError):
            exporter.export(
                "Owncloud", "not-known", "testfile.txt", "admin")

    def test_export_zenodo_from_owncloud_no_token_for_service_from(self):
        exporter = ExporterService(testing=True)

        # call to get file from owncloud
        pact.given(
            'file is valid, but userId is not'
        ).upon_receiving(
            'corresponding error message'
        ).with_request(
            'GET', '/file/testfile.txt'
        ) .will_respond_with(401, body={"error": "Exception", "http_code": 401})

        with pact:
            result = exporter.export(
                "Owncloud", "Zenodo", "testfile.txt", "admin")
        self.assertFalse(result)

    def test_export_zenodo_from_owncloud_no_token_for_service_to(self):
        exporter = ExporterService(testing=True)

        # call to get file from owncloud
        pact.given(
            'file and userid is valid'
        ).upon_receiving(
            'returns file content'
        ).with_request(
            'GET', '/file/testfile.txt'
        ) .will_respond_with(200, body="Lorem Ipsum")

        # call to create depo in zenodo
        pact.given(
            'userId is valid'
        ).upon_receiving(
            'corresponding error message'
        ).with_request(
            'POST', '/deposition'
        ) .will_respond_with(401, body={"error": "Unauthorized", "http_code": 401})

        with pact:
            result = exporter.export(
                "Owncloud", "Zenodo", "testfile.txt", "admin")
        self.assertFalse(result)

    # TODO: this test cannot be handled, because pactman can only emulate json, nothing else.
    @unittest.skip
    def test_export_server(self):
        # call to get file from owncloud
        pact.given(
            'file and userid are valid'
        ).upon_receiving(
            'the wanted file content'
        ).with_request(
            'GET', '/file/testfile.txt'
        ) .will_respond_with(200, body="Lorem Ipsum")

        # call to create depo in zenodo
        pact.given(
            'userId is valid'
        ).upon_receiving(
            'create a new deposition'
        ).with_request(
            'POST', '/deposition'
        ) .will_respond_with(200, body={"depositionId": 1234})

        # call to push file to zenodo
        pact.given(
            'userId is valid'
        ).upon_receiving(
            'push the file to the new deposition successfully'
        ).with_request(
            'POST', '/deposition/1234/actions/upload',
            headers={'Content-Type': 'application/form-data'}
        ) .will_respond_with(200, body={"success": True})

        with pact:
            result = self.client.post("/exporter/export/Zenodo", data={"user_id": "admin", "from_service":"Owncloud", "filename":"testfile.txt"})
        self.assertEqual(result.json, {"success": True})
