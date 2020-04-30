import unittest
import json
from lib.Research import Research
from lib.Service import Service
from lib.File import File
from pactman import Consumer, Provider

pact = Consumer('PortZenodo').has_pact_with(Provider('Zenodo'), port=3000)


class Test_Research(unittest.TestCase):
    def test_init(self):
        userId = "admin"
        researchIndex = 1

        expected = {
            "userId": userId,
            "researchIndex": researchIndex,
            "researchId": None
        }

        r = Research(userId, researchIndex)

        self.assertEqual(r.to_dict(), expected)
        self.assertEqual(r.to_json(), json.dumps(expected))

    def test_loadServices(self):
        userid = "admin"
        researchIndex = 1
        files = []
        servicename = "Owncloud"
        filepath = "/test folder/"
        imports = [{
            "id": 1,
            "port" "port-owncloud"
            "properties": [
                {
                    "portType": "customProperties",
                    "value": [{
                        "key": "filepath",
                        "value": filepath
                    }]
                },
                {
                    "portType": "fileStorage",
                    "value": True
                }
            ],
        }]

        pact.given(
            'no files in service'
        ).upon_receiving(
            'the files in service'
        ).with_request(
            'GET', f'/user/{userid}/research/{researchIndex}/imports'
        ) .will_respond_with(200, body=imports)


        exports = [{
            "id": 1,
            "port" "port-zenodo"
            "properties": [
                {
                    "portType": "customProperties",
                    "value": [{
                        "key": "projectId",
                        "value": 123
                    }]
                },
                {
                    "portType": "fileStorage",
                    "value": True
                }
            ],
        }]

        pact.given(
            'no files in service'
        ).upon_receiving(
            'the files in service'
        ).with_request(
            'GET', f'/user/{userid}/research/{researchIndex}/exports'
        ) .will_respond_with(200, body=exports)
