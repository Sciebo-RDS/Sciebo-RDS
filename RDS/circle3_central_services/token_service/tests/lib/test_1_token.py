import unittest
import json

from lib.Token import Token, OAuth2Token


class Test_TokenStorage(unittest.TestCase):
    def setUp(self):
        self.token1 = Token("MusterService", "ABC")
        self.token2 = Token("BetonService", "DEF")

        self.oauthtoken1 = OAuth2Token.from_token(self.token1, "XYZ")
        self.oauthtoken2 = OAuth2Token.from_token(self.token2, "UVW")

    def test_token_empty_string(self):
        with self.assertRaises(ValueError):
            Token("", "")

        with self.assertRaises(ValueError):
            Token("MusterService", "")

        with self.assertRaises(ValueError):
            Token("", "ABC")

        with self.assertRaises(ValueError):
            OAuth2Token("", "", "")

        # refresh_token is the only parameter, which can be empty
        self.assertIsInstance(OAuth2Token("MusterService", "ABC"), OAuth2Token)

        with self.assertRaises(ValueError):
            OAuth2Token("MusterService", "")

        with self.assertRaises(ValueError):
            OAuth2Token("MusterService", "", "")

        with self.assertRaises(ValueError):
            OAuth2Token("", "ABC", "")

        with self.assertRaises(ValueError):
            OAuth2Token("", "", "X_ABC")

        with self.assertRaises(ValueError):
            OAuth2Token("MusterService", "", "X_ABC")

        with self.assertRaises(ValueError):
            OAuth2Token("", "ABC", "X_ABC")

    def test_token_equal(self):
        self.assertEqual(self.token1, self.token1)
        self.assertNotEqual(self.token1, self.token2)

        self.assertEqual(self.oauthtoken1, self.oauthtoken1)
        self.assertEqual(self.oauthtoken2, self.oauthtoken2)

        self.assertNotEqual(self.token1, self.oauthtoken1,
                            msg=f"\n{self.token1}\n {self.oauthtoken1}")
        self.assertNotEqual(self.oauthtoken1, self.token1)

        self.assertIsInstance(self.oauthtoken1, Token)

    def test_token_json(self):
        expected = {
            "type": "Token",
            "data": {
                "servicename": self.token1._servicename,
                "access_token": self.token1._access_token
            }
        }

        dump = json.dumps(self.token1)
        #self.assertEqual(dump, json.dumps(expected))
        self.assertEqual(Token.from_json(dump), self.token1)

        expected = {
            "type": "OAuth2Token",
            "data": {
                "servicename": self.oauthtoken1.servicename,
                "access_token": self.oauthtoken1.access_token,
                "refresh_token": self.oauthtoken1.refresh_token,
                "expiration_date": str(self.oauthtoken1.expiration_date)
            }
        }
        dump = json.dumps(self.oauthtoken1)
        #self.assertEqual(dump, json.dumps(expected))
        self.assertEqual(OAuth2Token.from_json(dump), self.oauthtoken1)
