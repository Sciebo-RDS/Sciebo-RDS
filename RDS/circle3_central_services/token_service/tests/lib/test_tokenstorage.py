import unittest

from src.lib.TokenStorage import TokenStorage
from src.lib.Token import Token
from src.lib.User import User
from src.lib.Exceptions.StorageException import UserExistsAlreadyError, UserHasTokenAlreadyError, UserNotExistsError


class Test_TokenStorage(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        self.empty_storage = TokenStorage()

        self.user1 = User("Max Mustermann")
        self.user2 = User("Mimi Mimikri")

        self.token1 = Token("MusterService", "ABC")
        self.token2 = Token("BetonService", "XYZ")

    def test_tokenstorage_add_user(self):
        # empty storage
        self.assertEqual(self.empty_storage._storage, {})

        # raise an exception, if a user not exist for token
        with self.assertRaises(UserHasTokenAlreadyError):
            self.empty_storage.addTokenToUser(self.user1, self.token1)

        # add one user, so in storage should be one
        expected = {
            "Max Mustermann": {
                "User": self.user1,
                "Tokens": []
            }
        }

        self.empty_storage.addUser(self.user1)
        self.assertEqual(self.empty_storage._storage, expected,
                         msg=f"Storage {self.empty_storage._storage}")

        # add token to user
        expected[self.user1.username]["Tokens"].append(self.token1)

        # should raise an Exception, if user already there
        with self.assertRaises(UserExistsAlreadyError):
            self.empty_storage.addUser(self.user1)

        self.empty_storage.addTokenToUser(self.user1, self.token1)
        self.assertEqual(self.empty_storage._storage, expected,
                         msg=f"Storage {self.empty_storage._storage}")

        # raise an exception, if token already there
        with self.assertRaises(UserHasTokenAlreadyError):
            self.empty_storage.addTokenToUser(self.user1, self.token1)

    def test_tokenstorage_add_token_force(self):
        # add Token to not existing user with force
        expected = {
            "Max Mustermann": {
                "User": self.user1,
                "Tokens": [self.token1]
            }
        }

        self.empty_storage.addTokenToUser(self.user1, self.token1, Force=True)
        self.assertEqual(self.empty_storage._storage, expected,
                         msg=f"Storage {self.empty_storage._storage}")

        # now overwrite the already existing token with force
        expected[self.user1.username]["Tokens"][0] = self.token2

        self.empty_storage.addTokenToUser(self.user1, self.token2, Force=True)
        self.assertEqual(self.empty_storage._storage, expected,
                         msg=f"Storage {self.empty_storage._storage}")
