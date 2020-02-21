import unittest
from src.lib.Port import Port


class Test_Port(unittest.TestCase):

    def test_port_init(self):
        with self.assertRaises(ValueError):
            Port("owncloud")

        portSmall = Port("port-owncloud")
        portOwncloud = Port("port-owncloud", fileStorage=True)
        portInvenio = Port("port-invenio", fileStorage=True, metadata=True)

        expected = {
            "port": "port-owncloud",
            "properties": {[]}
        }
        self.assertEqual(portSmall.getJSON(), expected)

        expected = {
            "port": "port-owncloud",
            "properties": {
                [
                    {"type": "fileStorage", "value": True}
                ]
            }
        }
        self.assertEqual(portOwncloud.getJSON(), expected)

        expected = {
            "port": "port-invenio",
            "properties": {
                [
                    {"type": "fileStorage", "value": True},
                    {"type": "metadata", "value": True},
                ]
            }
        }
        self.assertEqual(portInvenio.getJSON(), expected)

    def test_port_change(self):
        portOwncloud = Port("port-owncloud")

        expected = {
            "port": "port-owncloud",
            "properties": []
        }
        self.assertEqual(portOwncloud.getJSON(), expected)
        self.assertEqual(portOwncloud, Port("port-owncloud"))

        with self.assertRaises(ValueError):
            portOwncloud.setProperty(1, True)
            portOwncloud.setProperty("fileStorage", 1)

        self.assertFalse(portOwncloud.setProperty("not-found", True))

        self.assertTrue(portOwncloud.setProperty("fileStorage", True))
        expected = {
            "port": "port-owncloud",
            "properties": {
                [
                    {"type": "fileStorage", "value": True}
                ]
            }
        }
        self.assertEqual(portOwncloud.getJSON(), expected)
        self.assertEqual(portOwncloud, Port("port-owncloud", fileStorage=True))

        portOwncloud.setProperty("metadata", True)
        expected = {
            "port": "port-owncloud",
            "properties": {
                [
                    {"type": "fileStorage", "value": True},
                    {"type": "metadata", "value": True}
                ]
            }
        }
        self.assertEqual(portOwncloud.getJSON(), expected)
        self.assertEqual(portOwncloud, Port(
            "port-owncloud", fileStorage=True, metadata=True))
