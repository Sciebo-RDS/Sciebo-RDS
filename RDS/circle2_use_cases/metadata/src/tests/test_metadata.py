from lib.Metadata import Metadata
from pactman import Consumer, Provider
import unittest
import json


pact = Consumer('UseCaseMetadata').has_pact_with(
    Provider('PortMetadata'), port=3000)

testing_address = "localhost:3000"

unittest.TestCase.maxDiff = None


class Test_Metadata(unittest.TestCase):

    def test_metadata_init(self):
        """
        This unit tests the metadata object constructor.
        """

        Metadata(testing=testing_address)

    def test_metadata_get_researchid(self):
        """
        This unit tests ability of metadata object to get the researchId for corresponding userId and research index.
        """
        md = Metadata(testing=testing_address)

        def test_researchId(userId, researchIndex, researchId):
            nonlocal md

            research = {
                "userId": userId,
                "status": 1,
                "portIn": [],
                "portOut": [],
                "researchIndex": researchIndex,
                "researchId": researchId
            }

            pact.given(
                'A research service with research.'
            ).upon_receiving(
                f'A call to get the researchId from userId {userId} and researchIndex {researchIndex}.'
            ).with_request(
                'GET', f"/research/user/{userId}/research/{researchIndex}"
            ).will_respond_with(200, body=research)

            # should be the same as researchIndex, because there are no other research
            with pact:
                result = md.getResearchId(userId, researchIndex)
            self.assertEqual(result, researchId)

        userId = "admin"
        researchIndex = 0
        researchId = 0
        test_researchId(userId, researchIndex, researchId)
        researchIndex = 1
        researchId = 4
        test_researchId(userId, researchIndex, researchId)

    @unittest.skip("This test is currently not needed, because getPort is tested in Project")
    def test_metadata_get_connector(self):
        """
        This unit tests the ability of metadata object to get connector from a researchId.
        """
        md = Metadata(testing=testing_address)

        def test_getPorts(func, userId, researchId, portIn, portOut):
            research = {
                "userId": userId,
                "status": 1,
                "portIn": portIn,
                "portOut": portOut,
                "researchId": researchIndex
            }

            pact.given(
                'A research service with research.'
            ).upon_receiving(
                'A call to get the researchId from userId and researchIndex.'
            ).with_request(
                'GET', f"/research/user/{userId}/research/{researchIndex}"
            ).will_respond_with(200, body=research)

            with pact:
                result = func(userId, researchIndex)
            return result

        userId = "admin"
        researchIndex = 0

        for portIn in [[], ["port-owncloud"], ["port-owncloud", "port-zenodo"]]:
            for portOut in [[], ["port-owncloud"], ["port-owncloud", "port-zenodo"]]:
                with self.subTest(portIn=portIn, portOut=portOut):
                    result = test_getPorts(md.getPortIn, userId,
                                           researchIndex, portIn, portOut)
                    self.assertEqual(result, portIn)

                    result = test_getPorts(md.getPortOut, userId,
                                           researchIndex, portIn, portOut)
                    self.assertEqual(result, portOut)

    def test_metadata_get_metadata_from_connector(self):
        """
        This unit tests the ability of metadata object to get metadata from a given connector.
        This is the hard way to get informations from a specific port.
        """
        md = Metadata(testing=testing_address)

        port = "localhost:3000"
        projectId = 5

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

        pact.given(
            'A port with metadata informations.'
        ).upon_receiving(
            'A call to get the metadata from specific researchId.'
        ).with_request(
            'GET', f"/metadata/project/{projectId}"
        ).will_respond_with(200, body=metadata)

        with pact:
            result = md.getMetadataForProjectFromPort(port, projectId)
        self.assertEqual(result, metadata)

    def test_metadata_get_metadata_from_researchId(self):
        """
        This unit tests the ability of metadata object to get metadata from a given researchId.
        This is the handy way with researchId.
        Notice: Should be very similar to `test_metadata_get_metadata_from_connector`
        """
        md = Metadata(testing=testing_address)

        userId = 20
        researchIndex = 21
        researchId = 22
        projectId = 5

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

        expected_research = {
            "userId": userId,
            "researchIndex": researchIndex
        }

        expected_research["researchId"] = researchId
        expected_research["portIn"] = [{
            "port": "port-zenodo",
            "properties": [{
                    "portType": "metadata", "value": True
            }, {
                "portType": "customProperties", "value": [{
                    "key": "projectId",
                    "value": str(projectId)
                }]
            }]
        },
            {
            "port": "port-owncloud",
            "properties": [{
                "portType": "fileStorage", "value": True
            }]
        }]

        expected_research["portOut"] = [{
            "port": "port-zenodo",
            "properties": [{
                    "portType": "metadata", "value": True
            }]
        }]

        pact.given(
            'The research manager.'
        ).upon_receiving(
            f'A call to get the researchIndex {researchIndex} and user {userId}.'
        ).with_request(
            'GET', f"/research/id/{researchId}"
        ).will_respond_with(200, body=expected_research)

        expected_metadata = []

        # only portOut, because it has a duplicate from portIn and portIn has port-owncloud,
        # which should be out in results, because it is not of type `metadata`.
        for ports in expected_research["portOut"]:
            skip = True

            for prop in ports["properties"]:
                if prop["portType"] == "metadata":
                    skip = False

            if skip:
                continue

            port = ports["port"]

            apiKey = "ASDB12345"

            pact.given(
                'An access token for userid.'
            ).upon_receiving(
                f'A call to get the access token for user {userId}.'
            ).with_request(
                'GET', "/user/{}/service/{}".format(
                    userId, port.replace("port-", "").lower())
            ).will_respond_with(200, body={"type": "Token", "data": {"access_token": apiKey}})

            pact.given(
                'A port with metadata informations.'
            ).upon_receiving(
                f'A call to get the metadata from specific researchId {projectId} and port {port}.'
            ).with_request(
                'GET', f"/metadata/project/{projectId}"
            ).will_respond_with(200, body=metadata)

            expected_metadata.append({
                "port": port,
                "metadata": metadata
            })

        with pact:
            result = md.getMetadataForResearch(researchId=researchId)
        self.assertEqual(result, expected_metadata)

    def test_metadata_update_metadata_from_connector(self):
        """
        This unit tests the ability of metadata object to update metadata from a given connector.
        This is the hard way.
        """
        md = Metadata(testing=testing_address)

        def test_metadata_response(updateMetadata, projectId):
            port = "localhost:3000"

            metadata = {
                "Creators": [],
                "Identifiers": [],
                "PublicationYear": "",
                "Publisher": "",
                "ResourceType": "",
                "SchemaVersion": "http://datacite.org/schema/kernel-4",
                "Titles": []
            }

            metadata = dict(list(metadata.items()) +
                            list(updateMetadata.items()))

            pact.given(
                'A port with metadata informations.'
            ).upon_receiving(
                f'A call to update the metadata from specific projectId {projectId}.'
            ).with_request(
                'PATCH', f"/metadata/project/{projectId}"
            ).will_respond_with(200, body=updateMetadata)

            with pact:
                result = md.updateMetadataForResearchFromPort(
                    port, projectId, updateMetadata)
            self.assertEqual(result, updateMetadata)

        updateMetadata = {}
        updateMetadata["Creators"] = [{
            "creatorName":  "Max Mustermann",
            "nameType": "Personal",
            "familyName": "Mustermann",
            "givenName": "Max",
        }]
        test_metadata_response(updateMetadata, 10)

        updateMetadata["PublicationYear"] = "2020"
        test_metadata_response(updateMetadata, 11)

    def test_metadata_update_metadata_from_projectId(self):
        """
        This unit tests the ability of metadata object to update metadata from a given researchId.
        This is the handy way.
        Notice: Should be very similar to `test_metadata_get_metadata_from_connector`
        """
        md = Metadata(testing=testing_address)

        def test_metadata_response(updateMetadata):
            userId = 0
            researchIndex = 0
            researchId = 2
            projectId = 5

            metadata = {
                "Creators": [],
                "Identifiers": [],
                "PublicationYear": "",
                "Publisher": "",
                "ResourceType": "",
                "SchemaVersion": "http://datacite.org/schema/kernel-4",
                "Titles": []
            }

            metadata = dict(list(metadata.items()) +
                            list(updateMetadata.items()))

            expected_pid = {
                "userId": userId,
                "researchIndex": researchIndex
            }

            expected_research = expected_pid.copy()
            expected_research["status"] = 1
            expected_research["researchId"] = researchId
            expected_research["portIn"] = [{
                "port": "port-zenodo",
                "properties": [
                    {
                        "portType": "metadata", "value": True
                    }
                ]
            }, {
                "port": "port-owncloud",
                "properties": [{
                        "portType": "fileStorage", "value": True
                }]
            }]

            expected_research["portOut"] = [{
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
                'The research manager.'
            ).upon_receiving(
                'A call to get the researchIndex and user.'
            ).with_request(
                'GET', f"/research/id/{researchId}"
            ).will_respond_with(200, body=expected_research)

            expected_metadata = []
            # add patch requests for all given example ports, which are portType `metadata`
            for port in expected_research["portOut"]:
                skip = True

                for prop in port["properties"]:
                    if prop["portType"] == "metadata":
                        skip = False

                if skip:
                    continue

                apiKey = "ASDB12345"

                pact.given(
                    'An access token for userid.'
                ).upon_receiving(
                    f'A call to get the access token for user {userId}.'
                ).with_request(
                    'GET', f"/user/{userId}/service/zenodo"
                ).will_respond_with(200, body={"type": "Token", "data": {"access_token": apiKey}})

                portname = port["port"]

                pact.given(
                    'A port with metadata informations.'
                ).upon_receiving(
                    f'A call to update the metadata from specific projectId {projectId} for port {portname} with update {updateMetadata.keys()}.'
                ).with_request(
                    'PATCH', f"/metadata/project/{projectId}"
                ).will_respond_with(200, body=updateMetadata)

                expected_metadata.append({
                    "port": portname,
                    "metadata": updateMetadata
                })

            with pact:
                result = md.updateMetadataForResearch(
                    researchId, updateMetadata)
            self.assertEqual(result, expected_metadata)

        updateMetadata = {}
        updateMetadata["Creators"] = [{
            "creatorName":  "Max Mustermann",
            "nameType": "Personal",
            "familyName": "Mustermann",
            "givenName": "Max",
        }]
        test_metadata_response(updateMetadata)

        updateMetadata["PublicationYear"] = "2021"
        test_metadata_response(updateMetadata)

    def test_metadata_get_metadata_from_researchId_filtered(self):
        """
        This unit tests the ability of metadata object to get metadata from a given researchId.
        This is the handy way with researchId.
        Notice: Should be very similar to `test_metadata_get_metadata_from_connector`
        """
        md = Metadata(testing=testing_address)

        userId = 20
        researchIndex = 21
        researchId = 22
        projectId = 5

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

        wanted_metadata = {
            "Titles": "",
            "Publisher": ""
        }

        expected_metadata_from_port = {
            "Titles": metadata["Titles"],
            "Publisher": metadata["Publisher"]
        }

        expected_research = {
            "userId": userId,
            "researchIndex": researchIndex
        }

        expected_research["researchId"] = researchId
        expected_research["portIn"] = [{
            "port": "port-zenodo",
            "properties": [{
                    "portType": "metadata", "value": True
            }, {
                "portType": "customProperties", "value": [{
                    "key": "projectId",
                    "value": str(projectId)
                }]
            }]
        },
            {
            "port": "port-owncloud",
            "properties": [{
                "portType": "fileStorage", "value": True
            }]
        }]

        expected_research["portOut"] = [{
            "port": "port-zenodo",
            "properties": [{
                    "portType": "metadata", "value": True
            }]
        }]

        pact.given(
            'The research manager.'
        ).upon_receiving(
            f'A call to get the researchIndex {researchIndex} and user {userId}.'
        ).with_request(
            'GET', f"/research/id/{researchId}"
        ).will_respond_with(200, body=expected_research)

        expected_metadata = []

        # only portOut, because it has a duplicate from portIn and portIn has port-owncloud,
        # which should be out in results, because it is not of type `metadata`.
        for ports in expected_research["portOut"]:
            skip = True

            for prop in ports["properties"]:
                if prop["portType"] == "metadata":
                    skip = False

            if skip:
                continue

            apiKey = "ASDB12345"

            pact.given(
                'An access token for userid.'
            ).upon_receiving(
                f'A call to get the access token for user {userId}.'
            ).with_request(
                'GET', f"/user/{userId}/service/zenodo"
            ).will_respond_with(200, body={"type": "Token", "data": {"access_token": apiKey}})

            port = ports["port"]
            pact.given(
                'A port with metadata informations.'
            ).upon_receiving(
                f'A call to get the metadata from specific projectId {projectId} and port {port} for {expected_metadata_from_port}.'
            ).with_request(
                'GET', f"/metadata/project/{projectId}"
            ).will_respond_with(200, body=expected_metadata_from_port)

            expected_metadata.append({
                "port": port,
                "metadata": expected_metadata_from_port
            })

        with pact:
            result = md.getMetadataForResearch(
                researchId=researchId, metadataFields=wanted_metadata)
        self.assertEqual(result, expected_metadata)

    
    def test_metadata_publish(self):
        # TODO: implement me
        pass
