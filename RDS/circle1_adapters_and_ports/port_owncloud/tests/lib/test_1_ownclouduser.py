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

# TODO: Needs tests!!!
class Test_OwncloudUser(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    @unittest.skip("This does not work currently")
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
            "Head simple testfile"
        ).upon_receiving(
            "A found and valid plaintext."
        ).with_request(
            "HEAD", f"/remote.php/webdav/{expected_filename}"
        ).will_respond_with(200, body=expected_file)

        propfind = """<?xml version="1.0"?>
<d:multistatus xmlns:d="DAV:" xmlns:s="http://sabredav.org/ns" xmlns:oc="http://owncloud.org/ns"><d:response><d:href>/owncloud/remote.php/webdav/Documents/Paris.jpg</d:href><d:propstat><d:prop><d:getlastmodified>Wed, 18 Dec 2019 13:58:32 GMT</d:getlastmodified><d:getcontentlength>228761</d:getcontentlength><d:resourcetype/><d:getetag>&quot;b16edaf4334c12e11b218b1e5979e24d&quot;</d:getetag><d:getcontenttype>image/jpeg</d:getcontenttype></d:prop><d:status>HTTP/1.1 200 OK</d:status></d:propstat></d:response></d:multistatus>"""

        pact.given(
            "Get simple testfile"
        ).upon_receiving(
            "A found and valid plaintext."
        ).with_request(
            "PROPFIND", f"/remote.php/webdav/"
        ).will_respond_with(200, body=propfind)

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
        self.assertEqual(json.dumps(expected_file).encode(
            "utf-8"), file, msg=file)

        expected_filename = "test%20datei.txt"

        pact.given(
            "head simple testfile with spaces"
        ).upon_receiving(
            "A found and valid plaintext."
        ).with_request(
            "HEAD", f"/remote.php/webdav/{expected_filename}"
        ).will_respond_with(200, body=expected_file)

        pact.given(
            "Get simple testfile with spaces"
        ).upon_receiving(
            "A found and valid plaintext."
        ).with_request(
            "PROPFIND", f"/remote.php/webdav/"
        ).will_respond_with(200, body=propfind)

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
        self.assertEqual(json.dumps(expected_file).encode(
            "utf-8"), file, msg=file)

    @unittest.skip("This does not work currently")
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
            "HEAD simple testfile"
        ).upon_receiving(
            "A found and valid plaintext."
        ).with_request(
            "HEAD", f"/remote.php/webdav/{expected_filename}"
        ).will_respond_with(200, body=expected_file)

        pact.given(
            "Get simple testfile"
        ).upon_receiving(
            "A found and valid plaintext."
        ).with_request(
            "PROPFIND", f"/remote.php/webdav/{expected_filename}"
        ).will_respond_with(200, body=expected_file)

        pact.given(
            "Get simple testfile"
        ).upon_receiving(
            "A found and valid plaintext."
        ).with_request(
            "GET", f"/remote.php/webdav/{expected_filename}"
        ).will_respond_with(200, body=expected_file)

        with pact:
            data = {
                "userId": expected_user,
                "filepath": expected_filename
            }

            file = self.client.get(
                f"/storage/file", json=data).get_data()

        import json
        self.assertEqual(json.dumps(expected_file).encode(
            "utf-8"), file, msg=file)

    @unittest.skip("This does not work currently")
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
            "HEAD simple testfile with spaces"
        ).upon_receiving(
            "A found and valid plaintext."
        ).with_request(
            "HEAD", f"/remote.php/webdav/{expected_filename}"
        ).will_respond_with(200, body=expected_file)

        pact.given(
            "Get simple testfile with spaces"
        ).upon_receiving(
            "A found and valid plaintext."
        ).with_request(
            "PROPFIND", f"/remote.php/webdav/{expected_filename}"
        ).will_respond_with(200, body=expected_file)

        pact.given(
            "Get simple testfile with spaces"
        ).upon_receiving(
            "A found and valid plaintext."
        ).with_request(
            "GET", f"/remote.php/webdav/{expected_filename}"
        ).will_respond_with(200, body=expected_file)

        with pact:
            data = {
                "userId": expected_user,
                "filepath": expected_filename
            }

            file = self.client.get(
                f"/storage/file", json=data).get_data()

        import json
        self.assertEqual(json.dumps(expected_file).encode(
            "utf-8"), file, msg=file)

    @unittest.skip("This does not work currently")
    def test_getFolders(self):
        expected_user = "testuser"
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

        expected_files = ["/owncloud/remote.php/webdav/Documents/Paris.jpg",
                          "/owncloud/remote.php/webdav/Documents/Example.odt"]
        expected_foldername = "/Documents"

        ocResponse = """<?xml version="1.0" encoding="UTF-8"?>
<d:multistatus xmlns:d="DAV:" xmlns:oc="http://owncloud.org/ns" xmlns:s="http://sabredav.org/ns">
   <d:response>
      <d:href>/owncloud/remote.php/webdav/Documents/</d:href>
      <d:propstat>
         <d:prop>
            <d:getlastmodified>Fri, 24 Apr 2020 08:30:44 GMT</d:getlastmodified>
            <d:resourcetype>
               <d:collection />
            </d:resourcetype>
            <d:quota-used-bytes>264988</d:quota-used-bytes>
            <d:quota-available-bytes>-3</d:quota-available-bytes>
            <d:getetag>"5ea2a3b47fcf9"</d:getetag>
         </d:prop>
         <d:status>HTTP/1.1 200 OK</d:status>
      </d:propstat>
   </d:response>
   <d:response>
      <d:href>/owncloud/remote.php/webdav/Documents/Example.odt</d:href>
      <d:propstat>
         <d:prop>
            <d:getlastmodified>Wed, 18 Dec 2019 13:58:32 GMT</d:getlastmodified>
            <d:getcontentlength>36227</d:getcontentlength>
            <d:resourcetype />
            <d:getetag>"53988e76978c103ef6ee1b5d13e89f82"</d:getetag>
            <d:getcontenttype>application/vnd.oasis.opendocument.text</d:getcontenttype>
         </d:prop>
         <d:status>HTTP/1.1 200 OK</d:status>
      </d:propstat>
      <d:propstat>
         <d:prop>
            <d:quota-used-bytes />
            <d:quota-available-bytes />
         </d:prop>
         <d:status>HTTP/1.1 404 Not Found</d:status>
      </d:propstat>
   </d:response>
   <d:response>
      <d:href>/owncloud/remote.php/webdav/Documents/Paris.jpg</d:href>
      <d:propstat>
         <d:prop>
            <d:getlastmodified>Wed, 18 Dec 2019 13:58:32 GMT</d:getlastmodified>
            <d:getcontentlength>228761</d:getcontentlength>
            <d:resourcetype />
            <d:getetag>"b16edaf4334c12e11b218b1e5979e24d"</d:getetag>
            <d:getcontenttype>image/jpeg</d:getcontenttype>
         </d:prop>
         <d:status>HTTP/1.1 200 OK</d:status>
      </d:propstat>
      <d:propstat>
         <d:prop>
            <d:quota-used-bytes />
            <d:quota-available-bytes />
         </d:prop>
         <d:status>HTTP/1.1 404 Not Found</d:status>
      </d:propstat>
   </d:response>
</d:multistatus>
"""

        pact.given(
            "HEAD given folder"
        ).upon_receiving(
            "A valid webdav response."
        ).with_request(
            "HEAD", f"/remote.php/webdav/Documents/"
        ).will_respond_with(200, body=ocResponse)

        pact.given(
            "Get all files within folder"
        ).upon_receiving(
            "A valid webdav response."
        ).with_request(
            "PROPFIND", f"/remote.php/webdav/Documents/"
        ).will_respond_with(200, body=ocResponse)

        with pact:
            user = OwncloudUser(expected_user)
            files = user.getFolder(expected_foldername)

        self.assertEqual(expected_files, files)
