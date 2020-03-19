import unittest
from lib.ProjectService import ProjectService
from lib.Port import Port
from lib.Project import Project
from lib.EnumStatus import Status


class Test_projectserviceService(unittest.TestCase):
    def test_service_init(self):
        """
        Check a lot of init
        """
        md = ProjectService()

        self.assertEqual(md.getProject(), [])

        add = md.addProject("admin")
        self.assertEqual(add, Project("admin"))

        expected = [
            {
                "userId": "admin",
                "projectId": 0,
                "projectIndex": 0,
                "status": Status.CREATED.value,
                "portIn": [],
                "portOut": []
            }
        ]

        self.assertEqual([proj.getDict()
                          for proj in md.getProject()], expected)

        md.addProject("user")

        expected = [
            {
                "userId": "admin",
                "projectId": 0,
                "projectIndex": 0,
                "status": Status.CREATED.value,
                "portIn": [],
                "portOut": []
            },
            {
                "userId": "user",
                "projectId": 1,
                "projectIndex": 0,
                "status": Status.CREATED.value,
                "portIn": [],
                "portOut": []
            }
        ]

        self.assertEqual([proj.getDict()
                          for proj in md.getProject()], expected)

        expected = [
            {
                "userId": "admin",
                "projectId": 0,
                "projectIndex": 0,
                "status": Status.CREATED.value,
                "portIn": [],
                "portOut": []
            }
        ]

        self.assertEqual([proj.getDict()
                          for proj in md.getProject(user="admin")], expected)

        expected = [
            {
                "userId": "user",
                "projectId": 1,
                "projectIndex": 0,
                "status": Status.CREATED.value,
                "portIn": [],
                "portOut": []
            }
        ]

        self.assertEqual([proj.getDict()
                          for proj in md.getProject(user="user")], expected)

        with self.assertRaises(ValueError):
            md.getProject(user="user", projectIndex="0")

        self.assertEqual(md.getProject(
            user="user", projectIndex=0).getDict(), expected[0])

    def test_service_ports(self):
        """
        Check the setter for imports and portOuts
        """
        md = ProjectService()

        portOwncloud = Port("port-owncloud", fileStorage=True)
        portInvenio = Port("port-invenio", fileStorage=True, metadata=True)

        md.addProject("admin", portIn=[])
        md.addProject("admin", portIn=[portOwncloud])
        md.addProject("user", portIn=[portOwncloud], portOut=[portInvenio])

        expected = [
            {
                "userId": "admin",
                "projectId": 0,
                "projectIndex": 0,
                "status": Status.CREATED.value,
                "portIn": [],
                "portOut": []
            },
            {
                "userId": "admin",
                "projectId": 1,
                "projectIndex": 1,
                "status": Status.CREATED.value,
                "portIn": [portOwncloud.getDict()],
                "portOut": []
            },
            {
                "userId": "user",
                "projectId": 2,
                "projectIndex": 0,
                "status": Status.CREATED.value,
                "portIn": [portOwncloud.getDict()],
                "portOut": [portInvenio.getDict()]
            }
        ]

        self.assertEqual(md.getDict(), expected)

    def test_projectservice_get_project(self):
        """
        Check the getters for the projects
        """
        md = ProjectService()

        portOwncloud = Port("port-owncloud", fileStorage=True)
        portInvenio = Port("port-invenio", fileStorage=True, metadata=True)

        md.addProject("admin", portIn=[])
        md.addProject("admin", portIn=[portOwncloud])
        proj = Project(user="user", portIn=[
                       portOwncloud], portOut=[portInvenio])
        md.addProject(proj)

        self.assertEqual(md.getProject(projectId=0), Project("admin"))
        # the following is not equal, because the first project comes with a projectId
        self.assertNotEqual(md.getProject(
            projectId=0).getDict(), Project("admin").getDict())
        self.assertEqual(md.getProject(projectId=2), proj)

        # check if the id is used as index relative to user, if username is set.
        self.assertEqual(md.getProject(user="admin", projectIndex=1),
                         Project("admin", portIn=[portOwncloud]))

        from lib.Exceptions.ProjectServiceExceptions import NotFoundIDError
        with self.assertRaises(NotFoundIDError):
            md.getProject(user="user", projectIndex=2)

    def test_projectservice_port_change(self):
        """
        Check the methods, which changes the values within the object.
        """
        md = ProjectService()

        portOwncloud = Port("port-owncloud", fileStorage=True)
        portInvenio = Port("port-invenio", fileStorage=True, metadata=True)

        md.addProject("admin", portIn=[])
        md.addProject("admin", portIn=[portOwncloud])
        md.addProject("user", portIn=[portOwncloud], portOut=[portInvenio])

        md.getProject(user="admin", projectIndex=1)

    def test_projectservice_remove_project(self):
        """
        Check the remove method
        """
        md = ProjectService()

        portOwncloud = Port("port-owncloud", fileStorage=True)
        portInvenio = Port("port-invenio", fileStorage=True, metadata=True)

        id1 = md.addProject("admin", portIn=[]).projectId
        id2 = md.addProject("admin", portIn=[portOwncloud]).projectId
        id3 = md.addProject("user", portIn=[portOwncloud], portOut=[
                            portInvenio]).projectId

        md.removeProject("admin", id1)
        expected = [{
            "userId": "admin",
            "projectId": 0,
            "projectIndex": 0,
            "status": Status.DELETED.value,
            "portIn": [],
            "portOut": []
        }, {
            "userId": "admin",
            "projectId": 1,
            "projectIndex": 1,
            "status": Status.CREATED.value,
            "portIn": [portOwncloud.getDict()],
            "portOut": []
        }, {
            "userId": "user",
            "projectId": 2,
            "projectIndex": 0,
            "status": Status.CREATED.value,
            "portIn": [portOwncloud.getDict()],
            "portOut": [portInvenio.getDict()]
        }]

        self.assertEqual([proj.getDict()
                          for proj in md.getProject()], expected)

        expected[0]["status"] = Status.DELETED.value
        md.removeProject("admin", 0)
        self.assertEqual([proj.getDict()
                          for proj in md.getProject()], expected)

        expected[2]["status"] = Status.DELETED.value
        md.removeProject("user")
        self.assertEqual([proj.getDict()
                          for proj in md.getProject()], expected)

        from lib.Exceptions.ProjectServiceExceptions import NotFoundUserError, NotFoundIDError
        with self.assertRaises(NotFoundUserError):
            md.removeProject("user")

        with self.assertRaises(NotFoundIDError):
            md.removeProject(projectId=2)

        with self.assertRaises(NotFoundUserError):
            md.removeProject("user", projectId=2)

        with self.assertRaises(NotFoundIDError):
            md.removeProject("user", projectIndex=2)

        

    def test_projectservice_get_projectId(self):
        """
        This unit tests the projectid, if it goes up, although we remove some projects.
        """
        md = ProjectService()

        portOwncloud = Port("port-owncloud", fileStorage=True)
        portInvenio = Port("port-invenio", fileStorage=True, metadata=True)

        id1 = md.addProject("admin", portIn=[]).projectId
        id2 = md.addProject("admin", portIn=[portOwncloud]).projectId
        id3 = md.addProject("user", portIn=[portOwncloud], portOut=[
                            portInvenio]).projectId

        # we remove the first one, so there are only 2 projects left
        md.removeProject(projectId=id1)

        # save for later asserts
        id_old = id1

        # now we add one project
        id1 = md.addProject("admin", portIn=[]).projectId

        # all id's should be different
        self.assertNotEqual(id1, id2)
        self.assertNotEqual(id3, id2)
        self.assertNotEqual(id3, id1)

        self.assertNotEqual(id_old, id1)
