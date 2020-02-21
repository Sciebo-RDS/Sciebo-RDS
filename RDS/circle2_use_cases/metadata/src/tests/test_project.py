import unittest
from src.lib.Project import Project
from src.lib.EnumStatus import Status
from src.lib.Port import Port

class Test_Project(unittest.TestCase):

    def test_project_init(self):
        proj1 = Project("admin")

        expected = {
            "userId": "admin",
            "status": "CREATED",
            "portIn": [],
            "portOut": []
        }
        self.assertEqual(proj1.getJSON(), expected, msg=proj1.getJSON())

        proj2 = Project("admin", portIn=[])
        self.assertEqual(proj1, proj2)

        proj3 = Project("admin", portIn=[], portOut=[])
        self.assertEqual(proj1, proj3)
        self.assertEqual(proj2, proj3)

    def test_project_addPort(self):
        proj1 = Project("admin")
        proj2 = Project("admin", portIn=[])
        proj3 = Project("admin", portIn=[], portOut=[])

        portOwncloud = Port("port-owncloud")

        projOwncloud1 = Project("admin", portIn=[portOwncloud])
        proj1.addPortIn(portOwncloud)
        self.assertEqual(proj1, projOwncloud1)

        projOwncloud2 = Project("admin", portOut=[portOwncloud])
        proj2.addPortOut(portOwncloud)
        self.assertEqual(proj2, projOwncloud2)

        projOwncloud3 = Project(
            "admin", portIn=[portOwncloud], portOut=[portOwncloud])
        proj3.addPortIn(portOwncloud)
        proj3.addPortOut(portOwncloud)
        self.assertEqual(proj3, projOwncloud3)

    def test_project_status(self):
        proj1 = Project("admin")

        self.assertEqual(proj1.status, Status.CREATED)
        self.assertEqual(proj1.nextStatus(), Status.WORK)

        # find the last state
        last = proj1.status
        while proj1.nextStatus() is not last:
            last = proj1.status

        self.assertEqual(proj1.status, Status.DELETED)
