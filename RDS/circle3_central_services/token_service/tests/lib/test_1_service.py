import unittest
from lib.Service import Service, OAuth2Service


class TestService(unittest.TestCase):
    def setUp(self):
        self.service1 = Service("MusterService")
        self.service2 = Service("BetonService")
        self.service3 = Service("FahrService")

        self.oauthservice1 = OAuth2Service.from_service(
            self.service1, "http://localhost:5000/oauth/authorize", "http://localhost:5000/oauth/refresh", "ABC", "XYZ")
        self.oauthservice2 = OAuth2Service.from_service(
            self.service2, "http://localhost:5001/oauth/authorize", "http://localhost:5001/oauth/refresh", "DEF", "UVW")
        self.oauthservice3 = OAuth2Service.from_service(
            self.service3, "http://localhost:5001/api/authorize", "http://localhost:5001/api/refresh", "GHI", "MNO")

    def test_service(self):
        with self.assertRaises(ValueError):
            Service("")

        with self.assertRaises(ValueError):
            OAuth2Service("", "", "", "", "")

        with self.assertRaises(ValueError):
            OAuth2Service("MusterService", "", "", "", "")

        with self.assertRaises(ValueError):
            OAuth2Service(
                "", "http://localhost:5001/oauth/authorize", "", "", "")

        with self.assertRaises(ValueError):
            OAuth2Service(
                "", "", "http://localhost:5001/oauth/refresh", "", "")

        with self.assertRaises(ValueError):
            OAuth2Service("", "", "", "ABC", "")

        with self.assertRaises(ValueError):
            OAuth2Service("", "", "", "", "XYZ")

        with self.assertRaises(ValueError):
            OAuth2Service("MusterService",
                          "http://localhost:5001/oauth/authorize", "", "", "")

        with self.assertRaises(ValueError):
            OAuth2Service("MusterService", "",
                          "http://localhost:5001/oauth/refresh", "", "")

        with self.assertRaises(ValueError):
            OAuth2Service("MusterService", "", "", "ABC", "")

        with self.assertRaises(ValueError):
            OAuth2Service("MusterService", "", "", "", "XYZ")

        with self.assertRaises(ValueError):
            OAuth2Service("MusterService",
                          "http://localhost:5001/oauth/refresh", "", "", "")

        with self.assertRaises(ValueError):
            OAuth2Service("MusterService", "http://localhost:5001/oauth/authorize",
                          "http://localhost:5001/oauth/refresh", "", "")

        # same input for authorize and refresh
        with self.assertRaises(ValueError):
            OAuth2Service("MusterService", "http://localhost:5001/oauth/authorize",
                          "http://localhost:5001/oauth/refresh", "", "")

    def test_service_no_protocoll(self):
        # no protocoll
        with self.assertRaises(ValueError):
            OAuth2Service("MusterService", "localhost",
                          "http://localhost:5001/oauth/refresh", "ABC", "XYZ")

        with self.assertRaises(ValueError):
            OAuth2Service("MusterService", "localhost:5001",
                          "http://localhost:5001/oauth/authorize", "ABC", "XYZ")

        with self.assertRaises(ValueError):
            OAuth2Service("MusterService", "localhost:5001/oauth/authorize",
                          "http://localhost:5001/oauth/refresh", "ABC", "XYZ")

        with self.assertRaises(ValueError):
            OAuth2Service("MusterService", "http://localhost:5001",
                          "localhost:5001/oauth/refresh", "ABC", "XYZ")

        with self.assertRaises(ValueError):
            OAuth2Service("MusterService", "http://localhost:5001",
                          "localhost:5001/oauth/authorize", "ABC", "XYZ")

    def test_service_equal(self):
        # check if they are equal
        svc1 = OAuth2Service("MusterService", "http://localhost:5001",
                             "http://localhost:5001/oauth/refresh", "ABC", "XYZ")
        svc2 = OAuth2Service("MusterService", "http://localhost:5001",
                             "http://localhost:5001/oauth/refresh", "ABC", "XYZ")
        self.assertEqual(
            svc1, svc2, msg=f"Service1: {svc1}\n Service2: {svc2}")

    def test_service_trailing_slash(self):
        # check if root dir is valid
        svc1 = OAuth2Service("MusterService", "http://localhost:5001",
                             "http://localhost:5001/oauth/refresh", "ABC", "XYZ")
        self.assertIsInstance(svc1, OAuth2Service)

        svc2 = OAuth2Service("MusterService", "http://localhost:5001/",
                             "http://localhost:5001/oauth/refresh/", "ABC", "XYZ")
        self.assertIsInstance(svc2, OAuth2Service)

        # check if they are equal
        self.assertEqual(
            svc1, svc2, msg=f"Service1: {svc1}\n Service2: {svc2}")

    def test_service_check_raises(self):
        svc1 = OAuth2Service("MusterService", "http://localhost:5001",
                             "http://localhost:5001/oauth/refresh", "ABC", "XYZ")

        from lib.User import User
        from lib.Token import Token, OAuth2Token
        with self.assertRaises(ValueError):
            svc1.refresh(Token(User("Max Mustermann"), svc1, "ABC"))

        with self.assertRaises(ValueError):
            svc1.refresh("asd")

        with self.assertRaises(ValueError):
            svc1.refresh(123)
