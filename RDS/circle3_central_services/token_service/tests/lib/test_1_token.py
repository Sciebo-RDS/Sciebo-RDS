import unittest

from lib.Token import Token, Oauth2Token

class Test_TokenStorage(unittest.TestCase):
    def test_tokenstorage_empty_string(self):
        with self.assertRaises(ValueError):
            Token("", "")

        with self.assertRaises(ValueError):
            Token("MusterService", "")

        with self.assertRaises(ValueError):
            Token("", "ABC")

        with self.assertRaises(ValueError):
            Oauth2Token("", "", "")

        with self.assertRaises(ValueError):
            Oauth2Token("MusterService", "", "")

        with self.assertRaises(ValueError):
            Oauth2Token("", "ABC", "")

        with self.assertRaises(ValueError):
            Oauth2Token("", "", "X_ABC")

        with self.assertRaises(ValueError):
            Oauth2Token("MusterService", "", "X_ABC")

        with self.assertRaises(ValueError):
            Oauth2Token("", "ABC", "X_ABC")
