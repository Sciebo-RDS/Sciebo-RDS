import unittest
from lib.EnumStatus import Status

def create_app():
    from src import bootstrap
    # creates a test client
    app = bootstrap(use_default_error=True).app
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

            resp = self.client.get(f"/projects/user/{userId}")
            self.assertEqual(resp.status_code, 404)
            self.assertEqual(resp.json, [])

            expected = [{
                "userId": f"{userId}",
                "status": 1,
                "portIn": [],
                "portOut": [],
                "projectId": highest_index,
                "projectIndex": 0
            }]

            highest_index += 1

            resp = self.client.post(
                "/projects/user/{}".format(expected[0]["userId"]))
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.json, expected[0])

            resp = self.client.get(f"/projects/user/{userId}")
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.json, expected)

        test_user_creation(0)
        test_user_creation("1")
        test_user_creation("admin")
        test_user_creation("user")

    def test_add_and_change_projects(self):
        expected = [{
            "userId": "admin",
            "status": 1,
            "portIn": [],
            "portOut": [],
            "projectId": 0,
            "projectIndex": 0
        }, {
            "userId": "admin",
            "status": 1,
            "portIn": [],
            "portOut": [],
            "projectId": 1,
            "projectIndex": 1
        }, {
            "userId": "user",
            "status": 1,
            "portIn": [],
            "portOut": [],
            "projectId": 2,
            "projectIndex": 0
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
                "/projects/user/{}".format(ex["userId"]), json=ex)
            self.assertEqual(resp.json, ex)
            self.assertEqual(resp.status_code, 200)

            resp = self.client.get(
                "/projects/user/{}/project/{}".format(ex["userId"], ex["projectIndex"]))
            self.assertEqual(resp.json, ex)
            self.assertEqual(resp.status_code, 200)

    def test_remove_projects(self):
        expected = [{
            "userId": "admin",
            "status": 1,
            "portIn": [],
            "portOut": [],
            "projectId": 0,
            "projectIndex": 0
        }]

        # first it should be empty
        resp = self.client.get(
            "/projects/user/{}".format(expected[0]["userId"]))
        self.assertEqual(resp.json, [])

        # add one entry
        resp = self.client.post(
            "/projects/user/{}".format(expected[0]["userId"]))
        self.assertEqual(resp.json, expected[0])
        self.assertEqual(resp.status_code, 200)

        # is it there?
        resp = self.client.get(
            "/projects/user/{}".format(expected[0]["userId"]))
        self.assertEqual(resp.json, expected)

        # remove it
        resp = self.client.delete("/projects/user/{}/project/0".format(
            expected[0]["userId"]))
        self.assertEqual(resp.status_code, 204)

        # status should be set to deleted
        expected[0]["status"] = Status.DELETED.value
        resp = self.client.get(
            "/projects/user/{}".format(expected[0]["userId"]))
        self.assertEqual(resp.json, expected)
        self.assertEqual(resp.status_code, 200)

    def test_add_ports(self):
        expected = [{
            "userId": "admin",
            "status": 1,
            "portIn": [],
            "portOut": [],
            "projectId": 0,
            "projectIndex": 0
        }]
        resp = self.client.post(
            "/projects/user/{}".format(expected[0]["userId"]))
        self.assertEqual(resp.json, expected[0])
        self.assertEqual(resp.status_code, 200)

        expected[0]["portIn"].append(
            {"port": "port-zenodo", "properties": [{"portType": "metadata", "value": True}]})
        resp = self.client.post("/projects/user/{}/project/{}/imports".format(
            expected[0]["userId"], 0), json=expected[0]["portIn"][0])
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, expected[0]["portIn"])

        resp = self.client.get(
            "/projects/user/{}".format(expected[0]["userId"]))
        self.assertEqual(resp.json, expected)
        self.assertEqual(resp.status_code, 200)

        expected[0]["portOut"].append(
            {"port": "port-zenodo", "properties": [{"portType": "metadata", "value": True}]})
        resp = self.client.post("/projects/user/{}/project/{}/exports".format(
            expected[0]["userId"], 0), json=expected[0]["portOut"][0])
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, expected[0]["portOut"])

        expected[0]["portOut"].append(
            {"port": "port-owncloud", "properties": [{"portType": "fileStorage", "value": True}]})
        resp = self.client.post("/projects/user/{}/project/{}/exports".format(
            expected[0]["userId"], 0), json=expected[0]["portOut"][1])
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, expected[0]["portOut"])

        resp = self.client.get(
            "/projects/user/{}".format(expected[0]["userId"]))
        self.assertEqual(resp.json, expected)
        self.assertEqual(resp.status_code, 200)

    def test_remove_ports(self):
        expected = [{
            "userId": "admin",
            "status": 1,
            "portIn": [],
            "portOut": [],
            "projectId": 0,
            "projectIndex": 0
        }]
        resp = self.client.post(
            "/projects/user/{}".format(expected[0]["userId"]))
        self.assertEqual(resp.json, expected[0])
        self.assertEqual(resp.status_code, 200)

        # add one to portIn and remove it
        expected[0]["portIn"].append(
            {"port": "port-zenodo", "properties": [{"portType": "metadata", "value": True}]})
        resp = self.client.post("/projects/user/{}/project/{}/imports".format(
            expected[0]["userId"], 0), json=expected[0]["portIn"][0])
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, expected[0]["portIn"])

        del expected[0]["portIn"][0]
        resp = self.client.delete("/projects/user/{}/project/{}/imports/{}".format(
            expected[0]["userId"], 0, 0))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, expected[0]["portIn"])

        # add one to portOut and remove it
        expected[0]["portOut"].append(
            {"port": "port-owncloud", "properties": [{"portType": "fileStorage", "value": True}]})
        resp = self.client.post("/projects/user/{}/project/{}/exports".format(
            expected[0]["userId"], 0), json=expected[0]["portOut"][0])
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, expected[0]["portOut"])

        del expected[0]["portOut"][0]
        resp = self.client.delete("/projects/user/{}/project/{}/exports/{}".format(
            expected[0]["userId"], 0, 0))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, expected[0]["portOut"])

        resp = self.client.get(
            "/projects/user/{}".format(expected[0]["userId"]))
        self.assertEqual(resp.json, expected)
        self.assertEqual(resp.status_code, 200)

    def test_get_projectIndex_and_user_from_id(self):
        # test the projcetId getter

        projectId = 0
        userId = "admin"
        projectIndex = 0

        project = {
            "userId": userId,
            "projectIndex": projectIndex,
            "projectId": projectId,
            "status": 1,
            "portIn": [],
            "portOut": [],
        }

        respProject = self.client.post(
            "/projects/user/{}".format(userId)).json

        self.assertEqual(respProject, project)

        resp = self.client.get(
            "/projects/user/{}/project/{}".format(userId, projectIndex)).json
        resp2 = self.client.get("projects/id/{}".format(projectId)).json

        self.assertEqual(resp, respProject)
        self.assertEqual(resp2, respProject)
