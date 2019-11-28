import unittest

from lib.Storage import Storage
from lib.Token import Token, Oauth2Token
from lib.User import User
from lib.Service import Service, OAuth2Service
from lib.Exceptions.StorageException import UserExistsAlreadyError, UserHasTokenAlreadyError, UserNotExistsError


class Test_TokenStorage(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

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

    def test_tokenstorage_empty_string(self):
        with self.assertRaises(ValueError, msg=f"Storage {self.empty_storage}"):
            Token("", "")

        with self.assertRaises(ValueError, msg=f"Storage {self.empty_storage}"):
            Token("MusterService", "")

        with self.assertRaises(ValueError, msg=f"Storage {self.empty_storage}"):
            Token("", "ABC")

        with self.assertRaises(ValueError, msg=f"Storage {self.empty_storage}"):
            Oauth2Token("", "", "")

        with self.assertRaises(ValueError, msg=f"Storage {self.empty_storage}"):
            Oauth2Token("MusterService", "", "")

        with self.assertRaises(ValueError, msg=f"Storage {self.empty_storage}"):
            Oauth2Token("", "ABC", "")

        with self.assertRaises(ValueError, msg=f"Storage {self.empty_storage}"):
            Oauth2Token("", "", "X_ABC")

        with self.assertRaises(ValueError, msg=f"Storage {self.empty_storage}"):
            Oauth2Token("MusterService", "", "X_ABC")

        with self.assertRaises(ValueError, msg=f"Storage {self.empty_storage}"):
            Oauth2Token("", "ABC", "X_ABC")

    def test_tokenstorage_service(self):
        with self.assertRaises(ValueError, msg=f"Service {self.empty_storage}"):
            Service("")

        with self.assertRaises(ValueError, msg=f"Service {self.empty_storage}"):
            OAuth2Service("", "", "", "", "")

        with self.assertRaises(ValueError, msg=f"Service {self.empty_storage}"):
            OAuth2Service("MusterService", "", "", "", "")

        with self.assertRaises(ValueError, msg=f"Service {self.empty_storage}"):
            OAuth2Service("", "http://localhost:5001/oauth/refresh", "", "", "")

        with self.assertRaises(ValueError, msg=f"Service {self.empty_storage}"):
            OAuth2Service("", "", "http://localhost:5001/oauth/authorize", "", "")

        with self.assertRaises(ValueError, msg=f"Service {self.empty_storage}"):
            OAuth2Service("", "", "", "ABC", "")

        with self.assertRaises(ValueError, msg=f"Service {self.empty_storage}"):
            OAuth2Service("", "", "", "", "XYZ")

        with self.assertRaises(ValueError, msg=f"Service {self.empty_storage}"):
            OAuth2Service("MusterService", "http://localhost:5001/oauth/refresh", "", "", "")

        with self.assertRaises(ValueError, msg=f"Service {self.empty_storage}"):
            OAuth2Service("MusterService", "", "http://localhost:5001/oauth/authorize", "", "")
            
        with self.assertRaises(ValueError, msg=f"Service {self.empty_storage}"):
            OAuth2Service("MusterService", "", "", "ABC", "")
            
        with self.assertRaises(ValueError, msg=f"Service {self.empty_storage}"):
            OAuth2Service("MusterService", "", "", "", "XYZ")
            
        with self.assertRaises(ValueError, msg=f"Service {self.empty_storage}"):
            OAuth2Service("MusterService", "http://localhost:5001/oauth/refresh", "", "", "")
            
        with self.assertRaises(ValueError, msg=f"Service {self.empty_storage}"):
            OAuth2Service("MusterService", "http://localhost:5001/oauth/refresh", "http://localhost:5001/oauth/authorize", "", "")

        # same input for authorize and refresh
        with self.assertRaises(ValueError, msg=f"Service {self.empty_storage}"):
            OAuth2Service("MusterService", "http://localhost:5001/oauth/refresh", "http://localhost:5001/oauth/refresh", "", "")

        # no protocoll
        with self.assertRaises(ValueError, msg=f"Service {self.empty_storage}"):
            OAuth2Service("MusterService", "localhost", "http://localhost:5001/oauth/authorize", "", "")
        with self.assertRaises(ValueError, msg=f"Service {self.empty_storage}"):
            OAuth2Service("MusterService", "localhost:5001", "http://localhost:5001/oauth/authorize", "", "")

        # check if root dir is valid
        svc = OAuth2Service("MusterService", "http://localhost:5001", "http://localhost:5001/oauth/authorize", "", "")
        self.assertIsInstance(svc, OAuth2Service)
        svc2 = OAuth2Service("MusterService", "http://localhost:5001/", "http://localhost:5001/oauth/authorize", "", "")
        self.assertIsInstance(svc2, OAuth2Service)
        self.assertEqual(svc, svc2)

    def test_tokenstorage_add_user(self):
        # empty storage
        self.assertEqual(self.empty_storage._storage, {})

        # raise an exception, if a user not exist for token
        with self.assertRaises(UserNotExistsError, msg=f"Storage {self.empty_storage}"):
            self.empty_storage.addTokenToUser(self.user1, self.token1)

        # add one user, so in storage should be one
        expected = {
            "Max Mustermann": {
                "data": self.user1,
                "tokens": []
            }
        }

        self.empty_storage.addUser(self.user1)
        self.assertEqual(self.empty_storage._storage, expected,
                         msg=f"Storage {self.empty_storage}")

        # should raise an Exception, if user already there
        with self.assertRaises(UserExistsAlreadyError, msg=f"Storage {self.empty_storage}"):
            self.empty_storage.addUser(self.user1)

        # add token to user
        expected[self.user1.username]["tokens"].append(self.token1)

        self.empty_storage.addTokenToUser(self.user1, self.token1)
        self.assertEqual(self.empty_storage._storage, expected,
                         msg=f"Storage {self.empty_storage}")

        # raise an exception, if token already there
        with self.assertRaises(UserHasTokenAlreadyError, msg=f"Storage {self.empty_storage}"):
            self.empty_storage.addTokenToUser(self.user1, self.token1)

    def test_tokenstorage_add_token_force(self):
        # add Token to not existing user with force
        expected = {
            "Max Mustermann": {
                "data": self.user1,
                "tokens": [self.token1]
            }
        }

        self.empty_storage.addTokenToUser(self.user1, self.token1, Force=True)
        self.assertEqual(self.empty_storage._storage, expected,
                         msg=f"Storage {self.empty_storage}")

        # now overwrite the already existing token with force
        expected[self.user1.username]["tokens"][0] = self.token_like_token1

        self.empty_storage.addTokenToUser(
            self.user1, self.token_like_token1, Force=True)
        self.assertEqual(self.empty_storage._storage, expected,
                         msg=f"Storage {self.empty_storage}")

    def test_tokenstorage_oauthtokens_add_user(self):
        # empty storage
        self.assertEqual(self.empty_storage._storage, {})

        # raise an exception, if a user not exist for token
        with self.assertRaises(UserNotExistsError, msg=f"Storage {self.empty_storage}"):
            self.empty_storage.addTokenToUser(self.user1, self.oauthtoken1)

        # add one user, so in storage should be one
        expected = {
            "Max Mustermann": {
                "data": self.user1,
                "tokens": []
            }
        }

        self.empty_storage.addUser(self.user1)
        self.assertEqual(self.empty_storage._storage, expected,
                         msg=f"Storage {self.empty_storage}")

        # should raise an Exception, if user already there
        with self.assertRaises(UserExistsAlreadyError, msg=f"Storage {self.empty_storage}"):
            self.empty_storage.addUser(self.user1)

        # add token to user
        expected[self.user1.username]["tokens"].append(self.oauthtoken1)

        self.empty_storage.addTokenToUser(self.user1, self.oauthtoken1)
        self.assertEqual(self.empty_storage._storage, expected,
                         msg=f"Storage {self.empty_storage}")

        # raise an exception, if token already there
        with self.assertRaises(UserHasTokenAlreadyError, msg=f"Storage {self.empty_storage}"):
            self.empty_storage.addTokenToUser(self.user1, self.oauthtoken1)

    def test_tokenstorage_oauthtokens_add_token_force(self):
        # add Token to not existing user with force
        expected = {
            "Max Mustermann": {
                "data": self.user1,
                "tokens": [self.oauthtoken1]
            }
        }

        self.empty_storage.addTokenToUser(
            self.user1, self.oauthtoken1, Force=True)
        self.assertEqual(self.empty_storage._storage, expected,
                         msg=f"Storage {self.empty_storage}")

        # now overwrite the already existing token with force
        expected[self.user1.username]["tokens"][0] = self.oauthtoken_like_token1

        self.empty_storage.addTokenToUser(
            self.user1, self.oauthtoken_like_token1, Force=True)
        self.assertEqual(self.empty_storage._storage, expected,
                         msg=f"Storage {self.empty_storage}")
