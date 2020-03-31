from lib.Research import Research
from pactman import Consumer, Provider
import unittest

pact = Consumer('UseCaseMetadataResearch').has_pact_with(
    Provider('PortMetadata'), port=3000)

testing_address = "localhost:3000"


class Test_Research(unittest.TestCase):
    def test_research_init_researchId(self):
        userId = 0
        researchIndex = 0
        researchId = 1

        ports = [
            # no entries
            [],
            # one entry
            [{
                "port": "port-zenodo",
                "properties": [{
                        "portType": "metadata", "value": True
                }]
            }],
            # two entries
            [{
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
        ]

        for portIn in ports:
            for portOut in ports:
                with self.subTest(portIn=portIn, portOut=portOut):

                    research = {
                        "userId": userId,
                        "status": 1,
                        "portIn": portIn,
                        "portOut": portOut,
                        "researchId": researchId,
                        "researchIndex": researchIndex
                    }

                    pact.given(
                        'A research manager.'
                    ).upon_receiving(
                        f'A call to get the researchId from userId and researchIndex with portIn {len(portIn)} and  portOut {len(portOut)}.'
                    ).with_request(
                        'GET', f"/research/id/{researchId}"
                    ).will_respond_with(200, body=research)

                    with pact:
                        p = Research(testing=testing_address,
                                     researchId=researchId)

                    self.assertEqual(p.portIn, research["portIn"])
                    self.assertEqual(p.portOut, research["portOut"])
                    self.assertEqual(
                        p.getPorts(metadata=False), research["portIn"] + research["portOut"])

                    # check, if we can find duplicates and metadata
                    noDuplicates = []

                    for port in research["portIn"] + research["portOut"]:
                        if port not in noDuplicates:
                            for prop in port["properties"]:
                                if prop["portType"] == "metadata":
                                    noDuplicates.append(port)
                                    break

                    self.assertEqual(p.getPorts(), noDuplicates)
                    self.assertEqual(p.getPorts(metadata=True), noDuplicates)

    def test_research_init_researchIndex(self):
        userId = 0
        researchIndex = 0
        researchId = 1

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

        with pact:
            p = Research(testing=testing_address, userId=userId,
                         researchIndex=researchIndex)

        self.assertEqual(p.researchId, researchId)

    def test_research_init_exceptions(self):
        userId = 0
        researchIndex = 0

        with pact:
            with self.assertRaises(ValueError):
                Research(testing=testing_address, userId=userId)

        with pact:
            with self.assertRaises(ValueError):
                Research(testing=testing_address, researchIndex=researchIndex)

    def test_research_custom_properties(self):
        userId = 0
        researchIndex = 0
        researchId = 1

        projectId_zen1 = 1
        projectId_zen2 = 3

        ports = [
            # no entries
            [],
            # one entry
            [{
                "port": "port-zenodo",
                "properties": [{
                    "portType": "metadata", "value": True
                }, {
                    "portType": "customProperties", "value": [{
                        "key": "projectId",
                        "value": str(projectId_zen1)
                    }]
                }]
            }],
            # two entries
            [{
                "port": "port-zenodo",
                "properties": [{
                    "portType": "metadata", "value": True
                }, {
                    "portType": "customProperties", "value": [{
                        "key": "projectId",
                        "value": str(projectId_zen2)
                    }]
                }]
            }, {
                "port": "port-owncloud",
                "properties": [{
                    "portType": "fileStorage", "value": True
                }]
            }]
        ]

        i = 0
        for portIn in ports:
            for portOut in ports:
                with self.subTest(portIn=portIn, portOut=portOut):
                    expected = []

                    for port in portIn + portOut:
                        projectId = None
                        for prop in port["properties"]:
                            if prop.get("portType", "") == "customProperties":
                                for customVal in prop["value"]:
                                    try:
                                        if customVal["key"] == "projectId":
                                            projectId = customVal["value"]
                                            break
                                    except:
                                        pass
                        expected.append((port, projectId))

                    research = {
                        "userId": userId,
                        "status": 1,
                        "portIn": portIn,
                        "portOut": portOut,
                        "researchId": researchId,
                        "researchIndex": researchIndex
                    }

                    pact.given(
                        'A research manager.'
                    ).upon_receiving(
                        f'A call to get the researchId from userId and researchIndex with portIn {len(portIn)} and  portOut {len(portOut)} with projectIds.'
                    ).with_request(
                        'GET', f"/research/id/{researchId}"
                    ).will_respond_with(200, body=research)

                    with pact:
                        p = Research(testing=testing_address,
                                     researchId=researchId)

                    self.assertEqual(p.portIn, research["portIn"])
                    self.assertEqual(p.portOut, research["portOut"])
                    self.assertEqual(
                        p.getPortsWithProjectId(metadata=False), expected)

                    # check, if we can find duplicates and metadata
                    noDuplicates = []

                    for port in expected:
                        if port not in noDuplicates:
                            for prop in port[0]["properties"]:
                                if prop["portType"] == "metadata":
                                    noDuplicates.append(port)
                                    break

                    self.assertEqual(p.getPortsWithProjectId(), noDuplicates)
                    self.assertEqual(p.getPortsWithProjectId(
                        metadata=True), noDuplicates)

                    i += 1
