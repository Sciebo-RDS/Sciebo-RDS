import unittest
from lib.EnumStatus import Status


def create_app():
    from src import bootstrap
    # creates a test client
    app = bootstrap(use_default_error=True, testing=True).app
    # propagate the exceptions to the test client
    app.config.update({"TESTING": True})

    return app


class TestProjectService(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_add_user(self):
        highest_index = 0

        def test_user_creation(userId):
            nonlocal highest_index

            resp = self.client.get(f"/research/user/{userId}")
            self.assertEqual(resp.status_code, 404)
            self.assertEqual(resp.json, [])

            expected = [{
                "userId": f"{userId}",
                "status": 1,
                "portIn": [],
                "portOut": [],
                "researchId": highest_index,
                "researchIndex": 0
            }]

            highest_index += 1

            resp = self.client.post(
                "/research/user/{}".format(expected[0]["userId"]))
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.json, expected[0])

            resp = self.client.get(f"/research/user/{userId}")
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.json, expected)

        test_user_creation(0)
        test_user_creation("1")
        test_user_creation("admin")
        test_user_creation("user")

    def test_add_and_change_research(self):
        expected = [{
            "userId": "admin",
            "status": 1,
            "portIn": [],
            "portOut": [],
            "researchId": 0,
            "researchIndex": 0
        }, {
            "userId": "admin",
            "status": 1,
            "portIn": [],
            "portOut": [],
            "researchId": 1,
            "researchIndex": 1
        }, {
            "userId": "user",
            "status": 1,
            "portIn": [],
            "portOut": [],
            "researchId": 2,
            "researchIndex": 0
        }]

        portZenodo = {
            "port": "port-zenodo",
            "properties": [{
                "portType": "metadata",
                "value": True
            }]
        }

        portOwncloud = {
            "port": "port-owncloud",
            "properties": [{
                "portType": "fileStorage",
                "value": True
            }]
        }

        expected[1]["portIn"].append(portZenodo)
        expected[2]["portIn"].append(portZenodo)
        expected[2]["portOut"].append(portOwncloud)

        for ex in expected:
            resp = self.client.post(
                "/research/user/{}".format(ex["userId"]), json=ex)
            self.assertEqual(resp.json, ex)
            self.assertEqual(resp.status_code, 200)

            resp = self.client.get(
                "/research/user/{}/research/{}".format(ex["userId"], ex["researchIndex"]))
            self.assertEqual(resp.json, ex)
            self.assertEqual(resp.status_code, 200)

    def test_remove_research(self):
        expected = [{
            "userId": "admin",
            "status": 1,
            "portIn": [],
            "portOut": [],
            "researchId": 0,
            "researchIndex": 0
        }]

        # first it should be empty
        resp = self.client.get(
            "/research/user/{}".format(expected[0]["userId"]))
        self.assertEqual(resp.json, [])

        # add one entry
        resp = self.client.post(
            "/research/user/{}".format(expected[0]["userId"]))
        self.assertEqual(resp.json, expected[0])
        self.assertEqual(resp.status_code, 200)

        # is it there?
        resp = self.client.get(
            "/research/user/{}".format(expected[0]["userId"]))
        self.assertEqual(resp.json, expected)

        # remove it
        resp = self.client.delete("/research/user/{}/research/0".format(
            expected[0]["userId"]))
        self.assertEqual(resp.status_code, 204)

        # status should be set to deleted
        expected[0]["status"] = Status.DELETED.value
        resp = self.client.get(
            "/research/user/{}".format(expected[0]["userId"]))
        self.assertEqual(resp.json, expected)
        self.assertEqual(resp.status_code, 200)

    def test_add_ports(self):
        expected = [{
            "userId": "admin",
            "status": 1,
            "portIn": [],
            "portOut": [],
            "researchId": 0,
            "researchIndex": 0
        }]
        resp = self.client.post(
            "/research/user/{}".format(expected[0]["userId"]))
        self.assertEqual(resp.json, expected[0])
        self.assertEqual(resp.status_code, 200)

        expected[0]["portIn"].append(
            {"port": "port-zenodo", "properties": [{"portType": "metadata", "value": True}]})
        resp = self.client.post("/research/user/{}/research/{}/imports".format(
            expected[0]["userId"], 0), json=expected[0]["portIn"][0])
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, expected[0]["portIn"])

        resp = self.client.get(
            "/research/user/{}".format(expected[0]["userId"]))
        self.assertEqual(resp.json, expected)
        self.assertEqual(resp.status_code, 200)

        expected[0]["portOut"].append(
            {"port": "port-zenodo", "properties": [{"portType": "metadata", "value": True}]})
        resp = self.client.post("/research/user/{}/research/{}/exports".format(
            expected[0]["userId"], 0), json=expected[0]["portOut"][0])
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, expected[0]["portOut"])

        expected[0]["portOut"].append(
            {"port": "port-owncloud", "properties": [{"portType": "fileStorage", "value": True}]})
        resp = self.client.post("/research/user/{}/research/{}/exports".format(
            expected[0]["userId"], 0), json=expected[0]["portOut"][1])
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, expected[0]["portOut"])

        resp = self.client.get(
            "/research/user/{}".format(expected[0]["userId"]))
        self.assertEqual(resp.json, expected)
        self.assertEqual(resp.status_code, 200)

    def test_remove_ports(self):
        expected = [{
            "userId": "admin",
            "status": 1,
            "portIn": [],
            "portOut": [],
            "researchId": 0,
            "researchIndex": 0
        }]
        resp = self.client.post(
            "/research/user/{}".format(expected[0]["userId"]))
        self.assertEqual(resp.json, expected[0])
        self.assertEqual(resp.status_code, 200)

        # add one to portIn and remove it
        expected[0]["portIn"].append(
            {"port": "port-zenodo", "properties": [{"portType": "metadata", "value": True}]})
        resp = self.client.post("/research/user/{}/research/{}/imports".format(
            expected[0]["userId"], 0), json=expected[0]["portIn"][0])
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, expected[0]["portIn"])

        del expected[0]["portIn"][0]
        resp = self.client.delete("/research/user/{}/research/{}/imports/{}".format(
            expected[0]["userId"], 0, 0))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, expected[0]["portIn"])

        # add one to portOut and remove it
        expected[0]["portOut"].append(
            {"port": "port-owncloud", "properties": [{"portType": "fileStorage", "value": True}]})
        resp = self.client.post("/research/user/{}/research/{}/exports".format(
            expected[0]["userId"], 0), json=expected[0]["portOut"][0])
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, expected[0]["portOut"])

        del expected[0]["portOut"][0]
        resp = self.client.delete("/research/user/{}/research/{}/exports/{}".format(
            expected[0]["userId"], 0, 0))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, expected[0]["portOut"])

        resp = self.client.get(
            "/research/user/{}".format(expected[0]["userId"]))
        self.assertEqual(resp.json, expected)
        self.assertEqual(resp.status_code, 200)

    def test_get_researchIndex_and_user_from_id(self):
        # test the projcetId getter

        researchId = 0
        userId = "admin"
        researchIndex = 0

        research = {
            "userId": userId,
            "researchIndex": researchIndex,
            "researchId": researchId,
            "status": 1,
            "portIn": [],
            "portOut": [],
        }

        respProject = self.client.post(
            "/research/user/{}".format(userId)).json

        self.assertEqual(respProject, research)

        resp = self.client.get(
            "/research/user/{}/research/{}".format(userId, researchIndex)).json
        resp2 = self.client.get("research/id/{}".format(researchId)).json

        self.assertEqual(resp, respProject)
        self.assertEqual(resp2, respProject)

    def test_next_status(self):
        expected = [{
            "userId": "admin",
            "status": 1,
            "portIn": [],
            "portOut": [],
            "researchId": 0,
            "researchIndex": 0
        }]
        resp = self.client.post(
            "/research/user/{}".format(expected[0]["userId"]))
        self.assertEqual(resp.json, expected[0])
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get(
            "/research/user/{}/research/{}/status".format(expected[0]["userId"], expected[0]["researchId"]))
        self.assertEqual(resp.json, {"status": expected[0]["status"]})
        self.assertEqual(resp.status_code, 200)

        expected[0]["status"] = 2
        resp = self.client.patch(
            "/research/user/{}/research/{}/status".format(expected[0]["userId"], expected[0]["researchId"]))
        self.assertEqual(resp.json, {"status": expected[0]["status"]})
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get(
            "/research/user/{}/research/{}/status".format(expected[0]["userId"], expected[0]["researchId"]))
        self.assertEqual(resp.json, {"status": expected[0]["status"]})
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get(
            "/research/user/{}".format(expected[0]["userId"]))
        self.assertEqual(resp.json, expected)
        self.assertEqual(resp.status_code, 200)

    def test_customProperties(self):
        custom = {"key": "serviceProjectId", "value": "12345"}

        portExpected = {
            "port": "port-zenodo",
            "properties":
            [
                {
                    "portType": "customProperties",
                    "value": [custom]
                }
            ]
        }

        expected = [{
            "userId": "admin",
            "status": 1,
            "portIn": [portExpected],
            "portOut": [],
            "researchId": 0,
            "researchIndex": 0
        }]
        resp = self.client.post(
            "/research/user/{}".format(expected[0]["userId"]))

        resp = self.client.post("/research/user/{}/research/{}/imports".format(
            expected[0]["userId"], 0), json=expected[0]["portIn"][0])

        self.assertEqual(resp.json, expected[0]["portIn"], msg=resp.json)
        self.assertEqual(resp.status_code, 200)

        expected[0]["portOut"].append(portExpected)

        resp = self.client.post("/research/user/{}/research/{}/exports".format(
            expected[0]["userId"], 0), json=expected[0]["portOut"][0])

        self.assertEqual(resp.json, expected[0]["portOut"])
        self.assertEqual(resp.status_code, 200)

    def test_customProperties_wrong(self):
        custom = {"key": "serviceProjectId", "value": "12345"}

        portNotExpected = {
            "port": "port-zenodo",
            "properties":
            [
                {
                    "portType": "customProperty",
                    "value": [custom]
                }
            ]
        }

        notExpected = [{
            "userId": "admin",
            "status": 1,
            "portIn": [portNotExpected],
            "portOut": [],
            "researchId": 0,
            "researchIndex": 0
        }]
        resp = self.client.post(
            "/research/user/{}".format(notExpected[0]["userId"]))

        resp = self.client.post("/research/user/{}/research/{}/imports".format(
            notExpected[0]["userId"], 0), json=notExpected[0]["portIn"][0])

        self.assertNotEqual(resp.json, notExpected[0]["portIn"], msg=resp.json)
        self.assertEqual(resp.status_code, 200)

        notExpected[0]["portOut"].append(portNotExpected)

        resp = self.client.post("/research/user/{}/research/{}/exports".format(
            notExpected[0]["userId"], 0), json=notExpected[0]["portOut"][0])

        self.assertNotEqual(
            resp.json, notExpected[0]["portOut"])
        self.assertEqual(resp.status_code, 200)

        del portNotExpected["properties"][0]

        self.assertEqual(resp.json, [portNotExpected])
