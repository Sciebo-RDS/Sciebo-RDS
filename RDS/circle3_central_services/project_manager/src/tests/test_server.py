import unittest


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

    def test_empty_projects(self):
        def test_user_creation(userId):
            resp = self.client.get(f"/projects/{userId}")
            self.assertEqual(resp.status_code, 404)
            self.assertEqual(resp.json, [])

            expected = [{
                "userId": f"{userId}",
                "status": 1,
                "portIn": [],
                "portOut": []
            }]
            resp = self.client.post(
                "/projects/{}".format(expected[0]["userId"]))
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.json, expected[0])

            resp = self.client.get(f"/projects/{userId}")
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.json, expected)

        test_user_creation(0)
        test_user_creation("1")
        test_user_creation("admin")
        test_user_creation("user")

    def test_get_and_change_projects(self):
        expected = [{
            "userId": "admin",
            "status": 1,
            "portIn": [],
            "portOut": []
        }]
        resp = self.client.post(
            "/projects/{}".format(expected[0]["userId"]))
        self.assertEqual(resp.json, expected[0])
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get(
            "/projects/{}/project/0".format(expected[0]["userId"]))
        self.assertEqual(resp.json, expected[0])
        self.assertEqual(resp.status_code, 200)

        # patch methods not needed, remove it, if you want to change it.
        """expected[0]["userId"] = "user"
        resp = self.client.patch("/projects/{}/project/0".format(
            expected[0]["userId"]), json={"userId": expected[0]["userId"]})
        self.assertEqual(resp.json, expected[0])
        self.assertEqual(resp.status_code, 200)"""

    def test_remove_projects(self):
        expected = [{
            "userId": "admin",
            "status": 1,
            "portIn": [],
            "portOut": []
        }]

        # first it should be empty
        resp = self.client.get(
            "/projects/{}".format(expected[0]["userId"]))
        self.assertEqual(resp.json, [])

        # add one entry
        resp = self.client.post(
            "/projects/{}".format(expected[0]["userId"]))
        self.assertEqual(resp.json, expected[0])
        self.assertEqual(resp.status_code, 200)

        # is it there?
        resp = self.client.get(
            "/projects/{}".format(expected[0]["userId"]))
        self.assertEqual(resp.json, expected)

        # remove it
        resp = self.client.delete("/projects/{}/project/0".format(
            expected[0]["userId"]))
        self.assertEqual(resp.status_code, 204)

        # should be empty again
        resp = self.client.get(
            "/projects/{}".format(expected[0]["userId"]))
        self.assertEqual(resp.json, [])
        self.assertEqual(resp.status_code, 200)

    def test_add_ports(self):
        expected = [{
            "userId": "admin",
            "status": 1,
            "portIn": [],
            "portOut": []
        }]
        resp = self.client.post(
            "/projects/{}".format(expected[0]["userId"]))
        self.assertEqual(resp.json, expected[0])
        self.assertEqual(resp.status_code, 200)

        # TODO test add ports to import and export

    def test_change_ports(self):
        expected = [{
            "userId": "admin",
            "status": 1,
            "portIn": [],
            "portOut": []
        }]
        resp = self.client.post(
            "/projects/{}".format(expected[0]["userId"]))
        self.assertEqual(resp.json, expected[0])
        self.assertEqual(resp.status_code, 200)

        # TODO test add one port  to import and export and change it

    def test_remove_ports(self):
        expected = [{
            "userId": "admin",
            "status": 1,
            "portIn": [],
            "portOut": []
        }]
        resp = self.client.post(
            "/projects/{}".format(expected[0]["userId"]))
        self.assertEqual(resp.json, expected[0])
        self.assertEqual(resp.status_code, 200)

        # TODO test add one port  to import and export and delete it
