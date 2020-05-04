import unittest
from lib.File import File
from pactman import Consumer, Provider
import json


pact = Consumer('PortZenodo').has_pact_with(Provider('Zenodo'), port=3000)


class Test_File(unittest.TestCase):

    def test_init(self):
        expected = {
            "path": "/test folder/testdatei.txt"
        }

        f = File(expected["path"])
        self.assertEqual(f.to_dict(), expected)
        self.assertEqual(f.to_json(), json.dumps(expected))
