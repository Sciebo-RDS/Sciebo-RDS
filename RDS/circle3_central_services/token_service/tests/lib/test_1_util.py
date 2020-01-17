import unittest
import Util
import json

from lib.Service import Service, OAuth2Service
from lib.User import User
from lib.Token import Token, OAuth2Token


class Test_Util(unittest.TestCase):
    def setUp(self):
        self.service1 = Service("MusterService")
        self.service2 = Service("BetonService")
        self.oauthservice1 = OAuth2Service.from_service(
            self.service1, "http://localhost:5000/oauth/authorize", "http://localhost:5000/oauth/refresh", "ABC", "XYZ")

        self.oauthservice2 = OAuth2Service.from_service(
            self.service2, "http://localhost:5000/oauth/authorize", "http://localhost:5000/oauth/refresh", "DEF", "MNO")

        self.user1 = User("Max Mustermann")
        self.user2 = User("Mimi Mimikri")

        self.token1 = Token(self.user1, self.service1, "ABC")
        self.token2 = Token(self.user1, self.service2, "DEF")

        self.oauthtoken1 = OAuth2Token(self.user1, self.oauthservice1, "ABC", "XYZ")
        self.oauthtoken2 = OAuth2Token(self.user1, self.oauthservice2, "DEF", "UVW")

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            Util.load_class_from_json(123)

        with self.assertRaises(ValueError):
            Util.load_class_from_json([])

        with self.assertRaises(ValueError):
            Util.load_class_from_json("")

        with self.assertRaises(ValueError):
            Util.load_class_from_json("Blub bla bla")

        with self.assertRaises(ValueError):
            Util.load_class_from_json(json.dumps({}))

        with self.assertRaises(ValueError):
            jsonStr = json.dumps(self.token1)
            data = json.loads(jsonStr)
            del data["type"]
            Util.load_class_from_json(json.dumps(data))

        with self.assertRaises(ValueError):
            Util.initialize_object_from_json(123)

        with self.assertRaises(ValueError):
            Util.initialize_object_from_json([])

        with self.assertRaises(ValueError):
            Util.initialize_object_from_json("")

        with self.assertRaises(ValueError):
            Util.initialize_object_from_json("blub bla bla")

    def test_load_class_from_json(self):
        self.assertEqual(Util.load_class_from_json(json.dumps(
            self.service1)), self.service1.__class__, msg=json.dumps(self.service1))
        self.assertEqual(Util.load_class_from_json(json.dumps(
            self.oauthservice1)), self.oauthservice1.__class__)

        self.assertEqual(Util.load_class_from_json(
            json.dumps(self.token1)), self.token1.__class__)
        self.assertEqual(Util.load_class_from_json(
            json.dumps(self.oauthtoken1)), self.oauthtoken1.__class__)

        self.assertEqual(Util.load_class_from_json(
            json.dumps(self.user1)), self.user1.__class__)

    def test_load_class_from_dict(self):
        # currently nowhere used.
        pass

    def test_initialize_object(self):
        self.assertEqual(Util.initialize_object_from_json(
            json.dumps(self.token1)), self.token1)
        self.assertEqual(Util.initialize_object_from_json(
            json.dumps(self.oauthtoken1)), self.oauthtoken1)

        self.assertEqual(Util.initialize_object_from_json(
            json.dumps(self.service1)), self.service1)
        self.assertEqual(Util.initialize_object_from_json(
            json.dumps(self.oauthservice1)), self.oauthservice1)

        self.assertEqual(Util.initialize_object_from_json(
            json.dumps(self.user1)), self.user1)
