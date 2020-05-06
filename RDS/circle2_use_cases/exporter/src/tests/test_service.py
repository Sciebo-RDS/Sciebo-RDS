import unittest
from lib.Service import Service
from pactman import Consumer, Provider
import json

pact = Consumer('PortZenodo').has_pact_with(Provider('Zenodo'), port=3000)
testingaddress = "http://localhost:3000"


class Test_Service(unittest.TestCase):
    @staticmethod
    def requestFolderGET(pact, folderpath: str, userId: str, files: list):
        pact.given(
            f'user {userId} has {len(files)} files in folderpath {folderpath}'
        ).upon_receiving(
            'the filepaths for files in folder with folderpath'
        ).with_request(
            'GET', f'/storage/folder'
        ) .will_respond_with(200, body=files)

    @staticmethod
    def requestFileGET(pact, filepath: str, userId: str, fileContent: bytes):
        pact.given(
            f'user {userId} has a file in filepath {filepath}'
        ).upon_receiving(
            'the filecontent of the given filepath'
        ).with_request(
            'GET', f'/storage/file'
        ) .will_respond_with(200, body=fileContent)

    @staticmethod
    def requestFilePOST(pact, userId: str, projectId: int, files: list):
        pact.given(
            f'projectId {projectId} exists in metadata'
        ).upon_receiving(
            'a file was added'
        ).with_request(
            'POST', f'/metadata/project/{projectId}/files'
        ) .will_respond_with(200, body=files)

    @staticmethod
    def getOwncloudPort(id):
        return [{
            "id": id,
            "port": "port-owncloud",
            "properties": [
                {
                    "portType": "customProperties",
                    "value": [{
                        "key": "filepath",
                        "value": "/test folder"
                    }]
                },
                {
                    "portType": "fileStorage",
                    "value": True
                }
            ],
        }]

    @staticmethod
    def getZenodoPort(id):
        return [{
            "id": id,
            "port": "port-zenodo",
            "properties": [
                {
                    "portType": "customProperties",
                    "value": [{
                        "key": "projectId",
                        "value": 123
                    }]
                },
                {
                    "portType": "metadata",
                    "value": True
                }
            ],
        }]

    def test_init(self):
        expected = {
            "servicename": "Owncloud",
            "files": []
        }

        self.requestFileGET(pact, "/test folder", "admin", "Lorem ipsum")
        with pact:
            s = Service(expected["servicename"], "admin", 1, metadata=True,
                        customProperties=self.getZenodoPort(1)[0]["properties"][0]["value"], testing=testingaddress)
        self.assertEqual(s.getDict(), expected)
        self.assertEqual(s.getJSON(), json.dumps(expected))

    @unittest.skip("Unhandled body content type with post files")
    def test_addFile(self):
        userId = "admin"
        expected = {
            "servicename": "Owncloud",
            "folder": "/test folder/",
            "files": []
        }

        self.requestFolderGET(pact, "/", userId,
                              [])
        with pact:
            s = Service(expected["servicename"], userId, 1, metadata=True,
                        customProperties=self.getZenodoPort(1)[0]["properties"][0]["value"], testing=testingaddress)

        f = "/test folder/testFile.txt"
        fcontent = "Lorem Ipsum"

        expected["files"].append(f)
        self.requestFilePOST(pact, "admin", 5, expected["files"])

        with pact:
            s.addFile(f, fcontent)

        self.assertEqual(s.getDict(), expected)
        self.assertEqual(s.getJSON(), json.dumps(expected))
