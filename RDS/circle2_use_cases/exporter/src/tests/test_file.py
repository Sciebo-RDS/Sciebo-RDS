import unittest
from lib.File import File
from pactman import Consumer, Provider
import json


pact = Consumer('PortZenodo').has_pact_with(Provider('Zenodo'), port=3000)


class Test_File(unittest.TestCase):

    def test_init(self):
        expected = {
            "id": 1,
            "path": "/test folder/testdatei.txt"
        }

        f = File(expected["id"], expected["path"])
        self.assertEqual(f.to_dict(), expected)
        self.assertEqual(f.to_json(), json.dumps(expected))

    def test_isFolderOrFile(self):
        f = File(1, "/test folder/testdatei.txt")
        self.assertTrue(f.isFile())
        self.assertFalse(f.isFolder())

        f = File(1, "/test folder/")
        self.assertFalse(f.isFile())
        self.assertTrue(f.isFolder())
