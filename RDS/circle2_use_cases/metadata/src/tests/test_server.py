import unittest
from pactman import Consumer, Provider


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
        global pact
        pact = Consumer('UseCaseMetadataProject').has_pact_with(
            Provider('PortMetadata'), port=3000)

        self.app = create_app()
        self.client = self.app.test_client()

    def test_userProject(self):
        """
        In this unit, we test the endpoint to get the corresponding researchId
        """

        userId = 0
        researchIndex = 0
        researchId = 1
        projectId = 22

        research = {
            "userId": userId,
            "status": 1,
            "portIn": [],
            "portOut": [],
            "researchId": researchId,
            "researchIndex": researchIndex
        }

        pact.given(
            'A research manager.'
        ).upon_receiving(
            'A call to get the research with researchId.'
        ).with_request(
            'GET', f"/research/user/{userId}/research/{researchIndex}"
        ).will_respond_with(200, body=research)

        research = {
            "userId": userId,
            "status": 1,
            "portIn": [],
            "portOut": [],
            "researchId": researchId,
            "researchIndex": researchIndex
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
            'A research manager.'
        ).upon_receiving(
            'A call to get the research with researchId with empty ports.'
        ).with_request(
            'GET', f"/research/id/{researchId}"
        ).will_respond_with(200, body=research)

        expectedListMetadata = {
            "researchId": researchId, "length": 0, "list": []}

        with pact:
            result = self.client.get(
                f"/metadata/user/{userId}/research/{researchIndex}").json

        self.assertEqual(result, expectedListMetadata)

    def test_research_get(self):
        """
        In this unit, we test the endpoint for creators to get and update entries.
        """

        userId = 0
        researchIndex = 0
        researchId = 1
        projectId = 5

        research = {
            "userId": userId,
            "status": 1,
            "portIn": [],
            "portOut": [],
            "researchId": researchId,
            "researchIndex": researchIndex
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
            'A research manager.'
        ).upon_receiving(
            'A call to get the research with researchId with empty ports.'
        ).with_request(
            'GET', f"/research/id/{researchId}"
        ).will_respond_with(200, body=research)

        with pact:
            result = self.client.get(
                f"/metadata/research/{researchId}").json

        expectedListMetadata = {"list": [], "length": 0}
        self.assertEqual(result, expectedListMetadata)

        ####
        # try to get metadata, if one port with projectId is there
        research["portIn"] = [{
            "port": "port-zenodo",
            "properties": [{
                    "portType": "metadata", "value": True
            }, {
                "portType": "customProperties", "value": [{
                    "key": "projectId",
                    "value": str(projectId)
                }]
            }]
        }]

        pact.given(
            'A research manager.'
        ).upon_receiving(
            'A call to get the research with port {}.'.format(
                research["portIn"] + research["portOut"])
        ).with_request(
            'GET', f"/research/id/{researchId}"
        ).will_respond_with(200, body=research)

        pact.given(
            'A port with metadata informations.'
        ).upon_receiving(
            f'A call to get the empty metadata from specific projectId {projectId}.'
        ).with_request(
            'GET', f"/metadata/project/{projectId}"
        ).will_respond_with(200, body=metadata)

        with pact:
            result = self.client.get(
                f"/metadata/research/{researchId}").json

        expectedListMetadata["list"].append({
            "port": research["portIn"][0]["port"],
            "metadata": metadata
        })
        expectedListMetadata["length"] = 1
        self.assertEqual(result, expectedListMetadata)

        ####
        # try to get metadata, if there is a port, which is used as in- and output

        research["portOut"] = [{
            "port": "port-zenodo",
            "properties": [{
                    "portType": "metadata", "value": True
            }]
        }]

        pact.given(
            'A research manager.'
        ).upon_receiving(
            'A call to get the research with port {}.'.format(
                research["portIn"] + research["portOut"])
        ).with_request(
            'GET', f"/research/id/{researchId}"
        ).will_respond_with(200, body=research)

        pact.given(
            'A port with metadata informations.'
        ).upon_receiving(
            f'A call to get the metadata from specific projectId {projectId}.'
        ).with_request(
            'GET', f"/metadata/project/{projectId}"
        ).will_respond_with(200, body=metadata)

        with pact:
            result = self.client.get(
                f"/metadata/research/{researchId}").json

        self.assertEqual(result, expectedListMetadata)

    def test_research_update_metadata(self):
        userId = 0
        researchIndex = 0
        researchId = 1
        projectId = 5

        research = {
            "userId": userId,
            "status": 1,
            "portIn": [],
            "portOut": [{
                "port": "port-zenodo",
                "properties": [
                    {
                        "portType": "metadata", "value": True
                    }, {
                        "portType": "customProperties", "value": [{
                            "key": "projectId",
                            "value": str(projectId)
                        }]
                    }
                ]
            }],
            "researchId": researchId,
            "researchIndex": researchIndex
        }

        pact.given(
            'A research manager.'
        ).upon_receiving(
            'A call to get the research with port {} to update creators.'.format(
                research["portIn"] + research["portOut"])
        ).with_request(
            'GET', f"/research/id/{researchId}"
        ).will_respond_with(200, body=research)

        metadataFull = {
            "Creators": [{
                "name":  "Mustermann, Max",
                "nameType": "Personal",
                "familyName": "Mustermann",
                "givenName": "Max",
            }],
            "Identifiers": [{"identifierType": "DOI",
                             "identifier": "10.5072/example"}],
            "PublicationYear": "2020",
            "Publisher": "University of Münster",
            "ResourceType": "Poster",
            "SchemaVersion": "http://datacite.org/schema/kernel-4",
            "Titles": [{"title": "This is a test title", "lang": "de"}]
        }

        metadata = {
            "Creators": metadataFull["Creators"]
        }

        pact.given(
            'A port with metadata informations.'
        ).upon_receiving(
            f'A call to update the metadata for from specific projectId {projectId}.'
        ).with_request(
            'PATCH', f"/metadata/project/{projectId}"
        ).will_respond_with(200, body=metadata)

        with pact:
            result = self.client.patch(
                f"/metadata/research/{researchId}", json=metadata).json

        expectedListMetadata = {}
        expectedListMetadata["list"] = [{
            "port": research["portOut"][0]["port"],
            "metadata": metadata
        }]
        expectedListMetadata["length"] = 1

        self.assertEqual(result, expectedListMetadata)

        metadata = {
            "Creators": metadataFull["Creators"],
            "Titles": metadataFull["Titles"],
            "Publisher": metadataFull["Publisher"]
        }

        pact.given(
            'A research manager.'
        ).upon_receiving(
            'A call to get the research with port {} to update creators.'.format(
                research["portIn"] + research["portOut"])
        ).with_request(
            'GET', f"/research/id/{researchId}"
        ).will_respond_with(200, body=research)

        pact.given(
            'A port with metadata informations.'
        ).upon_receiving(
            f'A call to update the metadata again from specific projectId {projectId}.'
        ).with_request(
            'PATCH', f"/metadata/project/{projectId}"
        ).will_respond_with(200, body=metadata)

        with pact:
            result = self.client.patch(
                f"/metadata/research/{researchId}", json=metadata).json

        expectedListMetadata = {}
        expectedListMetadata["list"] = [{
            "port": research["portOut"][0]["port"],
            "metadata": metadata
        }]
        expectedListMetadata["length"] = 1

        self.assertEqual(result, expectedListMetadata)

        # TODO: add more tests for the following cases
        # - the port responds with a status_code >= 300, this could be follow, when
        #   - the port does not support an optional metadata property
        #   - the port does not support a required property
        #   - the port has a bad implementation (bad request etc.)

    def test_creators_id(self):
        """
        In this unit, we test the endpoint for given creators to get and update a specific entry.
        """
        userId = 0
        researchIndex = 0
        researchId = 1
        projectId = 5

        research = {
            "userId": userId,
            "status": 1,
            "portIn": [],
            "portOut": [],
            "researchId": researchId,
            "researchIndex": researchIndex
        }

        research["portIn"] = [{
            "port": "port-zenodo",
            "properties": [{
                    "portType": "metadata", "value": True
            }, {
                "portType": "customProperties", "value": [{
                            "key": "projectId",
                            "value": str(projectId)
                }]
            }]
        }]

        metadata = {
            "Creators": [{
                "name":  "Mustermann, Max",
                "nameType": "Personal",
                "familyName": "Mustermann",
                "givenName": "Max",
            }],
            "Identifiers": [{"identifierType": "DOI",
                             "identifier": "10.5072/example"}],
            "PublicationYear": "2020",
            "Publisher": "University of Münster",
            "ResourceType": "Poster",
            "SchemaVersion": "http://datacite.org/schema/kernel-4",
            "Titles": [{"title": "This is a test title", "lang": "de"}]
        }

        # check, if there are creators
        pact.given(
            'A research manager.'
        ).upon_receiving(
            'A call to get the research with port {} for creators.'.format(
                research["portIn"] + research["portOut"])
        ).with_request(
            'GET', f"/research/id/{researchId}"
        ).will_respond_with(200, body=research)

        pact.given(
            'A port with metadata informations.'
        ).upon_receiving(
            f'A call to get the metadata for creator from specific projectId {projectId}.'
        ).with_request(
            'GET', f"/metadata/project/{projectId}"
        ).will_respond_with(200, body={"Creators": metadata["Creators"]})

        expectedMetadata = []
        for port in research["portIn"]:
            expectedMetadata.append({
                "port": port["port"],
                "metadata": {"Creators": metadata["Creators"]}
            })

        expectedMetadata = {
            "length": len(expectedMetadata),
            "list": expectedMetadata
        }

        with pact:
            result = self.client.get(
                f"/metadata/research/{researchId}", json={"Creators": ""}).json

        self.assertEqual(result, expectedMetadata)

        # update the creator
        metadata["Creators"] = [{
            "name":  "Mimimi, Maxim",
            "nameType": "Personal",
            "familyName": "Mimimi",
            "givenName": "Maxim",
        }]

        pact.given(
            'A research manager.'
        ).upon_receiving(
            'A call to get the research with port {} for creators to update.'.format(
                research["portIn"] + research["portOut"])
        ).with_request(
            'GET', f"/research/id/{researchId}"
        ).will_respond_with(200, body=research)

        pact.given(
            'A port with metadata informations.'
        ).upon_receiving(
            f'A call to update the metadata for creator from specific projectId {projectId}.'
        ).with_request(
            'PATCH', f"/metadata/project/{projectId}"
        ).will_respond_with(200, body=metadata)

        with pact:
            result = self.client.patch(
                f"/metadata/research/{researchId}", json=metadata).json

        expectedMetadata = []
        for port in research["portIn"]:
            expectedMetadata.append({
                "port": port["port"],
                "metadata": metadata
            })

        expectedMetadata = {
            "length": len(expectedMetadata),
            "list": expectedMetadata
        }

        self.assertEqual(result, expectedMetadata)

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

    def test_jsonschema(self):
        result = self.client.get("/metadata/jsonschema").json

        with open("datacite_4.3_schema.json", "r") as file:
            import json
            d = json.load(file)

            # schema in result should be string
            expected = {
                "kernelversion": "4.3", "schema": json.dumps(d)
            }
            self.assertEqual(result, expected)

            # schema in result should be not a dict
            expected = {
                "kernelversion": "4.3", "schema": d
            }
            self.assertNotEqual(result, expected)

            # schema in result should be not a bytestring
            expected = {
                "kernelversion": "4.3", "schema": str(json.dumps(d)).encode("utf-8")
            }
            self.assertNotEqual(result, expected)
