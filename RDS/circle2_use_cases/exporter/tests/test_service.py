import unittest
from lib.Service import Service
from pactman import Consumer, Provider
import json

pact = Consumer('ServiceExporter').has_pact_with(Provider('Zenodo'), port=3000)
testingaddress = "http://localhost:3000"


class Test_Service(unittest.TestCase):
    @staticmethod
    def requestStorageFolderGET(pact, folderpath: str, userId: str, files: list):
        pact.given(
            f'user {userId} has {len(files)} files in folderpath {folderpath}'
        ).upon_receiving(
            'the filepaths for files in folder with folderpath'
        ).with_request(
            'GET', f'/storage/folder'
        ) .will_respond_with(200, body={"files": files})

    @staticmethod
    def requestStorageFileGET(pact, filepath: str, userId: str, fileContent: str, code=200):
        pact.given(
            f'user {userId} has a file in filepath {filepath}'
        ).upon_receiving(
            'the filecontent of the given filepath'
        ).with_request(
            'GET', f'/storage/file'
        ) .will_respond_with(code, body=fileContent)

    @staticmethod
    def requestMetadataFilePOST(pact, userId: str, projectId: int, files: list):
        pact.given(
            f'projectId {projectId} exists in metadata'
        ).upon_receiving(
            'a file was added'
        ).with_request(
            'POST', f'/metadata/project/{projectId}/files'
        ) .will_respond_with(200, body=files)

    @staticmethod
    def requestMetadataFileDELETE(pact, userId: str, projectId: int, fileId: int = None):
        if fileId is None:
            pact.given(
                f'projectId {projectId} exists in metadata'
            ).upon_receiving(
                'all files were deleted'
            ).with_request(
                'DELETE', f'/metadata/project/{projectId}/files'
            ) .will_respond_with(200, body=[])

        else:
            pact.given(
                f'projectId {projectId} exists in metadata'
            ).upon_receiving(
                'a file was deleted'
            ).with_request(
                'DELETE', f'/metadata/project/{projectId}/files/{fileId}'
            ) .will_respond_with(200, body=[])

    @staticmethod
    def requestStorageFileDELETE(pact, userId, file):
        pact.given(
            f'user {userId} has file {file} in storage'
        ).upon_receiving(
            'a file was deleted'
        ).with_request(
            'DELETE', f'/storage/file'
        ) .will_respond_with(200, body=[])

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

        self.requestStorageFolderGET(
            pact, "/test folder", "admin", expected["files"])

        with pact:
            s = Service(expected["servicename"], "admin", 1, fileStorage=True,
                        customProperties=self.getOwncloudPort(1)[0]["properties"][0]["value"], testing=testingaddress)
        self.assertEqual(s.getDict(), expected)
        self.assertEqual(s.getJSON(), json.dumps(expected))

        expected = {
            "servicename": "Owncloud",
            "files": ["/test folder/testfile.txt"]
        }

        self.requestStorageFolderGET(
            pact, "/test folder", "admin", expected["files"])

        with pact:
            s = Service(expected["servicename"], "admin", 1, fileStorage=True,
                        customProperties=self.getOwncloudPort(1)[0]["properties"][0]["value"], testing=testingaddress)

        self.assertEqual(s.getDict(), expected)
        self.assertEqual(s.getJSON(), json.dumps(expected))

    def test_getFilesContent(self):
        expected_content = ("/test folder/testfile.txt",
                            "Lorem ipsum")
        expected = {
            "servicename": "Owncloud",
            "files": [expected_content[0]]
        }
        expected_content = [(expected_content[0],
                             f'"{expected_content[1]}"'.encode("utf-8"))]

        self.requestStorageFolderGET(
            pact, "/test folder", "admin", expected["files"])

        self.requestStorageFileGET(
            pact, expected["files"][0], "admin", "Lorem ipsum")

        with pact:
            s = Service(expected["servicename"], "admin", 1, fileStorage=True,
                        customProperties=self.getOwncloudPort(1)[0]["properties"][0]["value"], testing=testingaddress)
            files = [(x, y.getvalue())
                     for x, y in s.getFiles(getContent=True)]
        self.assertEqual(files, expected_content)

    @unittest.skip("needs to be fixed, because delete is not currently tested")
    def test_removeFile(self):
        expected = {
            "servicename": "Owncloud",
            "files": ["/test folder/testfile.txt"]
        }

        self.requestStorageFolderGET(
            pact, "/test folder", "admin", expected["files"])

        with pact:
            s = Service(expected["servicename"], "admin", 1, fileStorage=True,
                        customProperties=self.getOwncloudPort(1)[0]["properties"][0]["value"], testing=testingaddress)

        #TODO: self.assertEqual(s.getDict()["files"], expected["files"])

        del expected["files"][0]
        self.requestStorageFileDELETE(pact, "admin", "/testfile.txt")
        self.requestStorageFileGET(
            pact, "/testfile.txt", "admin", "", code=404)

        self.requestMetadataFileDELETE(pact, "admin", self.getOwncloudPort(1)[
                                       0]["properties"][0]["value"][0]["value"])

        with pact:
            self.assertTrue(s.removeAllFiles())

        self.assertEqual(s.getDict()["files"], expected["files"])

    @unittest.skip("Unhandled body content type with post files")
    def test_addFile(self):
        userId = "admin"
        expected = {
            "servicename": "Owncloud",
            "folder": "/test folder/",
            "files": []
        }

        self.requestStorageFolderGET(pact, "/", userId,
                                     [])
        with pact:
            s = Service(expected["servicename"], userId, 1, metadata=True,
                        customProperties=self.getZenodoPort(1)[0]["properties"][0]["value"], testing=testingaddress)

        f = "/test folder/testFile.txt"
        fcontent = "Lorem Ipsum"

        expected["files"].append(f)
        self.requestMetadataFilePOST(pact, "admin", 5, expected["files"])

        with pact:
            s.addFile(f, fcontent)

        self.assertEqual(s.getDict(), expected)
        self.assertEqual(s.getJSON(), json.dumps(expected))
