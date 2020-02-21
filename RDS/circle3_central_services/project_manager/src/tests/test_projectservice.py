import unittest
from src.lib.ProjectService import ProjectService
from src.lib.Port import Port
from src.lib.Project import Project
from src.lib.EnumStatus import Status


class Test_MetadataService(unittest.TestCase):
    def test_service_init(self):
        """
        Check a lot of init
        """
        md = ProjectService()

        self.assertEqual(md.getProject(), [])

        md.addProject("admin")

        expected = [
            {
                "userId": "admin",
                "projectId": 0,
                "status": Status.CREATED.value,
                "portIn": [],
                "portOut": []
            }
        ]

        self.assertEqual([proj.getDict() for proj in md.getProject()], expected)

        md.addProject("user")

        expected = [
            {
                "userId": "admin",
                "projectId": 0,
                "status": Status.CREATED.value,
                "portIn": [],
                "portOut": []
            },
            {
                "userId": "user",
                "projectId": 1,
                "status": Status.CREATED.value,
                "portIn": [],
                "portOut": []
            }
        ]

        self.assertEqual([proj.getDict() for proj in md.getProject()], expected)

        expected = [
            {
                "userId": "admin",
                "projectId": 0,
                "status": Status.CREATED.value,
                "portIn": [],
                "portOut": []
            }
        ]

        self.assertEqual([proj.getDict() for proj in md.getProject(user="admin")], expected)

        expected = [
            {
                "userId": "user",
                "projectId": 1,
                "status": Status.CREATED.value,
                "portIn": [],
                "portOut": []
            }
        ]

        self.assertEqual([proj.getDict() for proj in md.getProject(user="user")], expected)

        with self.assertRaises(ValueError):
            md.getProject(user="user", id="0")

        self.assertEqual(md.getProject(user="user", id=0).getDict(), expected[0])

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
                "status": Status.CREATED.value,
                "portIn": [],
                "portOut": []
            },
            {
                "userId": "admin",
                "projectId": 1,
                "status": Status.CREATED.value,
                "portIn": [portOwncloud.getDict()],
                "portOut": []
            },
            {
                "userId": "user",
                "projectId": 2,
                "status": Status.CREATED.value,
                "portIn": [portOwncloud.getDict()],
                "portOut": [portInvenio.getDict()]
            }
        ]

        
        self.assertEqual([proj.getDict() for proj in md.getProject()], expected)

    def test_metadata_get_project(self):
        """
        Check the getters for the projects
        """
        md = ProjectService()

        portOwncloud = Port("port-owncloud", fileStorage=True)
        portInvenio = Port("port-invenio", fileStorage=True, metadata=True)

        md.addProject("admin", portIn=[])
        md.addProject("admin", portIn=[portOwncloud])
        proj = Project(user="user", portIn=[portOwncloud], portOut=[portInvenio])
        md.addProject(proj)

        self.assertEqual(md.getProject(id=0), Project("admin"))
        # the following is not equal, because the first project comes with a projectId
        self.assertNotEqual(md.getProject(id=0).getDict(), Project("admin").getDict())
        self.assertEqual(md.getProject(id=2), proj)

        # check if the id is used as index relative to user, if username is set.
        self.assertEqual(md.getProject(user="admin", id=1), Project("admin", portIn=[portOwncloud]))

        with self.assertRaises(IndexError):
            md.getProject(user="user", id=2)

    def test_metadata_port_change(self):
        """
        Check the methods, which changes the values within the object.
        """
        md = ProjectService()

        portOwncloud = Port("port-owncloud", fileStorage=True)
        portInvenio = Port("port-invenio", fileStorage=True, metadata=True)

        md.addProject("admin", portIn=[])
        md.addProject("admin", portIn=[portOwncloud])
        md.addProject("user", portIn=[portOwncloud], portOut=[portInvenio])

        md.getProject(user="admin", id=1)
