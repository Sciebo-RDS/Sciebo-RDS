import unittest


class Test_Websocket(unittest.TestCase):
    def test_changeports(self):
        rdsRequest1 = {
            "researchID": 1,
            "import": {
                "add": [],
                "remove": [],
                "change": []
            },
            "export": {
                "add": [
                    {
                        "servicename": "port-zenodo"
                    }
                ],
                "remove": [],
                "change": []
            }
        }

        rdsRequest2 = {
            "researchID": 2,
            "import": {
                "add": [],
                "remove": [],
                "change": []
            },
            "export": {
                "add": [],
                "remove": [
                    {
                        "servicename": "port-datasafe"
                    }
                ],
                "change": []
            }
        }

        rdsRequest3 = {
            "researchID": 1,
            "import": {
                "add": [],
                "remove": [],
                "change": []
            },
            "export": {
                "add": [
                    {
                        "servicename": "port-zenodo"
                    }
                ],
                "remove": [
                    {
                        "servicename": "port-datasafe"
                    }
                ],
                "change": []
            }
        }
