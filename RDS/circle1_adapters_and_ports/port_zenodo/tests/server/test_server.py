import unittest
import sys
import os
from pactman import Consumer, Provider
from constant import req, result as reqResult

api_key = os.getenv("ZENODO_API_KEY", default=None)


def create_app():
    from src import bootstrap

    # creates a test client
    app = bootstrap(use_default_error=True, address="http://localhost:3000").app
    # propagate the exceptions to the test client
    app.config.update({"TESTING": True})

    return app


pact = Consumer("PortZenodo").has_pact_with(Provider("Zenodo"), port=3000)

unittest.TestCase.maxDiff = None


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
                "service": {"data": {"servicename": "Zenodo"}},
            },
        }

        projectId = 5

        pact.given("user admin has a token in rds").upon_receiving(
            "the currently available token"
        ).with_request("GET", "/user/admin/service/Zenodo").will_respond_with(
            200, body=admintoken
        )

        pact.given("user admin exists in zenodo").upon_receiving(
            "user has no deposit"
        ).with_request("GET", "/api/deposit/depositions").will_respond_with(
            200, body=expected
        )

        result = None
        with pact:
            data = {"userId": "zenodo://user:ASD123GANZSICHA"}
            result = self.client.get("/metadata/project", json=data)

        self.assertEqual(result.json, expected)

        expected = []

        pact.given("user admin has a token in rds").upon_receiving(
            "the currently available token"
        ).with_request("GET", "/user/admin/service/Zenodo").will_respond_with(
            200, body=admintoken
        )

        pact.given("user admin exists in zenodo").upon_receiving(
            "user has no deposit"
        ).with_request("GET", "/api/deposit/depositions").will_respond_with(
            200, body=expected
        )

        result = None
        with pact:
            data = {"userId": "zenodo://user:ASD123GANZSICHA"}
            result = self.client.get(f"/metadata/project/{projectId}", json=data)

        self.assertEqual(result.json, expected)

    def test_without_apikey(self):
        """
        This test try to get something without apiKey, but this should be a Bad request.
        """

        expected = {
            "message": "The server could not verify that you are authorized to "
            "access the URL requested.  You either supplied the wrong "
            "credentials (e.g. a bad password), or your browser "
            "doesn't understand how to supply the credentials "
            "required.",
            "status": 401,
        }

        pact.given("user admin not exists in zenodo").upon_receiving(
            "user has no deposit"
        ).with_request("GET", "/api/deposit/depositions").will_respond_with(
            401, body=expected
        )

        with pact:
            result = self.client.get("/metadata/project")
            self.assertEqual(result.status_code, 400, msg=result.json)

    def test_with_invalid_apikey(self):
        expected = {
            "message": "The server could not verify that you are authorized to "
            "access the URL requested.  You either supplied the wrong "
            "credentials (e.g. a bad password), or your browser "
            "doesn't understand how to supply the credentials "
            "required.",
            "status": 401,
        }

        pact.given("user admin not exists in zenodo").upon_receiving(
            "user has no deposit"
        ).with_request("GET", "/api/deposit/depositions").will_respond_with(
            401, body=expected
        )

        with pact:
            data = {"userId": "zenodo://user:ASD123GANZSICHA"}
            result = self.client.get("/metadata/project", json=data)
            self.assertEqual(result.status_code, 401, msg=result.json)

    def test_projectId_not_found(self):
        expected = {"message": "Deposition not found", "status": 404}

        projectId = 5

        pact.given("projectId not exists in zenodo").upon_receiving(
            "user has no deposit"
        ).with_request(
            "GET", f"/api/deposit/depositions/{projectId}"
        ).will_respond_with(
            404, body=expected
        )

        with pact:
            data = {"userId": "zenodo://user:ASD123GANZSICHA"}
            result = self.client.get(f"/metadata/project/{projectId}", json=data)
            self.assertEqual(result.status_code, 404, msg=result.json)

    def test_index_metadata(self):
        projectId = 1234
        expected_body = {
            "created": "2016-06-15T16:10:03.319363+00:00",
            "files": [],
            "id": projectId,
            "links": {
                "discard": "https://zenodo.org/api/deposit/depositions/1234/actions/discard",
                "edit": "https://zenodo.org/api/deposit/depositions/1234/actions/edit",
                "files": "https://zenodo.org/api/deposit/depositions/1234/files",
                "publish": "https://zenodo.org/api/deposit/depositions/1234/actions/publish",
                "newversion": "https://zenodo.org/api/deposit/depositions/1234/actions/newversion",
                "self": "https://zenodo.org/api/deposit/depositions/1234",
            },
            "metadata": {
                "prereserve_doi": {"doi": "10.5072/zenodo.1234", "recid": projectId}
            },
            "modified": "2016-06-15T16:10:03.319371+00:00",
            "owner": 1,
            "record_id": projectId,
            "state": "unsubmitted",
            "submitted": False,
            "title": "",
        }

        pact.given("access token is valid").upon_receiving(
            "the corresponding user has one deposit as list"
        ).with_request("GET", "/api/deposit/depositions").will_respond_with(
            200, body=[expected_body]
        )

        with pact:
            data = {"userId": "zenodo://user:ASD123GANZSICHA"}
            result = self.client.get("/metadata/project", json=data)
            self.assertEqual(result.status_code, 200)
            self.assertEqual(
                result.json,
                [{"projectId": str(projectId), "metadata": expected_body["metadata"]}],
            )

        expected_body = {
            "created": "2016-06-15T16:10:03.319363+00:00",
            "files": [],
            "id": projectId,
            "links": {
                "discard": "https://zenodo.org/api/deposit/depositions/1234/actions/discard",
                "edit": "https://zenodo.org/api/deposit/depositions/1234/actions/edit",
                "files": "https://zenodo.org/api/deposit/depositions/1234/files",
                "publish": "https://zenodo.org/api/deposit/depositions/1234/actions/publish",
                "newversion": "https://zenodo.org/api/deposit/depositions/1234/actions/newversion",
                "self": "https://zenodo.org/api/deposit/depositions/1234",
            },
            "metadata": {
                "access_right": "open",
                "creators": [
                    {"affiliation": "WWU", "name": "Peter Heiss"},
                    {"name": "Jens Stegmann"},
                ],
                "description": "Beispieltest. Ganz viel<br><br>asd mit umbruch",
                "doi": "",
                "image_type": "drawing",
                "license": "CC-BY-4.0",
                "prereserve_doi": {"doi": "10.5072/zenodo.662835", "recid": 662835},
                "publication_date": "2020-09-29",
                "title": "testtitle123",
                "upload_type": "image",
            },
            "modified": "2016-06-15T16:10:03.319371+00:00",
            "owner": 1,
            "record_id": projectId,
            "state": "unsubmitted",
            "submitted": False,
            "title": "",
        }

        pact.given("access token is valid 2").upon_receiving(
            "the corresponding user has one deposit as list 2"
        ).with_request("GET", "/api/deposit/depositions").will_respond_with(
            200, body=[expected_body]
        )

        with pact:
            data = {"userId": "zenodo://user:ASD123GANZSICHA"}
            result = self.client.get("/metadata/project", json=data)
            self.assertEqual(result.status_code, 200)
            self.assertNotEqual(
                result.json,
                [{"projectId": str(projectId), "metadata": expected_body["metadata"]}],
            )

    def test_get_metadata(self):
        projectId = 5

        expected_body = {
            "projectId": projectId,
            "metadata": {
                "created": "2016-06-15T16:10:03.319363+00:00",
                "files": [],
                "id": 1234,
                "links": {
                    "discard": "https://zenodo.org/api/deposit/depositions/1234/actions/discard",
                    "edit": "https://zenodo.org/api/deposit/depositions/1234/actions/edit",
                    "files": "https://zenodo.org/api/deposit/depositions/1234/files",
                    "publish": "https://zenodo.org/api/deposit/depositions/1234/actions/publish",
                    "newversion": "https://zenodo.org/api/deposit/depositions/1234/actions/newversion",
                    "self": "https://zenodo.org/api/deposit/depositions/1234",
                },
                "metadata": {
                    "prereserve_doi": {"doi": "10.5072/zenodo.1234", "recid": 1234}
                },
                "modified": "2016-06-15T16:10:03.319371+00:00",
                "owner": 1,
                "record_id": 1234,
                "state": "unsubmitted",
                "submitted": False,
                "title": "",
            },
        }

        pact.given("access token is valid").upon_receiving(
            "the corresponding user has a deposit"
        ).with_request(
            "GET", f"/api/deposit/depositions/{projectId}"
        ).will_respond_with(
            200, body=expected_body
        )

        with pact:
            data = {"userId": "zenodo://user:ASD123GANZSICHA"}
            result = self.client.get(f"/metadata/project/{projectId}", json=data)
            self.assertEqual(result.status_code, 200)
            self.assertEqual(result.json, expected_body["metadata"])

        expected_body = {
            "projectId": projectId,
            "metadata": {
                "created": "2016-06-15T16:10:03.319363+00:00",
                "files": [],
                "id": 1234,
                "links": {
                    "discard": "https://zenodo.org/api/deposit/depositions/1234/actions/discard",
                    "edit": "https://zenodo.org/api/deposit/depositions/1234/actions/edit",
                    "files": "https://zenodo.org/api/deposit/depositions/1234/files",
                    "publish": "https://zenodo.org/api/deposit/depositions/1234/actions/publish",
                    "newversion": "https://zenodo.org/api/deposit/depositions/1234/actions/newversion",
                    "self": "https://zenodo.org/api/deposit/depositions/1234",
                },
                "metadata": {
                    "access_right": "open",
                    "creators": [
                        {"affiliation": "WWU", "name": "Peter Heiss"},
                        {"name": "Jens Stegmann"},
                    ],
                    "description": "Beispieltest. Ganz viel<br><br>asd mit umbruch",
                    "doi": "",
                    "image_type": "drawing",
                    "license": "CC-BY-4.0",
                    "prereserve_doi": {
                        "doi": "10.5072/zenodo.662835",
                        "recid": 662835,
                    },
                    "publication_date": "2020-09-29",
                    "title": "testtitle123",
                    "upload_type": "image",
                },
                "modified": "2016-06-15T16:10:03.319371+00:00",
                "owner": 1,
                "record_id": 1234,
                "state": "unsubmitted",
                "submitted": False,
                "title": "",
            },
        }

        pact.given("access token is valid 2").upon_receiving(
            "the corresponding user has a deposit 2"
        ).with_request(
            "GET", f"/api/deposit/depositions/{projectId}"
        ).will_respond_with(
            200, body=expected_body
        )

        with pact:
            data = {"userId": "zenodo://user:ASD123GANZSICHA"}
            result = self.client.get(f"/metadata/project/{projectId}", json=data)
            self.assertEqual(result.status_code, 200)
            self.assertNotEqual(result.json, expected_body["metadata"])

    def test_patch_metadata(self):
        projectId = 5

        expected_body = {
            "created": "2016-06-15T16:10:03.319363+00:00",
            "files": [],
            "id": 1234,
            "links": {
                "discard": "https://zenodo.org/api/deposit/depositions/1234/actions/discard",
                "edit": "https://zenodo.org/api/deposit/depositions/1234/actions/edit",
                "files": "https://zenodo.org/api/deposit/depositions/1234/files",
                "publish": "https://zenodo.org/api/deposit/depositions/1234/actions/publish",
                "newversion": "https://zenodo.org/api/deposit/depositions/1234/actions/newversion",
                "self": "https://zenodo.org/api/deposit/depositions/1234",
            },
            "metadata": {
                "prereserve_doi": {"doi": "10.5072/zenodo.1234", "recid": 1234}
            },
            "modified": "2016-06-15T16:10:03.319371+00:00",
            "owner": 1,
            "record_id": 1234,
            "state": "unsubmitted",
            "submitted": False,
            "title": "",
        }

        updated_metadata = {
            "prereserve_doi": {"doi": "10.5072/zenodo.1234", "recid": 1234},
            "title": "My first upload",
            "upload_type": "poster",
            "description": "This is my first upload",
            "creators": [{"name": "Doe, John", "affiliation": "Zenodo"}],
        }

        result_metadata = {
            "https://schema.org/creator": [
                {
                    "https://schema.org/affiliation": "Zenodo",
                    "https://schema.org/name": "Doe, John",
                }
            ],
            "https://schema.org/description": "This is my first upload",
            "https://schema.org/identifier": 1234,
            "https://schema.org/publicAccess": True,
            "https://schema.org/name": "My first upload",
            "https://www.research-data-services.org/jsonld/zenodocategory": "poster",
            "https://www.research-data-services.org/jsonld/doi": "10.5072/zenodo.1234",
        }

        expected_body["metadata"] = updated_metadata

        pact.given("access token is valid").upon_receiving(
            "the corresponding user has an updated deposit"
        ).with_request(
            "PUT", f"/api/deposit/depositions/{projectId}"
        ).will_respond_with(
            200, body=expected_body
        )

        with pact:
            data = {"userId": "zenodo://user:ASD123GANZSICHA"}
            result = self.client.patch(f"/metadata/project/{projectId}", json=data)
            self.assertEqual(result.status_code, 200)
            self.assertEqual(result.json, result_metadata)

        pact.given("access token is valid").upon_receiving(
            "the corresponding user has an updated deposit and has a title metadata"
        ).with_request(
            "PUT", f"/api/deposit/depositions/{projectId}"
        ).will_respond_with(
            200, body=expected_body
        )

        with pact:
            data = {"userId": "zenodo://user:ASD123GANZSICHA", "metadata": {"title": ""}}
            result = self.client.patch(f"/metadata/project/{projectId}", json=data)
            self.assertEqual(result.status_code, 200)
            self.assertEqual(result.json, result_metadata)

    def test_delete_metadata(self):
        projectId = 5

        pact.given("access token is valid").upon_receiving(
            "the corresponding user has a deposit which can be deleted"
        ).with_request(
            "DELETE", f"/api/deposit/depositions/{projectId}"
        ).will_respond_with(
            201, body=""
        )

        with pact:
            data = {"userId": "zenodo://user:ASD123GANZSICHA"}
            result = self.client.delete(f"/metadata/project/{projectId}", json=data)
            self.assertEqual(result.status_code, 204)

    def test_create_metadata(self):
        expected_body = {
            "created": "2016-06-15T16:10:03.319363+00:00",
            "files": [],
            "id": 1234,
            "links": {
                "discard": "https://zenodo.org/api/deposit/depositions/1234/actions/discard",
                "edit": "https://zenodo.org/api/deposit/depositions/1234/actions/edit",
                "files": "https://zenodo.org/api/deposit/depositions/1234/files",
                "publish": "https://zenodo.org/api/deposit/depositions/1234/actions/publish",
                "newversion": "https://zenodo.org/api/deposit/depositions/1234/actions/newversion",
                "self": "https://zenodo.org/api/deposit/depositions/1234",
            },
            "metadata": {
                "prereserve_doi": {"doi": "10.5072/zenodo.1234", "recid": 1234}
            },
            "modified": "2016-06-15T16:10:03.319371+00:00",
            "owner": 1,
            "record_id": 1234,
            "state": "unsubmitted",
            "submitted": False,
            "title": "",
        }

        pact.given("access token is valid").upon_receiving(
            "the corresponding user can create a deposit."
        ).with_request("POST", "/api/deposit/depositions").will_respond_with(
            201, body=expected_body
        )

        with pact:
            data = {"userId": "zenodo://user:ASD123GANZSICHA"}
            result = self.client.post("/metadata/project", json=data)
            self.assertEqual(result.status_code, 200)

        pact.given("access token is valid").upon_receiving(
            "the corresponding user can create a next deposit"
        ).with_request("POST", "/api/deposit/depositions").will_respond_with(
            201, body=expected_body
        )

        updated_metadata = {
            "title": "My first upload",
            "upload_type": "poster",
            "description": "This is my first upload",
            "creators": [{"name": "Doe, John", "affiliation": "Zenodo"}],
        }

        expected_body["metadata"] = updated_metadata

        pact.given("access token is valid").upon_receiving(
            "the corresponding user can update the newly created deposit"
        ).with_request(
            "PUT", f'/api/deposit/depositions/{expected_body["id"]}'
        ).will_respond_with(
            200, body=expected_body
        )

        with pact:
            data = {"userId": "zenodo://user:ASD123GANZSICHA", "metadata": updated_metadata}
            result = self.client.post("/metadata/project", json=data)
            self.assertEqual(result.status_code, 200)

    @unittest.skipIf(api_key is None, "no api key were given")
    @unittest.skip
    def test_create_deposition_and_upload_file(self):

        pact.given("user admin has a token in rds").upon_receiving(
            "the currently available token"
        ).with_request("GET", "/user/admin/service/Zenodo").will_respond_with(
            200,
            body={
                "data": {
                    "access_token": api_key,
                    "service": {"data": {"servicename": "Zenodo"}},
                }
            },
        )

        result = None
        with pact:
            data = {"userId": "admin"}
            result = self.client.get("/metadata/project", data=data)

        self.assertEqual(result.json, {"success": True})

    def test_metadata_get_jsonld_missing(self):
        import json

        projectId = 5

        incomplete = {
            "prereserve_doi": {"doi": "10.5072/zenodo.1234", "recid": 1234},
        }

        complete = {
            "title": "My first upload",
            "upload_type": "poster",
            "description": "This is my first upload",
            "creators": [{"name": "Doe, John", "affiliation": "Zenodo"}],
            "prereserve_doi": {"doi": "10.5072/zenodo.1234", "recid": 1234},
        }

        expected_body = {
            "created": "2016-06-15T16:10:03.319363+00:00",
            "files": [],
            "id": 1234,
            "links": {
                "discard": "https://zenodo.org/api/deposit/depositions/1234/actions/discard",
                "edit": "https://zenodo.org/api/deposit/depositions/1234/actions/edit",
                "files": "https://zenodo.org/api/deposit/depositions/1234/files",
                "publish": "https://zenodo.org/api/deposit/depositions/1234/actions/publish",
                "newversion": "https://zenodo.org/api/deposit/depositions/1234/actions/newversion",
                "self": "https://zenodo.org/api/deposit/depositions/1234",
            },
            "metadata": complete,
            "modified": "2016-06-15T16:10:03.319371+00:00",
            "owner": 1,
            "record_id": 1234,
            "state": "unsubmitted",
            "submitted": False,
            "title": "",
        }

        metadata = {
            "https://schema.org/creator": [
                {
                    "https://schema.org/affiliation": "Zenodo",
                    "https://schema.org/name": "Doe, John",
                }
            ],
            "https://www.research-data-services.org/jsonld/zenodocategory": "poster",
            "https://schema.org/name": "My first upload",
            "https://schema.org/description": "This is my first upload",
            "https://www.research-data-services.org/jsonld/doi": "10.5072/zenodo.1234",
            "https://schema.org/identifier": 1234,
            "https://schema.org/publicAccess": True,
        }

        pact.given("access token is valid").upon_receiving(
            "the corresponding user has an deposit no metadata"
        ).with_request(
            "GET", f"/api/deposit/depositions/{projectId}"
        ).will_respond_with(
            200, body=expected_body
        )

        # should return jsonld
        with pact:
            data = {"userId": "zenodo://user:ASD123GANZSICHA"}
            result = self.client.get(f"/metadata/project/{projectId}", json=data)
            self.assertEqual(result.status_code, 200)
            self.assertEqual(result.json, metadata)

        expected_body["metadata"] = incomplete

        pact.given("access token is valid").upon_receiving(
            "the corresponding user has a deposit with full metadata"
        ).with_request(
            "GET", f"/api/deposit/depositions/{projectId}"
        ).will_respond_with(
            200, body=expected_body
        )

        # should return zenodo specific api dataset, because there was an error in transfomration
        with pact:
            data = {"userId": "zenodo://user:ASD123GANZSICHA"}
            result = self.client.get(f"/metadata/project/{projectId}", json=data)
            self.assertEqual(result.status_code, 200)
            self.assertEqual(result.json, expected_body["metadata"])

    def test_metadata_update_jsonld_complete(self):
        import json

        metadata = {
            "https://schema.org/creator": [
                {
                    "https://schema.org/affiliation": "Zenodo",
                    "https://schema.org/name": "Doe, John",
                }
            ],
            "https://schema.org/description": "This is my first upload",
            "https://schema.org/identifier": 1234,
            "https://schema.org/publicAccess": True,
            "https://schema.org/name": "My first upload",
            "https://www.research-data-services.org/jsonld/zenodocategory": "poster",
            "https://www.research-data-services.org/jsonld/doi": "10.5072/zenodo.1234",
        }

        projectId = 5

        expected_body = {
            "created": "2016-06-15T16:10:03.319363+00:00",
            "files": [],
            "id": 1234,
            "links": {
                "discard": "https://zenodo.org/api/deposit/depositions/1234/actions/discard",
                "edit": "https://zenodo.org/api/deposit/depositions/1234/actions/edit",
                "files": "https://zenodo.org/api/deposit/depositions/1234/files",
                "publish": "https://zenodo.org/api/deposit/depositions/1234/actions/publish",
                "newversion": "https://zenodo.org/api/deposit/depositions/1234/actions/newversion",
                "self": "https://zenodo.org/api/deposit/depositions/1234",
            },
            "metadata": {
                "title": "My first upload",
                "upload_type": "poster",
                "description": "This is my first upload",
                "creators": [{"name": "Doe, John", "affiliation": "Zenodo"}],
                "prereserve_doi": {"doi": "10.5072/zenodo.1234", "recid": 1234},
            },
            "modified": "2016-06-15T16:10:03.319371+00:00",
            "owner": 1,
            "record_id": 1234,
            "state": "unsubmitted",
            "submitted": False,
            "title": "",
        }

        pact.given("access token is valid").upon_receiving(
            "the corresponding user has an updated deposit with"
        ).with_request(
            "PUT", f"/api/deposit/depositions/{projectId}"
        ).will_respond_with(
            200, body=expected_body
        )

        expected_body["metadata"] = metadata

        with pact:
            data = {"metadata": metadata, "userId": "zenodo://user:ASD123GANZSICHA"}
            result = self.client.patch(f"/metadata/project/{projectId}", json=data)
            self.assertEqual(result.status_code, 200)
            self.assertEqual(result.json, expected_body["metadata"])


if __name__ == "__main__":
    unittest.main()
