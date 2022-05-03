import copy
import unittest
from src.Util import (
    parsePortBack,
    parsePort,
    parseResearch,
    parseResearchBack,
    parseAllResearch,
    parseAllResearchBack,
    removeDuplicates,
    applyFilters,
    isServiceInLastServicelist,
)
import sys

sys.path.append("..")


class Test_parser(unittest.TestCase):
    def test_parseResearch(self):
        self.maxDiff = None
        rdsPortBefore = {
            "port": "port-zenodo",
            "properties": [
                {"portType": "metadata", "value": True},
                {
                    "portType": "customProperties",
                    "value": [{"key": "projectId", "value": "843339"}],
                },
            ],
        }
        rdsPort = {
            "port": "port-zenodo",
            "properties": {
                "type": ["metadata"],
                "customProperties": {"projectId": "843339"},
            },
        }

        self.assertEqual(rdsPort, parsePort(rdsPortBefore))
        self.assertEqual(rdsPortBefore, parsePortBack(rdsPort))
        self.assertEqual(rdsPortBefore, parsePortBack(parsePort(rdsPortBefore)))
        rdsResponse = [
            {
                "portIn": [
                    {
                        "port": "port-reva",
                        "properties": [
                            {"portType": "fileStorage", "value": True},
                            {
                                "portType": "customProperties",
                                "value": [{"key": "filepath", "value": "/RDSTest"}],
                            },
                        ],
                    }
                ],
                "portOut": [
                    {
                        "port": "port-zenodo",
                        "properties": [
                            {"portType": "metadata", "value": True},
                            {
                                "portType": "customProperties",
                                "value": [{"key": "projectId", "value": "719218"}],
                            },
                        ],
                    }
                ],
                "researchId": 0,
                "researchIndex": 0,
                "status": 1,
                "userId": "admin",
            },
            {
                "portIn": [
                    {
                        "port": "port-owncloud",
                        "properties": [
                            {"portType": "fileStorage", "value": True},
                            {
                                "portType": "customProperties",
                                "value": [
                                    {"key": "filepath", "value": "/rocratetestfolder"}
                                ],
                            },
                        ],
                    }
                ],
                "portOut": [
                    {
                        "port": "port-datasafe",
                        "properties": [{"portType": "metadata", "value": True}],
                    }
                ],
                "researchId": 1,
                "researchIndex": 1,
                "status": 1,
                "userId": "admin",
            },
            {
                "portIn": [
                    {
                        "port": "port-reva",
                        "properties": [
                            {"portType": "fileStorage", "value": True},
                            {
                                "portType": "customProperties",
                                "value": [{"key": "filepath", "value": "/RDSTest"}],
                            },
                        ],
                    }
                ],
                "portOut": [
                    {
                        "port": "port-zenodo",
                        "properties": [
                            {"portType": "metadata", "value": True},
                            {
                                "portType": "customProperties",
                                "value": [{"key": "projectId", "value": "719218"}],
                            },
                        ],
                    }
                ],
                "researchId": 2,
                "researchIndex": 2,
                "status": 1,
                "userId": "admin",
            },
        ]

        self.assertEqual(
            rdsResponse[0], parseResearchBack(parseResearch(rdsResponse[0]))
        )
        self.assertEqual(
            rdsResponse, parseAllResearchBack(parseAllResearch(rdsResponse))
        )

    def test_removeDuplicate(self):
        expected = [
            {
                "informations": {
                    "credentials": {"password": True, "userId": True},
                    "fileTransferArchive": 0,
                    "fileTransferMode": 0,
                    "implements": ["fileStorage"],
                    "servicename": "port-reva",
                },
                "jwt": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXJ2aWNlbmFtZSI6InBvcnQtcmV2YSIsImF1dGhvcml6ZV91cmwiOm51bGwsImRhdGUiOiIyMDIxLTAyLTI0IDE2OjU3OjAwLjY0MTU4NiIsImltcGxlbWVudHMiOlsiZmlsZVN0b3JhZ2UiXX0.tH-QihxXsDv_9oJNPXLpfB11CiTmwxCJcOrVhR-qfwk",
            },
            {
                "informations": {
                    "credentials": {"password": False, "userId": False},
                    "fileTransferArchive": 0,
                    "fileTransferMode": 0,
                    "implements": ["metadata"],
                    "servicename": "port-datasafe",
                },
                "jwt": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXJ2aWNlbmFtZSI6InBvcnQtZGF0YXNhZmUiLCJhdXRob3JpemVfdXJsIjpudWxsLCJkYXRlIjoiMjAyMS0wMi0yNCAxNjo1NzowMC42NDE5NTAiLCJpbXBsZW1lbnRzIjpbIm1ldGFkYXRhIl19.XZjOjups0zIpFWE4847AiopoKXTKx77M1nfAdnWT72E",
            },
            {
                "informations": {
                    "authorize_url": "https://10.14.29.60/owncloud/index.php/apps/oauth2/authorize%3Fredirect_uri=https://10.14.29.60/owncloud/index.php/apps/rds/oauth&response_type=code&client_id=KGvhrKUA3PJGLqDoLlRbF2hlFZmg7OHZb0bLE6CZhyY5pWpZsn1cylBjNGPn9PQD",
                    "client_id": "KGvhrKUA3PJGLqDoLlRbF2hlFZmg7OHZb0bLE6CZhyY5pWpZsn1cylBjNGPn9PQD",
                    "fileTransferArchive": 0,
                    "fileTransferMode": 0,
                    "implements": ["fileStorage"],
                    "refresh_url": "https://10.14.29.60/owncloud/index.php/apps/oauth2/api/v1/token",
                    "servicename": "port-owncloud",
                },
                "jwt": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXJ2aWNlbmFtZSI6InBvcnQtb3duY2xvdWQiLCJhdXRob3JpemVfdXJsIjoiaHR0cHM6Ly8xMC4xNC4yOS42MC9vd25jbG91ZC9pbmRleC5waHAvYXBwcy9vYXV0aDIvYXV0aG9yaXplJTNGcmVkaXJlY3RfdXJpPWh0dHBzOi8vMTAuMTQuMjkuNjAvb3duY2xvdWQvaW5kZXgucGhwL2FwcHMvcmRzL29hdXRoJnJlc3BvbnNlX3R5cGU9Y29kZSZjbGllbnRfaWQ9S0d2aHJLVUEzUEpHTHFEb0xsUmJGMmhsRlptZzdPSFpiMGJMRTZDWmh5WTVwV3Bac24xY3lsQmpOR1BuOVBRRCIsImRhdGUiOiIyMDIxLTAyLTI0IDE2OjU3OjAwLjY0MjE3OSIsImltcGxlbWVudHMiOlsiZmlsZVN0b3JhZ2UiXX0.uwzm7zT52L2pnHQsiK9qLShywmTmf2x1d3A0VkX5c-A",
            },
        ]
        example = copy.deepcopy(expected)
        example.append(expected[1])

        self.assertEqual(expected, removeDuplicates(example))

    def test_applyfilters_1(self):
        domain = {
            "oauth": {
                "name": "owncloud.local",
                "ADDRESS": "https://owncloud.local/owncloud",
                "OAUTH_CLIENT_ID": "ABC",
                "OAUTH_CLIENT_SECRET": "XYZ",
                "filters": {
                    "only": ["port-datasafe"],
                    "except": ["port-openscienceframework"],
                },
            }
        }

        services = [
            {"informations": {"servicename": "port-datasafe"}},
            {"informations": {"servicename": "port-openscienceframework"}},
            {"informations": {"servicename": "port-zenodo"}},
        ]
        expected = [{"informations": {"servicename": "port-datasafe"}}]
        self.assertEqual(expected, applyFilters(services, domain))

    def test_applyfilters_2(self):
        domain = {
            "oauth": {
                "name": "owncloud.local",
                "ADDRESS": "https://owncloud.local/owncloud",
                "OAUTH_CLIENT_ID": "ABC",
                "OAUTH_CLIENT_SECRET": "XYZ",
                "filters": {
                    "only": [
                        "port-datasafe",
                        "port-openscienceframework",
                    ],
                    "except": ["port-openscienceframework"],
                },
            }
        }

        services = [
            {"informations": {"servicename": "port-datasafe"}},
            {"informations": {"servicename": "port-openscienceframework"}},
            {"informations": {"servicename": "port-zenodo"}},
        ]
        expected = [{"informations": {"servicename": "port-datasafe"}}]
        self.assertEqual(expected, applyFilters(services, domain))

    def test_applyfilters_3(self):
        domain = {
            "oauth": {
                "name": "owncloud.local",
                "ADDRESS": "https://owncloud.local/owncloud",
                "OAUTH_CLIENT_ID": "ABC",
                "OAUTH_CLIENT_SECRET": "XYZ",
                "filters": {
                    "only": ["port-datasafe", "port-zenodo"],
                    "except": ["port-openscienceframework"],
                },
            }
        }

        services = [
            {"informations": {"servicename": "port-datasafe"}},
            {"informations": {"servicename": "port-openscienceframework"}},
            {"informations": {"servicename": "port-zenodo"}},
        ]
        expected = [
            {"informations": {"servicename": "port-datasafe"}},
            {"informations": {"servicename": "port-zenodo"}},
        ]
        self.assertEqual(expected, applyFilters(services, domain))

    def test_applyfilters_4(self):
        domain = {
            "oauth": {
                "name": "owncloud.local",
                "ADDRESS": "https://owncloud.local/owncloud",
                "OAUTH_CLIENT_ID": "ABC",
                "OAUTH_CLIENT_SECRET": "XYZ",
                "filters": {},
            }
        }

        services = [
            {"informations": {"servicename": "port-datasafe"}},
            {"informations": {"servicename": "port-openscienceframework"}},
            {"informations": {"servicename": "port-zenodo"}},
        ]
        expected = [
            {"informations": {"servicename": "port-datasafe"}},
            {"informations": {"servicename": "port-openscienceframework"}},
            {"informations": {"servicename": "port-zenodo"}},
        ]
        self.assertEqual(expected, applyFilters(services, domain))

    def test_applyfilters_5(self):
        domain = {
            "oauth": {
                "name": "owncloud.local",
                "ADDRESS": "https://owncloud.local/owncloud",
                "OAUTH_CLIENT_ID": "ABC",
                "OAUTH_CLIENT_SECRET": "XYZ",
                "filters": {
                    "only": ["port-datasafe", "port-zenodo"],
                },
            }
        }

        services = [
            {"informations": {"servicename": "port-datasafe"}},
            {"informations": {"servicename": "port-openscienceframework"}},
            {"informations": {"servicename": "port-zenodo"}},
        ]
        expected = [
            {"informations": {"servicename": "port-datasafe"}},
            {"informations": {"servicename": "port-zenodo"}},
        ]
        self.assertEqual(expected, applyFilters(services, domain))

    def test_applyfilters_6(self):
        domain = {
            "oauth": {
                "name": "owncloud.local",
                "ADDRESS": "https://owncloud.local/owncloud",
                "OAUTH_CLIENT_ID": "ABC",
                "OAUTH_CLIENT_SECRET": "XYZ",
                "filters": {"except": ["port-openscienceframework"]},
            }
        }

        services = [
            {"informations": {"servicename": "port-datasafe"}},
            {"informations": {"servicename": "port-openscienceframework"}},
            {"informations": {"servicename": "port-zenodo"}},
        ]
        expected = [
            {"informations": {"servicename": "port-datasafe"}},
            {"informations": {"servicename": "port-zenodo"}},
        ]
        self.assertEqual(expected, applyFilters(services, domain))

    def test_applyfilters_7(self):
        domain = {
            "oauth": {
                "name": "owncloud.local",
                "ADDRESS": "https://owncloud.local/owncloud",
                "OAUTH_CLIENT_ID": "ABC",
                "OAUTH_CLIENT_SECRET": "XYZ",
            }
        }

        services = [
            {"informations": {"servicename": "port-datasafe"}},
            {"informations": {"servicename": "port-openscienceframework"}},
            {"informations": {"servicename": "port-zenodo"}},
        ]
        expected = [
            {"informations": {"servicename": "port-datasafe"}},
            {"informations": {"servicename": "port-openscienceframework"}},
            {"informations": {"servicename": "port-zenodo"}},
        ]
        self.assertEqual(expected, applyFilters(services, domain))

    def test_applyfilters_8(self):
        domain = {
            "oauth": {
                "name": "owncloud.local",
                "ADDRESS": "https://owncloud.local/owncloud",
                "OAUTH_CLIENT_ID": "ABC",
                "OAUTH_CLIENT_SECRET": "XYZ",
                "filters": {"only": [], "except": ["port-openscienceframework"]},
            }
        }

        services = [
            {"informations": {"servicename": "port-datasafe"}},
            {"informations": {"servicename": "port-openscienceframework"}},
            {"informations": {"servicename": "port-zenodo"}},
        ]
        expected = [
            {"informations": {"servicename": "port-datasafe"}},
            {"informations": {"servicename": "port-zenodo"}},
        ]
        self.assertEqual(expected, applyFilters(services, domain))

    def test_applyfilters_raise_keyerror(self):
        domain = {
            "oauth": {
                "name": "owncloud.local",
                "ADDRESS": "https://owncloud.local/owncloud",
                "OAUTH_CLIENT_ID": "ABC",
                "OAUTH_CLIENT_SECRET": "XYZ",
                "filters": {"except": ["port-openscienceframework"]},
            }
        }

        services = [
            {"servicename": "port-datasafe"},
            {"servicename": "port-openscienceframework"},
            {"servicename": "port-zenodo"},
        ]
        
        with self.assertRaises(KeyError):
            applyFilters(services, domain)


    def test_servicelist_1(self):
        servicelist = [
            {"informations": {"servicename": "port-datasafe"}},
            {"informations": {"servicename": "port-openscienceframework"}},
            {"informations": {"servicename": "port-zenodo"}},
        ]

        self.assertEqual(
            True,
            isServiceInLastServicelist(
                "port-datasafe", {"servicelist": servicelist}
            ),
        )

    def test_servicelist_2(self):
        servicelist = [
            {"informations": {"servicename": "port-datasafe"}},
            {"informations": {"servicename": "port-openscienceframework"}},
            {"informations": {"servicename": "port-zenodo"}},
        ]

        self.assertEqual(
            False,
            isServiceInLastServicelist(
                "port-notfound", {"servicelist": servicelist}
            ),
        )

    def test_servicelist_3(self):
        servicelist = [
            {"informations": {"servicename": "port-datasafe"}},
            {"informations": {"servicename": "port-openscienceframework"}},
            {"informations": {"servicename": "port-zenodo"}},
        ]

        self.assertEqual(
            True,
            isServiceInLastServicelist(
                "port-datasafe", {"servicelist": servicelist}
            ),
        )
    
    def test_servicelist_4(self):
        servicelist = [
            {"informations": {"servicename": "port-datasafe"}},
            {"informations": {"servicename": "port-openscienceframework"}},
            {"informations": {"servicename": "port-zenodo"}},
        ]

        self.assertEqual(
            True,
            isServiceInLastServicelist(
                "port-datasafe", helperSession={"servicelist": servicelist}
            )
        )
        
    def test_servicelist_5(self):
        servicelist = [
            {"servicename": "port-datasafe"},
            {"servicename": "port-openscienceframework"},
            {"servicename": "port-zenodo"},
        ]

        with self.assertRaises(KeyError):
            isServiceInLastServicelist(
                "port-datasafe", helperSession={"servicelist": servicelist}
            )
    
