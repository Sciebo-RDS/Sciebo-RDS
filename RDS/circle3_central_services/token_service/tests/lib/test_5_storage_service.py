import unittest
from lib.Service import Service, OAuth2Service
from lib.Storage import Storage
from lib.Token import Token, Oauth2Token
from lib.User import User


class TestStorageService(unittest.TestCase):
    def setUp(self):
        self.empty_storage = Storage()

        self.user1 = User("Max Mustermann")
        self.user2 = User("Mimi Mimikri")

        self.token1 = Token("MusterService", "ABC")
        self.token_like_token1 = Token("MusterService", "DEF")
        self.token2 = Token("BetonService", "XYZ")

        self.oauthtoken1 = Oauth2Token.from_token(self.token1, "X_ABC")
        self.oauthtoken_like_token1 = Oauth2Token.from_token(
            self.token_like_token1, "X_DEF")
        self.oauthtoken2 = Oauth2Token.from_token(self.token2, "X_XYZ")

        self.service1 = Service("MusterService")
        self.service2 = Service("BetonService")

        self.oauthservice1 = OAuth2Service.from_service(
            self.service1, "http://localhost:5000/oauth/refresh", "http://localhost:5000/oauth/authorize", "ABC", "XYZ")
        self.oauthservice1 = OAuth2Service.from_service(
            self.service2, "http://localhost:5001/oauth/refresh", "http://localhost:5001/oauth/authorize", "DEF", "UVW")

    def test_refresh_token(self):
        pass
