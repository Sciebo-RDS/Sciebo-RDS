from src.lib.Metadata import Metadata
from pactman import Consumer, Provider
import unittest
import json


pact = Consumer('UseCaseMetadata').has_pact_with(
    Provider('PortMetadata'), port=3000)

testing_address = "localhost:3000"


class Test_Metadata(unittest.TestCase):
    def test_metadata_init(self):
        """
        This unit tests the metadata object constructor.
        """

        md = Metadata(testing=testing_address)

    def test_metadata_get_projectid(self):
        """
        This unit tests ability of metadata object to get the projectId for corresponding userId and project index.
        """
        md = Metadata(testing=testing_address)

        def test_projectId(userId, projectIndex, projectId):
            nonlocal md

            project = {
                "userId": userId,
                "status": 1,
                "portIn": [],
                "portOut": [],
                "projectIndex": projectIndex,
                "projectId": projectId
            }

            pact.given(
                'A project service with projects.'
            ).upon_receiving(
                f'A call to get the projectId from userId {userId} and projectIndex {projectIndex}.'
            ).with_request(
                'GET', f"/projects/{userId}/project/{projectIndex}"
            ).will_respond_with(200, body=project)

            # should be the same as projectIndex, because there are no other projects
            with pact:
                result = md.getProjectId(userId, projectIndex)
            self.assertEqual(result, projectId)

        userId = "admin"
        projectIndex = 0
        projectId = 0
        test_projectId(userId, projectIndex, projectId)
        projectIndex = 1
        projectId = 4
        test_projectId(userId, projectIndex, projectId)

    @unittest.skip("This test is currently not needed, because getPort is tested in Project")
    def test_metadata_get_connector(self):
        """
        This unit tests the ability of metadata object to get connector from a projectId.
        """
        md = Metadata(testing=testing_address)

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
            ).will_respond_with(200, body=project)

            with pact:
                result = func(userId, projectIndex)
            return result

        userId = "admin"
        projectIndex = 0

        for portIn in [[], ["port-owncloud"], ["port-owncloud", "port-zenodo"]]:
            for portOut in [[], ["port-owncloud"], ["port-owncloud", "port-zenodo"]]:
                with self.subTest(portIn=portIn, portOut=portOut):
                    result = test_getPorts(md.getPortIn, userId,
                                           projectIndex, portIn, portOut)
                    self.assertEqual(result, portIn)

                    result = test_getPorts(md.getPortOut, userId,
                                           projectIndex, portIn, portOut)
                    self.assertEqual(result, portOut)

    def test_metadata_get_metadata_from_connector(self):
        """
        This unit tests the ability of metadata object to get metadata from a given connector.
        This is the hard way to get informations from a specific port.
        """
        md = Metadata(testing=testing_address)

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
            'GET', f"/metadata/project/{projectId}"
        ).will_respond_with(200, body=metadata)

        with pact:
            result = md.getMetadataForProjectFromPort(port, projectId)
        self.assertEqual(result, metadata)

    def test_metadata_get_metadata_from_projectId(self):
        """
        This unit tests the ability of metadata object to get metadata from a given projectId. 
        This is the handy way with projectId.
        Notice: Should be very similar to `test_metadata_get_metadata_from_connector`
        """
        md = Metadata(testing=testing_address)

        userId = 20
        projectIndex = 21
        projectId = 22

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

        expected_project = {
            "userId": userId,
            "projectIndex": projectIndex
        }

        expected_project["projectId"] = projectId
        expected_project["portIn"] = [{
            "port": "port-zenodo",
            "properties": [{
                    "portType": "metadata", "value": True
            }]
        },
            {
            "port": "port-owncloud",
            "properties": [{
                "portType": "fileStorage", "value": True
            }]
        }]

        expected_project["portOut"] = [{
            "port": "port-zenodo",
            "properties": [{
                    "portType": "metadata", "value": True
            }]
        }]

        pact.given(
            'The project manager.'
        ).upon_receiving(
            f'A call to get the projectIndex {projectIndex} and user {userId}.'
        ).with_request(
            'GET', f"/projects/id/{projectId}"
        ).will_respond_with(200, body=expected_project)

        expected_metadata = []

        # only portOut, because it has a duplicate from portIn and portIn has port-owncloud,
        # which should be out in results, because it is not of type `metadata`.
        for ports in expected_project["portOut"]:
            skip = True

            for prop in ports["properties"]:
                if prop["portType"] == "metadata":
                    skip = False

            if skip:
                continue

            port = ports["port"]
            pact.given(
                'A port with metadata informations.'
            ).upon_receiving(
                f'A call to get the metadata from specific projectId {projectId} and port {port}.'
            ).with_request(
                'GET', f"/metadata/project/{projectId}"
            ).will_respond_with(200, body=metadata)

            expected_metadata.append({
                port: metadata
            })

        with pact:
            result = md.getMetadataForProject(projectId=projectId)
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

            for key, value in updateMetadata.items():
                key = str(key).lower()

                pact.given(
                    'A port with metadata informations.'
                ).upon_receiving(
                    f'A call to update the metadata from specific projectId {projectId} for key {key}.'
                ).with_request(
                    'PATCH', f"/metadata/project/{projectId}/{key}"
                ).will_respond_with(200, body=value)

            pact.given(
                'A port with metadata informations.'
            ).upon_receiving(
                f'A call to get the metadata from specific projectId {projectId}.'
            ).with_request(
                'GET', f"/metadata/project/{projectId}"
            ).will_respond_with(200, body=metadata)

            with pact:
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
        test_metadata_response(updateMetadata, 10)

        updateMetadata["PublicationYear"] = "2020"
        test_metadata_response(updateMetadata, 11)

    def test_metadata_update_metadata_from_projectId(self):
        """
        This unit tests the ability of metadata object to update metadata from a given projectId. 
        This is the handy way.
        Notice: Should be very similar to `test_metadata_get_metadata_from_connector`
        """
        md = Metadata(testing=testing_address)

        def test_metadata_response(updateMetadata):
            userId = 0
            projectIndex = 0
            projectId = 2

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
                "projectIndex": projectIndex
            }

            expected_project = expected_pid.copy()
            expected_project["status"] = 1
            expected_project["projectId"] = projectId
            expected_project["portIn"] = [{
                "port": "port-zenodo",
                "properties": [{
                        "portType": "metadata", "value": True
                }]
            }, {
                "port": "port-owncloud",
                "properties": [{
                        "portType": "fileStorage", "value": True
                }]
            }]

            expected_project["portOut"] = [{
                "port": "port-zenodo",
                "properties": [{
                        "portType": "metadata", "value": True
                }]
            }]

            pact.given(
                'The project manager.'
            ).upon_receiving(
                'A call to get the projectIndex and user.'
            ).with_request(
                'GET', f"/projects/id/{projectId}"
            ).will_respond_with(200, body=expected_project)

            expected_metadata = []
            # add patch requests for all given example ports, which are portType `metadata`
            for key, value in updateMetadata.items():
                for ports in expected_project["portOut"]:
                    skip = True

                    for prop in ports["properties"]:
                        if prop["portType"] == "metadata":
                            skip = False

                    if skip:
                        continue

                    port = ports["port"]
                    key = str(key).lower()

                    pact.given(
                        'A port with metadata informations.'
                    ).upon_receiving(
                        f'A call to update the metadata from specific projectId {projectId} for key {key} and port {port}.'
                    ).with_request(
                        'PATCH', f"/metadata/project/{projectId}/{key}"
                    ).will_respond_with(200, body=value)

            pact.given(
                'A port with metadata informations.'
            ).upon_receiving(
                f'A call to get the metadata from specific projectId {projectId} for key {key} and for port {port}.'
            ).with_request(
                'GET', f"/metadata/project/{projectId}"
            ).will_respond_with(200, body=metadata)

            expected_metadata.append({
                port: metadata
            })

            with pact:
                result = md.updateMetadataForProject(
                    projectId, updateMetadata)
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
