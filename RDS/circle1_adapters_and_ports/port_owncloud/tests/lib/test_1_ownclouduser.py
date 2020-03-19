import unittest
from lib.ownCloudUser import OwncloudUser
from pactman import Consumer, Provider
from urllib.parse import quote
import atexit

pact_host_port = 3000
pact_host_fqdn = f"http://localhost:{pact_host_port}"
pact = Consumer('PortOwncloud').has_pact_with(
    Provider('CentralTokenStorage'), port=pact_host_port)

def create_app():
    from src import bootstrap
    # creates a test client
    app = bootstrap(use_default_error=True).app
    # propagate the exceptions to the test client
    app.config.update({"TESTING": True})

    return app


class Test_OwncloudUser(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_getSimpleFile(self):
        expected_user = "testuser"
        expected_file = "Lorem Ipsum"
        expected_filename = "testdatei.txt"

        expected_token = "ASDGANZSICHERTOKEN"
        expected_token_dict = {
            "length": 1,
            "list": [
                {
                    "type": "Token",
                    "data": {
                        "service": {
                            "type": "Service",
                            "data": {
                                "servicename": "Owncloud"
                            }
                        },
                        "access_token": expected_token
                    }
                }
            ]
        }

        pact.given(
            "Get access token"
        ).upon_receiving(
            "send access token."
        ).with_request(
            "GET", f"/user/{expected_user}/service/Owncloud"
        ).will_respond_with(200, body=expected_token_dict)

        pact.given(
            "Get simple testfile"
        ).upon_receiving(
            "A found and valid plaintext."
        ).with_request(
            "GET", f"/remote.php/webdav/{expected_filename}"
        ).will_respond_with(200, body=expected_file)

        with pact:
            user = OwncloudUser(expected_user)
            file = user.getFile(expected_filename).read()

        import json
        self.assertEqual(json.dumps(expected_file).encode("utf-8"), file, msg=file)

        expected_filename = "test%20datei.txt"

        pact.given(
            "Get simple testfile with spaces"
        ).upon_receiving(
            "A found and valid plaintext."
        ).with_request(
            "GET", f"/remote.php/webdav/{expected_filename}"
        ).will_respond_with(200, body=expected_file)

        with pact:
            file = user.getFile(expected_filename).read()

        import json
        self.assertEqual(json.dumps(expected_file).encode("utf-8"), file, msg=file)

    def test_serverGetFileWithoutSpace(self):
        expected_user = "testuser"
        expected_file = "Lorem Ipsum"
        expected_filename = "testdatei.txt"

        expected_token = "ASDGANZSICHERTOKEN"
        expected_token_dict = {
            "length": 1,
            "list": [
                {
                    "type": "Token",
                    "data": {
                        "service": {
                            "type": "Service",
                            "data": {
                                "servicename": "Owncloud"
                            }
                        },
                        "access_token": expected_token
                    }
                }
            ]
        }

        pact.given(
            "Get access token"
        ).upon_receiving(
            "send access token."
        ).with_request(
            "GET", f"/user/{expected_user}/service/Owncloud"
        ).will_respond_with(200, body=expected_token_dict)

        pact.given(
            "Get simple testfile"
        ).upon_receiving(
            "A found and valid plaintext."
        ).with_request(
            "GET", f"/remote.php/webdav/{expected_filename}"
        ).will_respond_with(200, body=expected_file)

        with pact:
            data = {
                "userId" : expected_user
            }

            file = self.client.get(f"/file/{expected_filename}", query_string=data).get_data()

        import json
        self.assertEqual(json.dumps(expected_file).encode("utf-8"), file, msg=file)

    def test_serverGetFileWithSpaces(self):
        expected_user = "testuser"
        expected_file = "Lorem Ipsum"
        expected_filename = "test%20datei.txt"

        expected_token = "ASDGANZSICHERTOKEN"
        expected_token_dict = {
            "length": 1,
            "list": [
                {
                    "type": "Token",
                    "data": {
                        "service": {
                            "type": "Service",
                            "data": {
                                "servicename": "Owncloud"
                            }
                        },
                        "access_token": expected_token
                    }
                }
            ]
        }

        pact.given(
            "Get access token"
        ).upon_receiving(
            "send access token."
        ).with_request(
            "GET", f"/user/{expected_user}/service/Owncloud"
        ).will_respond_with(200, body=expected_token_dict)

        pact.given(
            "Get simple testfile with spaces"
        ).upon_receiving(
            "A found and valid plaintext."
        ).with_request(
            "GET", f"/remote.php/webdav/{expected_filename}"
        ).will_respond_with(200, body=expected_file)

        with pact:
            data = {
                "userId" : expected_user
            }

            file = self.client.get(f"/file/{expected_filename}", query_string=data).get_data()

        import json
        self.assertEqual(json.dumps(expected_file).encode("utf-8"), file, msg=file)
