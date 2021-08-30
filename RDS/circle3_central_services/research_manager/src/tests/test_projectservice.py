import unittest
from lib.ProjectService import ProjectService
from lib.Port import Port
from lib.Project import Project
from lib.EnumStatus import Status
from RDS import Util

from fakeredis import FakeStrictRedis


def get_opts(use_redis=False):
    if use_redis:
        return {
            "rc": FakeStrictRedis(decode_responses=True),
            "use_in_memory_on_failure": False,
        }
    return {"use_in_memory_on_failure": True}


def make_test_case(use_redis=False):
    class Test_projectserviceService(unittest.TestCase):
        def setUp(self):
            Util.monkeypatch(func_name="getJSON")

        def test_service_init(self):
            """
            Check a lot of init
            """
            md = ProjectService(**get_opts())

            self.assertEqual(md.getProject(), [])

            add = md.addProject("admin")
            self.assertEqual(add, Project("admin"))

            expected = [
                {
                    "userId": "admin",
                    "researchId": 0,
                    "researchIndex": 0,
                    "status": Status.CREATED.value,
                    "portIn": [],
                    "portOut": [],
                    "researchname": None,
                }
            ]

            self.assertEqual([proj.getDict()
                              for proj in md.getProject()], expected)

            md.addProject("user")

            expected = [
                {
                    "userId": "admin",
                    "researchId": 0,
                    "researchIndex": 0,
                    "status": Status.CREATED.value,
                    "portIn": [],
                    "portOut": [],
                    "researchname": None,
                },
                {
                    "userId": "user",
                    "researchId": 1,
                    "researchIndex": 0,
                    "status": Status.CREATED.value,
                    "portIn": [],
                    "portOut": [],
                    "researchname": None,
                },
            ]

            self.assertEqual([proj.getDict()
                              for proj in md.getProject()], expected)

            expected = [
                {
                    "userId": "admin",
                    "researchId": 0,
                    "researchIndex": 0,
                    "status": Status.CREATED.value,
                    "portIn": [],
                    "portOut": [],
                    "researchname": None,
                }
            ]

            self.assertEqual(
                [proj.getDict() for proj in md.getProject(user="admin")], expected
            )

            expected = [
                {
                    "userId": "user",
                    "researchId": 1,
                    "researchIndex": 0,
                    "status": Status.CREATED.value,
                    "portIn": [],
                    "portOut": [],
                    "researchname": None,
                }
            ]

            self.assertEqual(
                [proj.getDict() for proj in md.getProject(user="user")], expected
            )

            with self.assertRaises(ValueError):
                md.getProject(user="user", researchIndex="0")

            self.assertEqual(
                md.getProject(
                    user="user", researchIndex=0).getDict(), expected[0]
            )

        def test_highest_index(self):
            md = ProjectService(**get_opts())

            self.assertEqual(md.highest_index, 0)

            portOwncloud = Port("port-owncloud", fileStorage=True)
            portInvenio = Port("port-invenio", fileStorage=True, metadata=True)

            md.addProject("admin", portIn=[])
            self.assertEqual(md.highest_index, 1)

            md.addProject("admin", portIn=[portOwncloud])
            md.addProject("user", portIn=[portOwncloud], portOut=[portInvenio])

            self.assertEqual(md.highest_index, 3)

        def test_service_ports(self):
            """
            Check the setter for imports and portOuts
            """
            md = ProjectService(**get_opts())

            portOwncloud = Port("port-owncloud", fileStorage=True)
            portInvenio = Port("port-invenio", fileStorage=True, metadata=True)

            md.addProject("admin", portIn=[])
            md.addProject("admin", portIn=[portOwncloud])
            md.addProject("user", portIn=[portOwncloud], portOut=[portInvenio])

            expected = [
                {
                    "userId": "admin",
                    "researchId": 0,
                    "researchIndex": 0,
                    "status": Status.CREATED.value,
                    "portIn": [],
                    "portOut": [],
                    "researchname": None,
                },
                {
                    "userId": "admin",
                    "researchId": 1,
                    "researchIndex": 1,
                    "status": Status.CREATED.value,
                    "portIn": [portOwncloud.getDict()],
                    "portOut": [],
                    "researchname": None,
                },
                {
                    "userId": "user",
                    "researchId": 2,
                    "researchIndex": 0,
                    "status": Status.CREATED.value,
                    "portIn": [portOwncloud.getDict()],
                    "portOut": [portInvenio.getDict()],
                    "researchname": None,
                },
            ]

            self.assertEqual(md.getDict(), expected)

        def test_projectservice_get_project(self):
            """
            Check the getters for the projects
            """
            md = ProjectService(**get_opts())

            portOwncloud = Port("port-owncloud", fileStorage=True)
            portInvenio = Port("port-zenodo", fileStorage=True, metadata=True)

            md.addProject("admin", portIn=[])
            md.addProject("admin", portIn=[portOwncloud])
            proj = Project(user="user", portIn=[
                           portOwncloud], portOut=[portInvenio])
            md.addProject(proj)

            self.assertEqual(md.getProject(researchId=0), Project("admin"))
            # the following is not equal, because the first project comes with a researchId
            self.assertNotEqual(
                md.getProject(researchId=0).getDict(), Project(
                    "admin").getDict()
            )
            self.assertEqual(md.getProject(researchId=2), proj)

            # check if the id is used as index relative to user, if username is set.
            self.assertEqual(
                md.getProject(user="admin", researchIndex=1),
                Project("admin", portIn=[portOwncloud]),
            )

            from lib.Exceptions.ProjectServiceExceptions import NotFoundIDError

            with self.assertRaises(NotFoundIDError):
                md.getProject(user="user", researchIndex=2)

        def test_projectservice_port_change(self):
            """
            Check the methods, which changes the values within the object.
            """
            md = ProjectService(**get_opts())

            portOwncloud = Port("port-owncloud", fileStorage=True)
            portInvenio = Port("port-invenio", fileStorage=True, metadata=True)

            md.addProject("admin", portIn=[])
            md.addProject("admin", portIn=[portOwncloud])
            md.addProject("user", portIn=[portOwncloud], portOut=[portInvenio])

            md.getProject(user="admin", researchIndex=1)

        def test_projectservice_remove_project(self):
            """
            Check the remove method
            """
            md = ProjectService(**get_opts())

            portOwncloud = Port("port-owncloud", fileStorage=True)
            portInvenio = Port("port-invenio", fileStorage=True, metadata=True)

            id1 = md.addProject("admin", portIn=[]).researchId
            id2 = md.addProject("admin", portIn=[portOwncloud]).researchId
            id3 = md.addProject(
                "user", portIn=[portOwncloud], portOut=[portInvenio]
            ).researchId

            md.removeProject("admin", id1)
            expected = [
                {
                    "userId": "admin",
                    "researchId": 0,
                    "researchIndex": 0,
                    "status": Status.DELETED.value,
                    "portIn": [],
                    "portOut": [],
                    "researchname": None,
                },
                {
                    "userId": "admin",
                    "researchId": 1,
                    "researchIndex": 1,
                    "status": Status.CREATED.value,
                    "portIn": [portOwncloud.getDict()],
                    "portOut": [],
                    "researchname": None,
                },
                {
                    "userId": "user",
                    "researchId": 2,
                    "researchIndex": 0,
                    "status": Status.CREATED.value,
                    "portIn": [portOwncloud.getDict()],
                    "portOut": [portInvenio.getDict()],
                    "researchname": None,
                },
            ]

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

            from lib.Exceptions.ProjectServiceExceptions import (
                NotFoundUserError,
                NotFoundIDError,
            )

            with self.assertRaises(NotFoundUserError):
                md.removeProject("user")

            with self.assertRaises(NotFoundIDError):
                md.removeProject(researchId=2)

            with self.assertRaises(NotFoundUserError):
                md.removeProject("user", researchId=2)

            with self.assertRaises(NotFoundIDError):
                md.removeProject("user", researchIndex=2)

        def test_projectservice_get_projectId(self):
            """
            This unit tests the projectid, if it goes up, although we remove some projects.
            """
            md = ProjectService(**get_opts())

            portOwncloud = Port("port-owncloud", fileStorage=True)
            portInvenio = Port("port-invenio", fileStorage=True, metadata=True)

            id1 = md.addProject("admin", portIn=[]).researchId
            id2 = md.addProject("admin", portIn=[portOwncloud]).researchId
            id3 = md.addProject(
                "user", portIn=[portOwncloud], portOut=[portInvenio]
            ).researchId

            # we remove the first one, so there are only 2 projects left
            md.removeProject(researchId=id1)

            # save for later asserts
            id_old = id1

            # now we add one project
            id1 = md.addProject("admin", portIn=[]).researchId

            # all id's should be different
            self.assertNotEqual(id1, id2)
            self.assertNotEqual(id3, id2)
            self.assertNotEqual(id3, id1)

            self.assertNotEqual(id_old, id1)

        def test_projectservice_customProp(self):
            """
            This unit tests the projectid, if it goes up, although we remove some projects.
            """
            md = ProjectService(**get_opts())

            custom = {"key": "serviceProjectId", "value": "12345"}
            portOwncloud = Port(
                "port-owncloud", fileStorage=True, customProperties=custom
            )

            id1 = md.addProject("admin", portIn=[portOwncloud]).researchId

            # we remove the first one, so there are only 2 projects left
            self.assertEqual([portOwncloud], md.getProject(
                researchId=id1).getPortIn())

        def test_projectservice_setProject(self):
            """
            This unit tests the setProject method
            """
            md = ProjectService(**get_opts())

            custom = {"key": "serviceProjectId", "value": "12345"}
            portOwncloud = Port(
                "port-owncloud", fileStorage=True, customProperties=custom
            )

            expected_proj1 = Project("admin")

            proj1 = md.addProject("admin", portIn=[])
            self.assertEqual(expected_proj1, md.getProject(
                researchId=proj1.researchId))

            expected_proj1.addPortIn(portOwncloud)

            proj1.addPortIn(portOwncloud)
            md.setProject(proj1.user, proj1)

            self.assertEqual(expected_proj1, md.getProject(
                researchId=proj1.researchId))

    return Test_projectserviceService


class ProjectServiceTestCase(make_test_case()):
    pass


class ProjectServiceRedisBackedTestCase(make_test_case(use_redis=True)):
    def test_highest_index_redis(self):
        opts = get_opts(True)
        md = ProjectService(**opts)

        portOwncloud = Port("port-owncloud", fileStorage=True)
        portInvenio = Port("port-invenio", fileStorage=True, metadata=True)

        id1 = md.addProject("admin", portIn=[]).researchId
        id2 = md.addProject("admin", portIn=[portOwncloud]).researchId

        md2 = ProjectService(**opts)
        self.assertEqual(md.highest_index, 2)
        self.assertEqual(md2.highest_index, 2)

        id3 = md.addProject(
            "user", portIn=[portOwncloud], portOut=[portInvenio]
        ).researchId

        self.assertEqual(md.highest_index, md2.highest_index)
