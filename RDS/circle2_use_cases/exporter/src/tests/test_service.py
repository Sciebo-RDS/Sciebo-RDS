import unittest
from lib.Service import Service
from lib.File import File
from pactman import Consumer, Provider
import json

pact = Consumer('PortZenodo').has_pact_with(Provider('Zenodo'), port=3000)


class Test_Service(unittest.TestCase):

    def test_init(self):
        expected = {
            "servicename": "Owncloud",
            "files": []
        }

        s = Service(expected["servicename"])
        self.assertEqual(s.to_dict(), expected)
        self.assertEqual(s.to_json(), json.dumps(expected))

    def test_addFile(self):
        expected = {
            "servicename": "Owncloud",
            "folder": "/test folder/",
            "files": []
        }

        s = Service(expected["servicename"])

        f = File(1, "/test folder/testFile.txt")
        s.addFile(f)
        expected["files"].append(f.to_dict())
        self.assertEqual(s.to_dict(), expected)
        self.assertEqual(s.to_json(), json.dumps(expected))

    def test_getPortName(self):
        servicename = "Owncloud"
        expected = "circle1-port-owncloud"
        s = Service(servicename)
        self.assertEqual(s.getPortName(), expected)

    def test_loadFileFromService(self):
        userId = "admin"
        files = []
        servicename = "Owncloud"
        filepath = "test folder"

        pact.given(
            'no files in service'
        ).upon_receiving(
            'the files in service'
        ).with_request(
            'GET', f'/storage/file/{filepath}?userId={userId}'
        ) .will_respond_with(200, body=files)

        s = Service(servicename)
        s.addFolder(filepath)
        with pact:
            s.loadFiles()
        self.assertEqual(s.getFiles(), files)

        files.append(f"{filepath}testfile.txt")

        pact.given(
            'one file in service'
        ).upon_receiving(
            'the files in service'
        ).with_request(
            'GET', f'/storage/file/{filepath}?userId={userId}'
        ) .will_respond_with(200, body=files)

        s = Service(servicename)
        s.addFolder(filepath)
        with pact:
            s.loadFiles()
        self.assertEqual(s.getFiles(), files)

        files.append(f"{filepath}/test file.txt")

        pact.given(
            'two files in service'
        ).upon_receiving(
            'the files in service'
        ).with_request(
            'GET', f'/storage/file/{filepath}?userId={userId}'
        ) .will_respond_with(200, body=files)

        s = Service(servicename)
        s.addFolder(filepath)
        with pact:
            s.loadFiles()
        self.assertEqual(s.getFiles(), files)

    def test_triggerUpload(self):
        servicename = "Owncloud"
        s = Service(servicename)

    def test_addFolder(self):
        servicename = "Owncloud"
        expected_folders = []
        folders = []

        s = Service(servicename)
        self.assertEqual(s.getFolders(), folders)

        folders.append("test folder")
        expected_folders.append("/test folder")

        s.addFolder(folders[-1])
        self.assertEqual(s.getFolders(), expected_folders)

        folders.append("/test folder123")
        expected_folders.append("/test folder123")

        s.addFolder(folders[-1])
        self.assertEqual(s.getFolders(), expected_folders)

        folders.append("/test 123 folder/")
        expected_folders.append("/test 123 folder")

        s.addFolder(folders[-1])
        self.assertEqual(s.getFolders(), expected_folders)

        folders.append("testfolder")
        expected_folders.append("/testfolder")

        s.addFolder(folders[-1])
        self.assertEqual(s.getFolders(), expected_folders)
