import unittest
from src.lib.Project import Project
from src.lib.EnumStatus import Status
from src.lib.Port import Port


class Test_Project(unittest.TestCase):

    def test_project_init(self):
        proj1 = Project("admin")

        expected = {
            "userId": "admin",
            "status": Status.CREATED.value,
            "portIn": [],
            "portOut": []
        }
        self.assertEqual(proj1.getDict(), expected, msg=proj1.getDict())

        proj2 = Project("admin", portIn=[])
        self.assertEqual(proj1, proj2)

        proj3 = Project("admin", portIn=[], portOut=[])
        self.assertEqual(proj1, proj3)
        self.assertEqual(proj2, proj3)

    def test_project_addPort(self):
        project1 = Project("admin")
        project2 = Project("admin", portIn=[])
        project3 = Project("admin", portIn=[], portOut=[])

        portOwncloud = Port("port-owncloud")

        projOwncloud1 = Project("admin", portIn=[portOwncloud])
        project1.addPortIn(portOwncloud)
        self.assertEqual(project1, projOwncloud1)

        projOwncloud2 = Project("admin", portOut=[portOwncloud])
        project2.addPortOut(portOwncloud)
        self.assertEqual(project2, projOwncloud2, msg="{},{}".format(project2.getDict(), projOwncloud2.getDict()))

        projOwncloud3 = Project(
            "admin", portIn=[portOwncloud], portOut=[portOwncloud])
        project3.addPortIn(portOwncloud)
        project3.addPortOut(portOwncloud)
        self.assertEqual(project3, projOwncloud3)

    def test_project_status(self):
        proj1 = Project("admin")

        self.assertEqual(proj1.status, Status.CREATED)
        self.assertEqual(proj1.nextStatus(), Status.WORK)

        # find the last state
        last = proj1.status
        while proj1.nextStatus() is not last:
            last = proj1.status

        self.assertEqual(proj1.status, Status.DELETED)
