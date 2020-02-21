import unittest
from src.lib.MetadataService import MetadataService
from src.lib.Port import Port
from src.lib.Project import Project


class Test_MetadataService(unittest.TestCase):
    def test_service_init(self):
        """
        Check a lot of init
        """
        md = MetadataService()

        self.assertEqual(md.getProject(), [])

        md.addProject("admin")

        expected = [
            {
                "userId": "admin",
                "projectId": 1,
                "status": "created",
                "portIn": {},
                "portOut": {}
            }
        ]

        self.assertEqual(md.getProject(), expected)

        md.addProject("user")

        expected = [
            {
                "userId": "admin",
                "projectId": 1,
                "status": "created",
                "portIn": {},
                "portOut": {}
            },
            {
                "userId": "user",
                "projectId": 2,
                "status": "created",
                "portIn": {},
                "portOut": {}
            }
        ]

        self.assertEqual(md.getProject().getJSON(), expected)

        expected = [
            {
                "userId": "admin",
                "projectId": 1,
                "status": "created",
                "portIn": {},
                "portOut": {}
            }
        ]

        self.assertEqual(md.getProject(user="admin").getJSON(), expected)

        expected = [
            {
                "userId": "user",
                "projectId": 2,
                "status": "created",
                "portIn": {},
                "portOut": {}
            }
        ]

        self.assertEqual(md.getProject(user="user").getJSON(), expected)

    def test_service_ports(self):
        """
        Check the setter for imports and portOuts
        """
        md = MetadataService()

        portOwncloud = Port("port-owncloud", fileStorage=True)
        portInvenio = Port("port-invenio", fileStorage=True, metadata=True)

        md.addProject("admin", portIn=[])
        md.addProject("admin", portIn=[portOwncloud])
        md.addProject("user", portIn=[portOwncloud], portOut=[portInvenio])

        expected = [
            {
                "userId": "admin",
                "projectId": 1,
                "status": "created",
                "portIn": [],
                "portOut": []
            },
            {
                "userId": "admin",
                "projectId": 2,
                "status": "created",
                "portIn": [portOwncloud.getJSON()],
                "portOut": []
            },
            {
                "userId": "user",
                "projectId": 3,
                "status": "created",
                "portIn": [portOwncloud.getJSON()],
                "portOut": [portInvenio.getJSON()]
            }
        ]

        self.assertEqual(md.getProject().getJSON(), expected)

    def test_metadata_get_project(self):
        """
        Check the getters for the projects
        """
        md = MetadataService()

        portOwncloud = Port("port-owncloud", fileStorage=True)
        portInvenio = Port("port-invenio", fileStorage=True, metadata=True)

        md.addProject("admin", portIn=[])
        md.addProject("admin", portIn=[portOwncloud])
        proj = Project(user="user", portIn=[portOwncloud], portOut=[portInvenio])
        md.addProject(proj)

        self.assertEqual(md.getProject(id=1), Project(user="admin"))
        self.assertEqual(md.getProject(id=1).getJSON(), Project(user="admin").getJSON())
        self.assertEqual(md.getProject(id=3), proj)

        # check if the id is used as index relative to user, if username is set.
        self.assertEqual(md.getProject(user="admin", id=2), Project(user="admin", portIn=[portOwncloud]))

        with self.assertRaises(IndexError):
            md.getProject(user="user", id=2)

    def test_metadata_port_change(self):
        """
        Check the methods, which changes the values within the object.
        """
        md = MetadataService()

        portOwncloud = Port("port-owncloud", fileStorage=True)
        portInvenio = Port("port-invenio", fileStorage=True, metadata=True)

        md.addProject("admin", portIn=[])
        md.addProject("admin", portIn=[portOwncloud])
        md.addProject("user", portIn=[portOwncloud], portOut=[portInvenio])

        md.getProject(user="admin", id="1")
