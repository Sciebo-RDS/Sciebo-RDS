import unittest
from lib.UserService import UserService
from lib.User import User
from lib.Service import Service, OAuth2Service


class test_userservice(unittest.TestCase):
    def setUp(self):
        self.user1 = User("Max Mustermann")

        self.service1 = Service("MusterService")
        self.service2 = Service("BetonService")
        self.service3 = Service("FahrService")

        self.oauthservice1 = OAuth2Service.from_service(
            self.service1, "http://localhost:5000/oauth/authorize", "http://localhost:5000/oauth/refresh", "ABC", "XYZ")
        self.oauthservice2 = OAuth2Service.from_service(
            self.service2, "http://localhost:5001/oauth/authorize", "http://localhost:5001/oauth/refresh", "DEF", "UVW")
        self.oauthservice3 = OAuth2Service.from_service(
            self.service3, "http://localhost:5001/api/authorize", "http://localhost:5001/api/refresh", "GHI", "MNO")

    def test_userservice_input(self):
        userServiceDict = {
            "user": self.user1,
            "service": self.service1,
            "service_user_id": "12345",
            "service_access_token": "ABC",
            "service_refresh_token": "CED"
        }

        userServiceJSON = {"type": "UserService", "data": userServiceDict}

        self.userservice1 = UserService(
            self.user1, self.service1, "12345", "ABC", "CED")
        self.userservice2 = UserService(
            self.user1, self.oauthservice1, "12345", "ABC", "CED")

        with self.assertRaises(ValueError):
            UserService("", "", "", "", "")

        with self.assertRaises(ValueError):
            UserService(self.user1, "", "", "", "")

        with self.assertRaises(ValueError):
            UserService(self.user1, self.service1, "", "", "")

        with self.assertRaises(ValueError):
            UserService(self.user1, self.service1, "a", "", "")

        with self.assertRaises(ValueError):
            UserService(self.user1, self.service1, "", "b", "")

        with self.assertRaises(ValueError):
            UserService(self.user1, self.service1, "", "", "c")

        with self.assertRaises(ValueError):
            UserService(self.user1, self.oauthservice1, "", "", "c")

        self.assertEqual(self.userservice1.to_dict(), userServiceDict)

        self.assertEqual(self.userservice1.to_json(), userServiceJSON)

        self.assertEqual(UserService.from_dict(
            userServiceDict), self.userservice1)

        self.assertEqual(UserService.from_json(
            userServiceJSON), self.userservice1)
