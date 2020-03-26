import unittest
from lib.Port import Port


class Test_Port(unittest.TestCase):

    def test_port_init(self):
        with self.assertRaises(ValueError):
            Port("owncloud")

        portSmall = Port("port-owncloud")
        portOwncloud = Port("port-owncloud", fileStorage=True)
        portInvenio = Port("port-invenio", fileStorage=True, metadata=True)

        expected = {
            "port": "port-owncloud",
            "properties": []
        }
        self.assertEqual(portSmall.getDict(), expected)

        expected = {
            "port": "port-owncloud",
            "properties":
                [
                    {"portType": "fileStorage", "value": True}
                ]
        }
        self.assertEqual(portOwncloud.getDict(), expected)

        expected = {
            "port": "port-invenio",
            "properties":
                [
                    {"portType": "fileStorage", "value": True},
                    {"portType": "metadata", "value": True},
                ]
        }
        self.assertEqual(portInvenio.getDict(), expected)

    def test_port_change(self):
        portOwncloud = Port("port-owncloud")

        expected = {
            "port": "port-owncloud",
            "properties": []
        }
        self.assertEqual(portOwncloud.getDict(), expected)
        self.assertEqual(portOwncloud, Port("port-owncloud"))

        with self.assertRaises(ValueError):
            portOwncloud.setProperty(1, True)
            portOwncloud.setProperty("fileStorage", 1)

        self.assertFalse(portOwncloud.setProperty("not-found", True))

        self.assertTrue(portOwncloud.setProperty("fileStorage", True))
        expected = {
            "port": "port-owncloud",
            "properties":
                [
                    {"portType": "fileStorage", "value": True}
                ]
        }
        self.assertEqual(portOwncloud.getDict(), expected)
        self.assertEqual(portOwncloud, Port("port-owncloud", fileStorage=True))

        portOwncloud.setProperty("metadata", True)
        expected = {
            "port": "port-owncloud",
            "properties":
                [
                    {"portType": "fileStorage", "value": True},
                    {"portType": "metadata", "value": True}
                ]
        }
        self.assertEqual(portOwncloud.getDict(), expected)
        self.assertEqual(portOwncloud, Port(
            "port-owncloud", fileStorage=True, metadata=True))
<<<<<<< HEAD

    def test_port_customProperties(self):
        custom = [
            {
                "key": "serviceProjectId",
                "value": "12345"
            }
        ]

        expected = {
            "port": "port-owncloud",
            "properties":
                [
                    {
                        "portType": "customProperties",
                        "value": custom
                    }
                ]
        }

        portOwncloud = Port("port-owncloud", customProperties=custom)

        self.assertEqual(portOwncloud.getDict(), expected)

        expected["port"] = "port-zenodo"
        portZenodo = Port("port-zenodo")
        portZenodo.setProperty("customProperties", custom)

        self.assertEqual(portZenodo.getDict(), expected)

        self.assertEqual(portZenodo, Port.fromDict(portZenodo.getDict()))
        self.assertNotEqual(portOwncloud, Port.fromDict(portZenodo.getDict()))
        self.assertNotEqual(Port("port-zenodo"),
                            Port.fromDict(portZenodo.getDict()))
=======
>>>>>>> master
