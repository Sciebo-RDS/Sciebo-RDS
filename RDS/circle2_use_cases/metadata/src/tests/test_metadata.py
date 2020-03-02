from src.lib.Metadata import Metadata
import unittest
import json
from pactman import Consumer, Provider

# TODO: use pactman for requests

pact = Consumer('UseCaseMetadata').has_pact_with(
    Provider('PortMetadata'), port=3000)

testing_address = "http://localhost:3000"


class Test_Metadata(unittest.TestCase):
    def test_metadata_init(self):
        """
        This unit tests the metadata object constructor.
        """

        md = Metadata()

    def test_metadata_get_projectid(self):
        """
        This unit tests ability of metadata object to get the projectId for corresponding userId and project index.
        """
        md = Metadata()

        def test_projectId(userId, projectIndex):
            nonlocal md

            project = {
                "userId": userId,
                "status": 1,
                "portIn": [],
                "portOut": [],
                "projectId": projectIndex
            }

            pact.given(
                'A project service with projects.'
            ).upon_receiving(
                'A call to get the projectId from userId and projectIndex.'
            ).with_request(
                'GET', f"/projects/{userId}/project/{projectIndex}"
            ).will_respond_with(200, body=json.dumps(project))

            # should be the same as projectIndex, because there are no other projects
            with pact:
                result = md.getProjectId(userId, projectIndex)
            self.assertEqual(result, projectIndex)

        userId = "admin"
        projectIndex = 0
        test_projectId(userId, projectIndex)
        projectIndex = 1
        test_projectId(userId, projectIndex)

        # should be not the same as projectIndex, because there are other projects
        expectedId = 4
        projectIndex = 2
        result = md.getProjectId(userId, projectIndex)
        self.assertEqual(result, expectedId)
        self.assertNotEqual(result, projectIndex)

    def test_metadata_get_connector(self):
        """
        This unit tests the ability of metadata object to get connector from a projectId.
        """
        md = Metadata()

        def test_ports(portIn, portOut):
            def test_getPorts(func, userId, projectId, portIn, portOut):
                project = {
                    "userId": userId,
                    "status": 1,
                    "portIn": portIn,
                    "portOut": portOut,
                    "projectId": projectIndex
                }

                pact.given(
                    'A project service with projects.'
                ).upon_receiving(
                    'A call to get the projectId from userId and projectIndex.'
                ).with_request(
                    'GET', f"/projects/{userId}/project/{projectIndex}"
                ).will_respond_with(200, body=json.dumps(project))

                with pact:
                    result = func(userId, projectIndex)
                return result

            userId = "admin"
            projectIndex = 0

            result = test_getPorts(md.getPortIn, userId,
                                   projectIndex, portIn, portOut)
            self.assertEqual(result, portIn)
            result = test_getPorts(md.getPortOut, userId,
                                   projectIndex, portIn, portOut)
            self.assertEqual(result, portOut)

        ports = [
            ([], []),
            ([], ["port-zenodo"]),
            ([], ["port-owncloud", "port-zenodo"]),
            (["port-owncloud"], []),
            (["port-owncloud", "port-zenodo"], []),
            (["port-owncloud"], ["port-zenodo"]),
            (["port-owncloud"], ["port-owncloud", "port-zenodo"])
        ]

        for portIn, portOut in ports:
            test_ports(portIn, portOut)

    def test_metadata_get_metadata_from_connector(self):
        """
        This unit tests the ability of metadata object to get metadata from a given connector.
        This is the hard way to get informations from a specific port.
        """
        md = Metadata()

        projectId = 0
        port = "localhost:3000"
        metadata = {
            "Creators": ["admin"],
            "Identifiers": ["xyz"],
            "PublicationYear": "2020",
            "Publisher": "University of Münster",
            "ResourceType": "Poster",
            "SchemaVersion": "http://datacite.org/schema/kernel-4",
            "Titles": ["This is a test title"]
        }

        pact.given(
            'A port with metadata informations.'
        ).upon_receiving(
            'A call to get the metadata from specific projectId.'
        ).with_request(
            'GET', f"/project/{projectId}"
        ).will_respond_with(200, body=json.dumps(metadata))

        result = md.getMetadataForProjectFromPort(port, projectId)
        self.assertEqual(result, metadata)

    def test_metadata_get_metadata_from_projectId(self):
        """
        This unit tests the ability of metadata object to get metadata from a given projectId. 
        This is the handy way with projectId.
        Notice: Should be very similar to `test_metadata_get_metadata_from_connector`
        """
        md = Metadata()

        projectId = 0
        metadata = {
            "Creators": [{
                "creatorName":  "Max Mustermann",
                "nameType": "Personal",
                "familyName": "Mustermann",
                "givenName": "Max",
            }],
            "Identifiers": ["xyz"],
            "PublicationYear": "2020",
            "Publisher": "University of Münster",
            "ResourceType": "Poster",
            "SchemaVersion": "http://datacite.org/schema/kernel-4",
            "Titles": ["This is a test title"]
        }

        pact.given(
            'A port with metadata informations.'
        ).upon_receiving(
            'A call to get the metadata from specific projectId.'
        ).with_request(
            'GET', f"/project/{projectId}"
        ).will_respond_with(200, body=json.dumps(metadata))

        result = md.getMetadataForProject(projectId)
        self.assertEqual(result, metadata)

    def test_metadata_update_metadata_from_connector(self):
        """
        This unit tests the ability of metadata object to update metadata from a given connector.
        This is the hard way.
        """
        md = Metadata()

        def test_metadata_response(updateMetadata):
            port = "localhost:3000"
            projectId = 0
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

            for key, value in updateMetadata.items():
                pact.given(
                    'A port with metadata informations.'
                ).upon_receiving(
                    'A call to update the metadata from specific projectId.'
                ).with_request(
                    'PATCH', f"/project/{projectId}/{key}"
                ).will_respond_with(200, body=json.dumps({str(key).lower(): value}))

            result = md.updateMetadataForProjectFromPort(
                port, projectId, updateMetadata)
            self.assertEqual(result, metadata)

        updateMetadata = {}
        updateMetadata["Creators"] = [{
            "creatorName":  "Max Mustermann",
            "nameType": "Personal",
            "familyName": "Mustermann",
            "givenName": "Max",
        }]
        test_metadata_response(updateMetadata)

        updateMetadata["PublicationYear"] = "2020"
        test_metadata_response(updateMetadata)

    def test_metadata_update_metadata_from_projectId(self):
        """
        This unit tests the ability of metadata object to update metadata from a given projectId. 
        This is the handy way.
        Notice: Should be very similar to `test_metadata_get_metadata_from_connector`
        """
        md = Metadata()

        def test_metadata_response(updateMetadata):
            projectId = 0
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

            for key, value in updateMetadata.items():
                pact.given(
                    'A port with metadata informations.'
                ).upon_receiving(
                    'A call to update the metadata from specific projectId.'
                ).with_request(
                    'PATCH', f"/project/{projectId}/{key}"
                ).will_respond_with(200, body=json.dumps({str(key).lower(): value}))

            result = md.updateMetadataForProject(
                projectId, updateMetadata)
            self.assertEqual(metadata, result)

        updateMetadata = {}
        updateMetadata["Creators"] = [
            {
                "creatorName":  "Max Mustermann",
                "nameType": "Personal",
                "familyName": "Mustermann",
                "givenName": "Max",
            }
        ]
        test_metadata_response(updateMetadata)

        updateMetadata["PublicationYear"] = "2021"
        test_metadata_response(updateMetadata)
