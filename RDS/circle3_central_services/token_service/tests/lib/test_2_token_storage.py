import unittest

from lib.Storage import Storage
from lib.Token import Token, OAuth2Token
from lib.User import User
from lib.Exceptions.StorageException import UserExistsAlreadyError, UserHasTokenAlreadyError, UserNotExistsError


class Test_TokenStorage(unittest.TestCase):

    def setUp(self):
        self.empty_storage = Storage()

        self.user1 = User("Max Mustermann")
        self.user2 = User("Mimi Mimikri")

        self.token1 = Token("MusterService", "ABC")
        self.token_like_token1 = Token("MusterService", "DEF")
        self.token2 = Token("BetonService", "XYZ")

        self.oauthtoken1 = OAuth2Token.from_token(self.token1, "X_ABC")
        self.oauthtoken_like_token1 = OAuth2Token.from_token(
            self.token_like_token1, "X_DEF")
        self.oauthtoken2 = OAuth2Token.from_token(self.token2, "X_XYZ")

    def test_storage_listUser(self):
        empty_storage = Storage()
        self.assertEqual(empty_storage.getUsers(), [])
        empty_storage.addUser(self.user1)
        self.assertEqual(empty_storage.getUsers(), [self.user1])
        empty_storage.addUser(self.user2)
        self.assertEqual(empty_storage.getUsers(), [self.user1, self.user2])

        # should raise an Exception, if user already there
        with self.assertRaises(UserExistsAlreadyError, msg=f"Storage {empty_storage}"):
            empty_storage.addUser(self.user1)

    def test_storage_getUser_getToken(self):
        empty_storage = Storage()
        with self.assertRaises(UserNotExistsError):
            empty_storage.getUser(self.user1.username)
        
        with self.assertRaises(UserNotExistsError):
            empty_storage.getTokens(self.user1.username)

        empty_storage.addUser(self.user1)
        empty_storage.addTokenToUser(self.token1, self.user1)

        self.assertEqual(empty_storage.getUser(self.user1.username), self.user1)
        self.assertEqual(empty_storage.getTokens(self.user1.username), [self.token1])

        self.assertEqual(empty_storage.getToken(self.user1.username, 0), self.token1)
        self.assertEqual(empty_storage.getTokens(self.user1), [self.token1])

    def test_tokenstorage_add_user(self):
        # empty storage
        self.assertEqual(self.empty_storage._storage, {})

        # raise an exception, if a user not exist for token
        with self.assertRaises(UserNotExistsError, msg=f"Storage {self.empty_storage}"):
            self.empty_storage.addTokenToUser(self.token1, self.user1)

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

        self.empty_storage.addTokenToUser(self.token1, self.user1)
        self.assertEqual(self.empty_storage._storage, expected,
                         msg=f"Storage {self.empty_storage}")

        # raise an exception, if token already there
        with self.assertRaises(UserHasTokenAlreadyError, msg=f"Storage {self.empty_storage}"):
            self.empty_storage.addTokenToUser(self.token1, self.user1)

    def setUpRemove(self):
        #setUp        
        self.empty_storage.addUser(self.user1)
        self.empty_storage.addUser(self.user2)

    def test_tokenstorage_remove_user(self):
        self.setUpRemove()

        expected = {}
        expected[self.user1.username] = {
            "data": self.user1,
            "tokens": []
        }
        expected[self.user2.username] = {
            "data": self.user2,
            "tokens": []
        }

        # remove user
        self.empty_storage.removeUser(self.user1)
        del expected[self.user1.username]
        self.assertEqual(self.empty_storage._storage, expected)

        with self.assertRaises(UserNotExistsError):
            self.empty_storage.removeUser(self.user1)

        self.empty_storage.removeUser(self.user2)
        del expected[self.user2.username]
        self.assertEqual(self.empty_storage._storage, expected)

        # storage now empty
        self.assertEqual(self.empty_storage.getUsers(), [])




    def test_tokenstorage_add_token_force(self):
        # add Token to not existing user with force
        expected = {
            "Max Mustermann": {
                "data": self.user1,
                "tokens": [self.token1]
            }
        }

        self.empty_storage.addTokenToUser(self.token1, self.user1, Force=True)
        self.assertEqual(self.empty_storage._storage, expected,
                         msg=f"Storage {self.empty_storage}")

        # now overwrite the already existing token with force
        expected[self.user1.username]["tokens"][0] = self.token_like_token1

        self.empty_storage.addTokenToUser(
            self.token_like_token1, self.user1, Force=True)
        self.assertEqual(self.empty_storage._storage, expected,
                         msg=f"Storage {self.empty_storage}")

    def test_tokenstorage_oauthtokens_add_user(self):
        # empty storage
        self.assertEqual(self.empty_storage._storage, {})

        # raise an exception, if a user not exist for token
        with self.assertRaises(UserNotExistsError, msg=f"Storage {self.empty_storage}"):
            self.empty_storage.addTokenToUser(self.oauthtoken1, self.user1)

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

        self.empty_storage.addTokenToUser(self.oauthtoken1, self.user1)
        self.assertEqual(self.empty_storage._storage, expected,
                         msg=f"Storage {self.empty_storage}")

        # raise an exception, if token already there
        with self.assertRaises(UserHasTokenAlreadyError, msg=f"Storage {self.empty_storage}"):
            self.empty_storage.addTokenToUser(self.oauthtoken1, self.user1)

    def test_tokenstorage_oauthtokens_add_token_force(self):
        # add Token to not existing user with force
        expected = {
            "Max Mustermann": {
                "data": self.user1,
                "tokens": [self.oauthtoken1]
            }
        }

        self.empty_storage.addTokenToUser(
            self.oauthtoken1, self.user1, Force=True)
        self.assertEqual(self.empty_storage._storage, expected,
                         msg=f"Storage {self.empty_storage}")

        # now overwrite the already existing token with force
        expected[self.user1.username]["tokens"][0] = self.oauthtoken_like_token1

        self.empty_storage.addTokenToUser(
            self.oauthtoken_like_token1, self.user1, Force=True)
        self.assertEqual(self.empty_storage._storage, expected,
                         msg=f"\nStorage: {self.empty_storage._storage}\n expected: {expected}")
