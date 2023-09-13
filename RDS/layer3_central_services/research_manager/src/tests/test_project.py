import unittest
from freezegun import freeze_time
from lib.Project import Project
from lib.EnumStatus import Status
from lib.Port import Port


@freeze_time("2023-09-13")
class Test_Project(unittest.TestCase):

    def test_project_init(self):
        proj1 = Project("admin")

        expected = {
            "userId": "admin",
            "status": Status.CREATED.value,
            "portIn": [],
            "portOut": [],
            "researchname": None,
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
        self.assertEqual(project2, projOwncloud2, msg="{},{}".format(
            project2.getDict(), projOwncloud2.getDict()))

        projOwncloud3 = Project(
            "admin", portIn=[portOwncloud], portOut=[portOwncloud])
        project3.addPortIn(portOwncloud)
        project3.addPortOut(portOwncloud)
        self.assertEqual(project3, projOwncloud3)

    def test_project_changePort(self):
        project1 = Project("admin")
        project2 = Project("admin", portIn=[])
        project3 = Project("admin", portIn=[], portOut=[])

        portOwncloud = Port("port-owncloud")
        portOwncloud2 = Port("port-owncloud")
        portOwncloud3 = Port("port-owncloud")

        projOwncloud1 = Project("admin", portIn=[portOwncloud])
        project1.addPortIn(portOwncloud)
        self.assertEqual(project1, projOwncloud1)

        custom = [
            {
                "key": "filepath",
                "value": "/filepath/"
            }
        ]

        projOwncloud2 = Project("admin", portIn=[portOwncloud2])

        portOwncloud.setProperty("customProperties", custom)
        project4 = Project("admin", portIn=[portOwncloud])
        projOwncloud1.addPortIn(portOwncloud)
        self.assertEqual(project4, projOwncloud1)
        self.assertNotEqual(projOwncloud1, projOwncloud2)
        portOwncloud2.setProperty("customProperties", custom)
        self.assertEqual(projOwncloud1, projOwncloud2)
        projOwncloud2.addPortIn(portOwncloud3)
        self.assertNotEqual(projOwncloud1, projOwncloud2)

    def test_project_removePort(self):
        project1 = Project("admin")
        project2 = Project("admin", portIn=[])

        portOwncloud = Port("port-owncloud")

        projOwncloud1 = Project("admin", portIn=[portOwncloud])
        project1.addPortIn(portOwncloud)
        self.assertEqual(project1, projOwncloud1)
        project1.removePortIn(portOwncloud)
        self.assertEqual(project1, Project("admin", portIn=[]))

        projOwncloud2 = Project("admin", portOut=[portOwncloud])
        project2.addPortOut(portOwncloud)
        self.assertEqual(project2, projOwncloud2)
        project2.removePortOut(portOwncloud)
        self.assertEqual(project1, Project("admin", portOut=[]))

    def test_project_status(self):
        proj1 = Project("admin")

        self.assertEqual(proj1.status, Status.CREATED)
        self.assertEqual(proj1.nextStatus(), Status.WORK)

        # find the last state
        last = proj1.status
        while proj1.nextStatus() is not last:
            last = proj1.status

        self.assertEqual(proj1.status, Status.DELETED)

    def test_project_researchname(self):
        self.assertEqual(Project("admin").researchname, None)
        self.assertNotEqual(
            Project("admin", researchname="test1").researchname, None)

        expected_title = "test1"
        proj1 = Project("admin", researchname=expected_title)
        self.assertEqual(proj1.researchname, expected_title)

        expected_title = "test2"
        proj1.setResearchname(expected_title)
        self.assertEqual(proj1.researchname, expected_title)

        self.assertEqual(proj1, Project("admin", researchname=expected_title))
        self.assertNotEqual(proj1.getJSON(), Project(
            "admin").getJSON())
        self.assertEqual(proj1.getJSON(), Project(
            "admin", researchname=expected_title).getJSON())
        self.assertEqual(Project.fromJSON([proj1.getJSON()]), Project.fromJSON([
            Project("admin", researchname=expected_title).getJSON()]))
        self.assertEqual(Project.fromJSON(proj1.getJSON()), Project.fromJSON(
            Project("admin", researchname=expected_title).getJSON()))
        self.assertNotEqual(Project.fromJSON(proj1.getJSON()), Project.fromJSON(
            Project("admin").getJSON()))
