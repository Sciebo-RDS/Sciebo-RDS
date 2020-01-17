import unittest
import json

from lib.Token import Token, OAuth2Token


class Test_TokenStorage(unittest.TestCase):
    def setUp(self):
        from lib.User import User
        self.user1 = User("Max Mustermann")
        self.user2 = User("12345")

        from lib.Service import Service, OAuth2Service
        self.service1 = Service("MusterService")
        self.service2 = Service("BetonService")

        self.token1 = Token(self.user1, self.service1, "ABC")
        self.token2 = Token(self.user1, self.service2, "DEF")

        self.oauthservice1 = OAuth2Service(
            "MusterService", "http://localhost/oauth/authorize", "http://localhost/oauth/token", "MNO", "UVW")
        self.oauthservice2 = OAuth2Service(
            "BetonService", "http://owncloud/oauth/authorize", "http://owncloud/oauth/token", "UVP", "OMN")

        self.oauthtoken1 = OAuth2Token(self.user1, self.oauthservice1, "ABC", "XYZ")
        self.oauthtoken2 = OAuth2Token(self.user1, self.oauthservice2, "DEF", "UVW")


    def test_token_empty_string(self):
        with self.assertRaises(ValueError):
            Token(None, None, "")

        with self.assertRaises(ValueError):
            Token(self.user1, None, "")

        with self.assertRaises(ValueError):
            Token(self.user1, None, "ABC")

        with self.assertRaises(ValueError):
            OAuth2Token(self.user1, None, "", "")

        # refresh_token is the only parameter, which can be empty
        self.assertIsInstance(OAuth2Token(self.user1, self.oauthservice1, "ABC"), OAuth2Token)
        self.assertIsInstance(OAuth2Token(self.user1, self.oauthservice2, "ABC"), Token)

        with self.assertRaises(ValueError):
            OAuth2Token(self.user1, self.oauthservice1, "")

        with self.assertRaises(ValueError):
            OAuth2Token(self.user1, self.oauthservice1, "", "")

        with self.assertRaises(ValueError):
            OAuth2Token(self.user1, None, "ABC", "")

        with self.assertRaises(ValueError):
            OAuth2Token(self.user1, None, "", "X_ABC")

        with self.assertRaises(ValueError):
            OAuth2Token(self.user1, self.oauthservice1, "", "X_ABC")

        with self.assertRaises(ValueError):
            OAuth2Token(self.user1, None, "ABC", "X_ABC")

    def test_token_equal(self):
        self.assertEqual(self.token1, self.token1)
        self.assertNotEqual(self.token1, self.token2)

        self.assertEqual(self.oauthtoken1, self.oauthtoken1)
        self.assertEqual(self.oauthtoken2, self.oauthtoken2)

        self.assertEqual(self.token1, self.oauthtoken1,
                            msg=f"\n{self.token1}\n {self.oauthtoken1}")
        self.assertEqual(self.oauthtoken1, self.token1)

        self.assertIsInstance(self.oauthtoken1, Token)

    def test_token_json(self):
        expected = {
            "type": "Token",
            "data": {
                "service": self.service1,
                "access_token": self.token1._access_token
            }
        }

        dump = json.dumps(self.token1)
        #self.assertEqual(dump, json.dumps(expected))
        self.assertEqual(Token.from_json(dump), self.token1)

        expected = {
            "type": "OAuth2Token",
            "data": {
                "service": self.service1,
                "access_token": self.oauthtoken1.access_token,
                "refresh_token": self.oauthtoken1.refresh_token,
                "expiration_date": str(self.oauthtoken1.expiration_date)
            }
        }
        dump = json.dumps(self.oauthtoken1)
        #self.assertEqual(dump, json.dumps(expected))
        self.assertEqual(OAuth2Token.from_json(dump), self.oauthtoken1)
