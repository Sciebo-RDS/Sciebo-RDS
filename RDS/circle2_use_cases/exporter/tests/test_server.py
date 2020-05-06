
import unittest
import sys
import os
from pactman import Consumer, Provider
from .test_research import Test_Research
from .test_service import Test_Service


def create_app():
    testing_address = "http://localhost:3000"

    from src import bootstrap
    # creates a test client
    app = bootstrap(use_default_error=True).app
    # propagate the exceptions to the test client
    app.config.update({"TESTING": testing_address})

    return app


pact = Consumer('ServiceExporter').has_pact_with(Provider('Zenodo'), port=3000)

unittest.TestCase.maxDiff = None


class TestServiceExporter(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_files(self):
        userId = "admin"
        researchIndex = 1

        userId = "admin"
        researchIndex = 1
        expected_files = ["/test folder"]
        filesContent = ["Lorem ipsum"]
        research = {
            "userId": userId,
            "researchIndex": researchIndex,
            "researchId": researchIndex,
            "status": 0,
            "portIn": Test_Service.getOwncloudPort(0),
            "portOut": Test_Service.getZenodoPort(0)
        }

        Test_Research.requestResearchGET(pact, userId, researchIndex, research)
        Test_Service.requestStorageFolderGET(pact, "/", userId, expected_files)

        with pact:
            resp = self.client.get(
                "/exporter/user/{}/research/{}".format(userId, researchIndex)).json

        self.assertEqual(resp, expected_files)
