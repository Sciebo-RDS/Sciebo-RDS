from src.lib.Project import Project
from pactman import Consumer, Provider
import unittest

pact = Consumer('UseCaseMetadataProject').has_pact_with(
    Provider('PortMetadata'), port=3000)

testing_address = "localhost:3000"


class Test_Project(unittest.TestCase):
    def test_project_init_projectId(self):
        userId = 0
        projectIndex = 0
        projectId = 1

        project = {
            "userId": userId,
            "status": 1,
            "portIn": [],
            "portOut": [],
            "projectId": projectId,
            "projectIndex": projectIndex
        }

        pact.given(
            'A project manager.'
        ).upon_receiving(
            'A call to get the projectId from userId and projectIndex.'
        ).with_request(
            'GET', f"/projects/id/{projectId}"
        ).will_respond_with(200, body=project)

        with pact:
            Project(testing=testing_address, projectId=projectId)

    def test_project_init_projectIndex(self):
        userId = 0
        projectIndex = 0
        projectId = 1

        project = {
            "userId": userId,
            "status": 1,
            "portIn": [],
            "portOut": [],
            "projectId": projectId,
            "projectIndex": projectIndex
        }

        pact.given(
            'A project manager.'
        ).upon_receiving(
            'A call to get the project with projectId.'
        ).with_request(
            'GET', f"/projects/{userId}/project/{projectIndex}"
        ).will_respond_with(200, body=project)

        with pact:
            Project(testing=testing_address, userId=userId, projectIndex=projectIndex)

    def test_project_init_exceptions(self):
        userId = 0
        projectIndex = 0

        with pact:
            with self.assertRaises(ValueError):
                Project(testing=testing_address, userId=userId)

        with pact:
            with self.assertRaises(ValueError):
                Project(testing=testing_address, projectIndex=projectIndex)
