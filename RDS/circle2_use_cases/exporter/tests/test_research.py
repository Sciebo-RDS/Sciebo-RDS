import unittest
import json
from lib.Research import Research
from lib.Service import Service
from pactman import Consumer, Provider
from .test_service import Test_Service

pact = Consumer('ServiceExporter').has_pact_with(Provider('Zenodo'), port=3000)
testingaddress = "http://localhost:3000"


class Test_Research(unittest.TestCase):
    @staticmethod
    def requestImportsGET(pact, userid, researchIndex, imports):
        pact.given(
            f'user {userid} has research {researchIndex}'
        ).upon_receiving(
            'returns imports'
        ).with_request(
            'GET', f'/research/user/{userid}/research/{researchIndex}/imports'
        ).will_respond_with(200, body=imports)

    @staticmethod
    def requestExportsGET(pact, userid, researchIndex, exports):
        pact.given(
            f'user {userid} has research {researchIndex}'
        ).upon_receiving(
            'returns exports'
        ).with_request(
            'GET', f'/research/user/{userid}/research/{researchIndex}/exports'
        ).will_respond_with(200, body=exports)

    @staticmethod
    def requestResearchGET(pact, userId, researchIndex, research):
        pact.given(
            f'user {userId} has research {researchIndex}'
        ).upon_receiving(
            'returns everything'
        ).with_request(
            'GET', f'/research/user/{userId}/research/{researchIndex}'
        ).will_respond_with(200, body=research)

    @staticmethod
    def getZenodoPort(id):
        return Test_Service.getZenodoPort(id)

    @staticmethod
    def getOwncloudPort(id):
        return Test_Service.getOwncloudPort(id)

    def test_init(self):
        userId = "admin"
        researchIndex = 1
        files = ["/test folder"]
        filesContent = ["Lorem ipsum"]
        research = {
            "userId": userId,
            "researchIndex": researchIndex,
            "researchId": researchIndex,
            "status": 0,
            "portIn": Test_Service.getOwncloudPort(0),
            "portOut": Test_Service.getZenodoPort(0)
        }

        self.requestResearchGET(pact, userId, researchIndex, research)
        Test_Service.requestStorageFolderGET(
            pact, "/", userId, files)

        with pact:
            Research(userId=userId, researchIndex=researchIndex,
                     testing=testingaddress)

    def test_getFiles(self):
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

        self.requestResearchGET(pact, userId, researchIndex, research)
        Test_Service.requestStorageFolderGET(
            pact, "/", userId, expected_files)

        with pact:
            files = Research(userId=userId, researchIndex=researchIndex,
                             testing=testingaddress).getFiles()

        self.assertEqual(files, expected_files)

    @unittest.skip("cannot currently be tested, because pactman does not support multipart/form-data requests")
    def test_synchronization(self):
        # FIXME: cannot currently be tested, because pactman does not support multipart/form-data requests
        pass
