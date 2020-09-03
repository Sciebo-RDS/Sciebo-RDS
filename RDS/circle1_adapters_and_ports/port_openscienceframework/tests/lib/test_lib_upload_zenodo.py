import unittest
import sys
import os
from lib.upload_zenodo import Zenodo
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


class TestZenodoMethods(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_check_token(self):
        """
        Checks, if the given token is valid.
        """

        pact.given(
            'access token is valid'
        ).upon_receiving(
            'the corresponding user has no depositions'
        ).with_request(
            'GET', '/api/deposit/depositions'
        ) .will_respond_with(200, body=[])

        expected = True
        with pact:
            result = Zenodo.check_token(
                api_key, address="http://localhost:3000")
        self.assertEqual(result, expected)

        # check if acces token is invalid
        pact.given(
            'access token is invalid'
        ).upon_receiving(
            'the corresponding error message'
        ).with_request(
            'GET', '/api/deposit/depositions'
        ) .will_respond_with(401, body={
            "message": """The server could not verify that you are authorized to access the URL requested.
            You either supplied the wrong credentials (e.g. a bad password),
            or your browser doesn't understand how to supply the credentials required.""",
            "status": 401
        })

        expected = False
        with pact:
            result = Zenodo.check_token(
                api_key, address="http://localhost:3000")
        self.assertEqual(result, expected)

    def test_create_new_empty_deposit(self):
        """
        Create a new deposition
        """

        # create new deposition
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
                "self": "https://zenodo.org/api/deposit/depositions/1234"
            },
            "metadata": {
                "prereserve_doi": {
                    "doi": "10.5072/zenodo.1234",
                    "recid": 1234
                }
            },
            "modified": "2016-06-15T16:10:03.319371+00:00",
            "owner": 1,
            "record_id": 1234,
            "state": "unsubmitted",
            "submitted": False,
            "title": ""
        }

        pact.given(
            'access token is valid'
        ).upon_receiving(
            'the corresponding user creates a deposit'
        ).with_request(
            'POST', '/api/deposit/depositions'
        ) .will_respond_with(201, body=expected_body)

        with pact:
            result = Zenodo(
                api_key, address="http://localhost:3000").create_new_deposition()
        self.assertEqual(result, expected_body)

    def test_metadata_filter(self):
        """
        Filter metadata
        """

        # create new file
        expected_body = [{
            "created": "2016-06-15T16:10:03.319363+00:00",
            "files": [],
            "id": 1234,
            "links": {
                "discard": "https://zenodo.org/api/deposit/depositions/1234/actions/discard",
                "edit": "https://zenodo.org/api/deposit/depositions/1234/actions/edit",
                "files": "https://zenodo.org/api/deposit/depositions/1234/files",
                "publish": "https://zenodo.org/api/deposit/depositions/1234/actions/publish",
                "newversion": "https://zenodo.org/api/deposit/depositions/1234/actions/newversion",
                "self": "https://zenodo.org/api/deposit/depositions/1234"
            },
            'metadata': {
                'title': 'My first upload',
                'upload_type': 'poster',
                'description': 'This is my first upload',
                'creators': [{'name': 'Doe, John',
                              'affiliation': 'Zenodo'}]
            },
            "modified": "2016-06-15T16:10:03.319371+00:00",
            "owner": 1,
            "record_id": 1234,
            "state": "unsubmitted",
            "submitted": False,
            "title": ""
        }]

        pact.given(
            'access token is valid'
        ).upon_receiving(
            'the corresponding user has a deposit'
        ).with_request(
            'GET', '/api/deposit/depositions'
        ) .will_respond_with(201, body=expected_body)

        filter = {"title": ""}

        expected = {"title": expected_body[0]["metadata"]["title"]}
        with pact:
            result = Zenodo(
                api_key, address="http://localhost:3000").get_deposition(metadataFilter=filter)
        self.assertEqual(result, expected)

        filter = {"title": "", "description": ""}

        pact.given(
            'access token is valid'
        ).upon_receiving(
            'the corresponding user has a deposit'
        ).with_request(
            'GET', '/api/deposit/depositions'
        ) .will_respond_with(201, body=expected_body)

        expected = {"title": expected_body[0]["metadata"]["title"],
                    "description": expected_body[0]["metadata"]["description"]}
        with pact:
            result = Zenodo(
                api_key, address="http://localhost:3000").get_deposition(metadataFilter=filter)
        self.assertEqual(result, expected)

    @unittest.skip("Currently pactman does not support other content types as json")
    def test_upload_file(self):
        """
        Test the upload functions
        """
        projectId = 5

        from hashlib import md5
        import os

        filepath = "src/lib/upload_zenodo.py"
        file = open(os.path.expanduser(filepath), 'rb')
        hash = md5(file.read()).hexdigest()

        expected_body = {
            "checksum": hash,
            "name": os.path.basename(filepath),
            "id": "eb78d50b-ecd4-407a-9520-dfc7a9d1ab2c",
            "filesize": os.path.getsize(filepath)
        }

        pact.given(
            'access token is valid'
        ).upon_receiving(
            'the uploaded file'
        ).with_request(
            'POST', f'/api/deposit/depositions/{projectId}/files'
        ) .will_respond_with(201, body=expected_body)

        # add a file to deposition
        with pact:
            result = Zenodo(
                api_key, address="http://localhost:3000").upload_new_file_to_deposition(
                deposition_id=id, path_to_file=filepath)

        # file was uploaded
        self.assertTrue(result)

    def test_get_files(self):
        """
        Test the files list in depositions
        """
        projectId = 5

        expected_body = []

        pact.given(
            'access token is valid'
        ).upon_receiving(
            'empty fileslist'
        ).with_request(
            'GET', f'/api/deposit/depositions/{projectId}/files'
        ) .will_respond_with(200, body=expected_body)

        # add a file to deposition
        with pact:
            result = Zenodo(
                api_key, address="http://localhost:3000").get_files_from_deposition(
                deposition_id=projectId)

        self.assertEqual(result, expected_body)

        from hashlib import md5
        import os

        filepath = "src/lib/upload_zenodo.py"
        file = open(os.path.expanduser(filepath), 'rb')
        hash = md5(file.read()).hexdigest()

        expected_body = [{
            "checksum": hash,
            "name": os.path.basename(filepath),
            "id": "eb78d50b-ecd4-407a-9520-dfc7a9d1ab2c",
            "filesize": os.path.getsize(filepath)
        }]

        pact.given(
            'access token is valid'
        ).upon_receiving(
            'the deposition holds one file'
        ).with_request(
            'GET', f'/api/deposit/depositions/{projectId}/files'
        ) .will_respond_with(200, body=expected_body)

        # add a file to deposition
        with pact:
            result = Zenodo(
                api_key, address="http://localhost:3000").get_files_from_deposition(
                deposition_id=projectId)

        # file was uploaded
        self.assertEqual(result, expected_body)

    @unittest.skipIf(api_key is None, "no api key were given")
    def test_create_new_empty_deposit_forReal(self):
        z = Zenodo(api_key)
        result = z.create_new_deposition(return_response=True)
        r = result.json()

        # save the id from newly created deposition, to check it out and remove it
        id = r["id"]
        result = z.get_deposition(
            id=id, return_response=True)  # should be found
        json = result.json()

        # title should be empty
        self.assertNotEqual(result.json(), [])  # should not be an empty
        self.assertEqual(json["title"], "", msg=f"{result.content}")

        # remove it
        result = z.remove_deposition(id=id, return_response=True)

        self.assertEqual(result.status_code, 204)  # if success, 204 returned
        # an error in api doc (https://developers.zenodo.org/#http-status-codes)

        result = Zenodo.get_deposition(api_key, id=id, return_response=True)
        # should say, its gone
        self.assertEqual(result.status_code, 410, msg=f"{result.content}")
        # should be an empty value
        self.assertEqual(
            result.json()["message"], "PID has been deleted.", msg=f"{result.content}")

    @unittest.skipIf(api_key is None, "no api key were given")
    def test_create_new_filled_deposit(self):
        """
        Create a new deposition, uploads file to it, sets some metadata and remove it.
        """

        import time

        z = Zenodo(api_key)

        expected_title = "Python Uploader to Zenodo"
        metadata = {
            'title': expected_title,
            'upload_type': 'poster',
            'description': 'This is a library for python to enable your app publishising files on zenodo.',
            'creators': [{'name': 'Heiss, Peter',
                          'affiliation': 'Sciebo RDS'}],
        }

        result = z.create_new_deposition(
            metadata=metadata, return_response=True
        )

        status = result.status_code

        # because, we give a metadata, we will get the response from change_metadata
        self.assertEqual(status, 200, msg=f"{result.content}")

        # title should be taken from metadata
        json = result.json()
        title = json["title"]
        self.assertEqual(title, expected_title, msg=f"{result.content}")

        # save the id from newly created deposition, to check it out and remove it
        id = json["id"]
        result = z.get_deposition(
            id=id, return_response=True)  # should be found
        json = result.json()

        self.assertNotEqual(result.json(), [])  # should not be an empty
        self.assertEqual(json["title"], expected_title,
                         msg=f"{result.content}")

        # add a file to deposition
        filepath = "src/lib/upload_zenodo.py"
        result = z.upload_new_file_to_deposition(
            deposition_id=id, path_to_file=filepath, return_response=True)

        # file was uploaded
        self.assertEqual(result.status_code, 201, msg=f"{result.content}")

        json = result.json()
        from hashlib import md5
        import os
        # equal file on zenodo
        file = open(os.path.expanduser(filepath), 'rb').read()
        hash = md5(file).hexdigest()
        self.assertEqual(json["checksum"], hash)

        # remove it
        result = z.remove_deposition(id=id, return_response=True)

        self.assertEqual(result.status_code, 204)  # if success, 204 returned
        # an error in api doc (https://developers.zenodo.org/#http-status-codes)

        result = z.get_deposition(id=id, return_response=True)
        # should say, its gone
        self.assertEqual(result.status_code, 410, msg=f"{result.content}")
        # should be an empty value
        self.assertEqual(
            result.json()["message"], "PID has been deleted.", msg=f"{result.content}")

    @unittest.skip
    def test_create_new_empty_deposit_bytes(self):
        pass
        # test the bytes input


if __name__ == '__main__':
    unittest.main()
