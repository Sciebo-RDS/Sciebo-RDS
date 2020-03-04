import unittest
from pactman import Consumer, Provider


pact = Consumer('UseCaseMetadataProject').has_pact_with(
    Provider('PortMetadata'), port=3000)

testing_address = "localhost:3000"


def create_app():
    from src import bootstrap
    # creates a test client
    app = bootstrap(use_default_error=True).app
    # propagate the exceptions to the test client
    app.config.update({"TESTING": testing_address})

    return app


class TestMetadata(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_userProject(self):
        """
        In this unit, we test the endpoint to get the corresponding projectId
        """

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
            result = self.client.get(
                f"/service/user/{userId}/project/{projectIndex}").json

        expected = {"projectId": projectId}

        self.assertEqual(result, expected)

    def test_creators(self):
        """
        In this unit, we test the endpoint for creators to get and add entries.
        """

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

        metadata = {
            "Creators": [],
            "Identifiers": [],
            "PublicationYear": "",
            "Publisher": "",
            "ResourceType": "",
            "SchemaVersion": "http://datacite.org/schema/kernel-4",
            "Titles": []
        }

        ####
        # at first, try to get metadata, when there are no ports

        pact.given(
            'A project manager.'
        ).upon_receiving(
            'A call to get the project with projectId with empty ports.'
        ).with_request(
            'GET', f"/projects/id/{projectId}"
        ).will_respond_with(200, body=project)

        with pact:
            result = self.client.get(
                f"/metadata/project/{projectId}/creators").json

        expectedListMetadata = {"list": [], "length": 0}
        self.assertEqual(result, expectedListMetadata)

        ####
        # try to get metadata, if one port is there
        project["portIn"] = [{
            "port": "port-zenodo",
            "properties": [{
                    "portType": "metadata", "value": True
            }]
        }]

        pact.given(
            'A project manager.'
        ).upon_receiving(
            'A call to get the project with port {}.'.format(
                project["portIn"] + project["portOut"])
        ).with_request(
            'GET', f"/projects/id/{projectId}"
        ).will_respond_with(200, body=project)

        pact.given(
            'A port with metadata informations.'
        ).upon_receiving(
            f'A call to get the empty metadata from specific projectId {projectId}.'
        ).with_request(
            'GET', f"/metadata/project/{projectId}"
        ).will_respond_with(200, body=metadata)

        with pact:
            result = self.client.get(
                f"/metadata/project/{projectId}/creators").json

        expectedListMetadata["list"].append({
            "port": project["portIn"][0]["port"],
            "metadata": metadata
        })
        expectedListMetadata["length"] = 1
        self.assertEqual(result, expectedListMetadata)

        ####
        # try to get metadata, if there is a port, which is used as in- and output

        project["portOut"] = [{
            "port": "port-zenodo",
            "properties": [{
                    "portType": "metadata", "value": True
            }]
        }]

        pact.given(
            'A project manager.'
        ).upon_receiving(
            'A call to get the project with port {}.'.format(
                project["portIn"] + project["portOut"])
        ).with_request(
            'GET', f"/projects/id/{projectId}"
        ).will_respond_with(200, body=project)

        pact.given(
            'A port with metadata informations.'
        ).upon_receiving(
            f'A call to get the metadata from specific projectId {projectId}.'
        ).with_request(
            'GET', f"/metadata/project/{projectId}"
        ).will_respond_with(200, body=metadata)

        with pact:
            result = self.client.get(
                f"/metadata/project/{projectId}/creators").json

        self.assertEqual(result, expectedListMetadata)

    @unittest.skip("Currently not implemented")
    def test_creators_id(self):
        """
        In this unit, we test the endpoint for given creators to get and update a specific entry.
        """
        pass

    @unittest.skip("Currently not implemented")
    def test_titles(self):
        """
        In this unit, we test the endpoint for creators to get and add titles.
        """
        pass

    @unittest.skip("Currently not implemented")
    def test_titles_id(self):
        """
        In this unit, we test the endpoint for given title to get and update a specific entry.
        """
        pass

    @unittest.skip("Currently not implemented")
    def test_identifiers(self):
        """
        In this unit, we test the endpoint for identifiers to get entries.
        """
        pass

    @unittest.skip("Currently not implemented")
    def test_identifiers_id(self):
        """
        In this unit, we test the endpoint for given identifier to get a specific entry.
        """
        pass

    @unittest.skip("Currently not implemented")
    def test_publisher(self):
        """
        In this unit, we test the endpoint for publisher to get and update entries.
        """
        pass

    @unittest.skip("Currently not implemented")
    def test_publicationyear(self):
        """
        In this unit, we test the publicationyear for identifiers to get and update entries.
        """
        pass

    @unittest.skip("Currently not implemented")
    def test_schemaversion(self):
        """
        In this unit, we test the endpoint for schemaversion to get entries.
        """
        pass

    @unittest.skip("Currently not implemented")
    def test_resourcetype(self):
        """
        In this unit, we test the endpoint for resourcetype to get and update entries.
        """
        pass
