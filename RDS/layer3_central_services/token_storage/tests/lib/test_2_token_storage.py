import unittest
import pytest

from lib.Storage import Storage
from RDS import Token, OAuth2Token, User, LoginService, OAuth2Service, Util
from lib.Exceptions.StorageException import (
    UserExistsAlreadyError,
    UserHasTokenAlreadyError,
    UserNotExistsError,
)
from RDS.ServiceException import (
    ServiceNotExistsError,
    ServiceExistsAlreadyError,
)

from fakeredis import FakeStrictRedis


def get_opts(use_redis=False):
    if use_redis:
        return {
            "rc": FakeStrictRedis(decode_responses=True),
            "use_in_memory_on_failure": False,
        }
    return {"use_in_memory_on_failure": True}


def make_test_case(use_redis=False):
    class Test_TokenStorage(unittest.TestCase):
        def setUp(self):

            Util.monkeypatch()
            self.empty_storage = Storage(**get_opts(use_redis))

            self.user1 = User("Max Mustermann")
            self.user2 = User("Mimi Mimikri")

            self.service1 = LoginService(
                servicename="MusterService", implements=["metadata"]
            )
            self.service2 = LoginService(
                servicename="FahrService", implements=["metadata"]
            )
            self.oauthservice1 = OAuth2Service(
                servicename="BetonService",
                implements=["metadata"],
                authorize_url="http://localhost/oauth/authorize",
                refresh_url="http://localhost/oauth/token",
                client_id="MNO",
                client_secret="UVW",
            )
            self.oauthservice2 = OAuth2Service(
                servicename="FlugService",
                implements=["metadata"],
                authorize_url="http://localhost21/oauth/authorize",
                refresh_url="http://localhost21/oauth/token",
                client_id="XCA",
                client_secret="BCXY",
            )

            self.empty_storage.addService(self.service1)
            self.empty_storage.addService(self.oauthservice1)
            self.empty_storage.addService(self.oauthservice2)

            self.token1 = Token(self.user1, self.service1, "ABC")
            self.token_like_token1 = Token(self.user1, self.service1, "DEF")
            self.token2 = Token(self.user1, self.oauthservice1, "XYZ")
            self.token3 = Token(self.user2, self.service2, "XASD")
            self.token4 = Token(self.user2, self.service1, "IOAJSD")

            self.oauthtoken1 = OAuth2Token(
                self.user1, self.oauthservice1, "ABC", "X_ABC"
            )
            self.oauthtoken_like_token1 = OAuth2Token(
                self.user1, self.oauthservice1, "ABC", "X_DEF"
            )
            self.oauthtoken2 = OAuth2Token(
                self.user1, self.oauthservice1, "XYZ", "X_XYZ"
            )

            self.oauthtoken3 = OAuth2Token(
                self.user1, self.oauthservice2, "XYZ", "X_XYZ"
            )

        def test_storage_listUser(self):
            empty_storage = Storage(**get_opts())
            self.assertEqual(empty_storage.getUsers(), [])
            empty_storage.addUser(self.user1)
            self.assertEqual(empty_storage.getUsers(), [self.user1])
            empty_storage.addUser(self.user2)
            self.assertEqual(empty_storage.getUsers(), [self.user1, self.user2])

            # should raise an Exception, if user already there
            with self.assertRaises(
                UserExistsAlreadyError, msg=f"Storage {empty_storage}"
            ):
                empty_storage.addUser(self.user1)

        def test_tokenstorage_add_service(self):
            empty_storage = Storage(**get_opts())

            empty_storage.addUser(self.user1)
            #  test the exception raise
            with self.assertRaises(ServiceNotExistsError):
                empty_storage.addTokenToUser(self.token1, self.user1)
            # now should work
            empty_storage.addService(self.service1)
            empty_storage.addTokenToUser(self.token1, self.user1)

            self.assertEqual(empty_storage.getTokens(self.user1), [self.token1])

            with self.assertRaises(ServiceExistsAlreadyError):
                self.empty_storage.addService(self.service1)

        def test_storage_getUser_getToken(self):
            empty_storage = Storage(**get_opts())
            with self.assertRaises(UserNotExistsError):
                empty_storage.getUser(self.user1.username)

            with self.assertRaises(UserNotExistsError):
                empty_storage.getTokens(self.user1.username)

            empty_storage.addUser(self.user1)
            empty_storage.addService(self.service1)
            empty_storage.addTokenToUser(self.token1, self.user1)

            self.assertEqual(empty_storage.getUser(self.user1.username), self.user1)
            self.assertEqual(
                empty_storage.getTokens(self.user1.username), [self.token1]
            )

            self.assertEqual(
                empty_storage.getToken(self.user1.username, 0), self.token1
            )
            self.assertEqual(empty_storage.getTokens(self.user1), [self.token1])

            empty_storage.addUser(self.user2)
            empty_storage.addService(self.service2)
            empty_storage.addTokenToUser(self.token3, self.user2)

            self.assertEqual(empty_storage.getUser(self.user2.username), self.user2)

            self.assertEqual(empty_storage.getUser(self.user1.username), self.user1)

            self.assertEqual(
                empty_storage.getToken(self.user2.username, 0), self.token3
            )

            self.assertEqual(
                empty_storage.getToken(self.user1.username, self.token1.servicename),
                self.token1,
            )
            self.assertEqual(
                empty_storage.getToken(self.user2.username, self.token3.servicename),
                self.token3,
            )

            empty_storage.addTokenToUser(self.token4, self.user2)
            self.assertEqual(
                empty_storage.getToken(self.user2.username, self.token4.servicename),
                self.token4,
            )

        def test_tokenstorage_add_user(self):
            # raise an exception, if a user not exist for token
            with self.assertRaises(
                UserNotExistsError, msg=f"Storage {self.empty_storage}"
            ):
                self.empty_storage.addTokenToUser(self.token1, self.user1)

            # add one user, so in storage should be one
            expected = {"Max Mustermann": {"data": self.user1, "tokens": []}}

            self.empty_storage.addUser(self.user1)
            self.assertEqual(
                self.empty_storage._storage,
                expected,
                msg=f"Storage {self.empty_storage}",
            )

            # should raise an Exception, if user already there
            with self.assertRaises(
                UserExistsAlreadyError, msg=f"Storage {self.empty_storage}"
            ):
                self.empty_storage.addUser(self.user1)

            # add token to user
            expected[self.user1.username]["tokens"].append(self.token1)

            self.empty_storage.addTokenToUser(self.token1, self.user1)
            self.assertEqual(
                self.empty_storage._storage,
                expected,
                msg=f"Storage {self.empty_storage}",
            )

            # raise an exception, if token already there
            with self.assertRaises(
                UserHasTokenAlreadyError, msg=f"Storage {self.empty_storage}"
            ):
                self.empty_storage.addTokenToUser(self.token1, self.user1)

        def setUpRemove(self):
            # setUp
            self.empty_storage.addUser(self.user1)
            self.empty_storage.addUser(self.user2)

        def test_tokenstorage_remove_user(self):
            self.setUpRemove()

            expected = {}
            expected[self.user1.username] = {"data": self.user1, "tokens": []}
            expected[self.user2.username] = {"data": self.user2, "tokens": []}

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
            expected = {"Max Mustermann": {"data": self.user1, "tokens": [self.token1]}}

            self.empty_storage.addTokenToUser(self.token1, self.user1, Force=True)
            self.assertEqual(
                self.empty_storage._storage,
                expected,
                msg=f"Storage {self.empty_storage}",
            )

            # now overwrite the already existing token with force
            expected[self.user1.username]["tokens"][0] = self.token_like_token1

            self.empty_storage.addTokenToUser(
                self.token_like_token1, self.user1, Force=True
            )
            self.assertEqual(
                self.empty_storage._storage,
                expected,
                msg=f"Storage {self.empty_storage}",
            )

        def test_tokenstorage_oauthtokens_add_user(self):
            # empty storage
            self.assertEqual(self.empty_storage._storage, {})

            # raise an exception, if a user not exist for token
            with self.assertRaises(
                UserNotExistsError, msg=f"Storage {self.empty_storage}"
            ):
                self.empty_storage.addTokenToUser(self.oauthtoken1, self.user1)

            # add one user, so in storage should be one
            expected = {"Max Mustermann": {"data": self.user1, "tokens": []}}

            self.empty_storage.addUser(self.user1)
            self.assertEqual(
                self.empty_storage._storage,
                expected,
                msg=f"Storage {self.empty_storage}",
            )

            # should raise an Exception, if user already there
            with self.assertRaises(
                UserExistsAlreadyError, msg=f"Storage {self.empty_storage}"
            ):
                self.empty_storage.addUser(self.user1)

            # add token to user
            expected[self.user1.username]["tokens"].append(self.oauthtoken1)

            self.empty_storage.addTokenToUser(self.oauthtoken1, self.user1)
            self.assertEqual(
                self.empty_storage._storage,
                expected,
                msg=f"Storage {self.empty_storage}",
            )

            # raise an exception, if token already there
            with self.assertRaises(
                UserHasTokenAlreadyError, msg=f"Storage {self.empty_storage}"
            ):
                self.empty_storage.addTokenToUser(self.oauthtoken1, self.user1)

        def test_tokenstorage_oauthtokens_add_token_force(self):
            # add Token to not existing user with force
            expected = {
                "Max Mustermann": {"data": self.user1, "tokens": [self.oauthtoken1]}
            }

            self.empty_storage.addTokenToUser(self.oauthtoken1, self.user1, Force=True)
            self.assertEqual(
                self.empty_storage._storage,
                expected,
                msg=f"Storage {self.empty_storage}",
            )

            # now overwrite the already existing token with force
            expected[self.user1.username]["tokens"][0] = self.oauthtoken_like_token1

            self.empty_storage.addTokenToUser(
                self.oauthtoken_like_token1, self.user1, Force=True
            )
            self.assertEqual(
                self.empty_storage._storage,
                expected,
                msg=f"\nStorage: {self.empty_storage._storage}\n expected: {expected}",
            )

        def test_tokenstorage_tokens_under_user(self):
            oauthtoken1 = OAuth2Token(self.user1, self.oauthservice1, "ABC", "X_ABC")
            self.empty_storage.addTokenToUser(oauthtoken1, self.user1, Force=True)

            oauthtoken2 = OAuth2Token(self.user1, self.oauthservice2, "XYZ", "X_XYZ")
            self.empty_storage.addTokenToUser(oauthtoken2, self.user1, Force=True)

            token1 = Token(self.user1, self.service2, "ISADF")
            with self.assertRaises(ServiceNotExistsError):
                self.empty_storage.addTokenToUser(token1, self.user1, Force=True)

            self.empty_storage.addTokenToUser(self.token1, self.user1, Force=True)

        def test_tokenstorage_service_implementstype(self):
            empty_storage = Storage(**get_opts())
            service = LoginService(
                servicename="longname", implements=["fileStorage", "metadata"]
            )

            empty_storage.addUser(self.user1)
            token1 = Token(self.user1, service, "ISADF")
            #  test the exception raise
            with self.assertRaises(ServiceNotExistsError):
                empty_storage.addTokenToUser(token1, self.user1)

            # now should work
            self.assertTrue(empty_storage.addService(service))
            self.assertTrue(empty_storage.addTokenToUser(token1, self.user1))

            self.assertEqual(empty_storage.getTokens(self.user1), [token1])

            with self.assertRaises(ServiceExistsAlreadyError):
                empty_storage.addService(service)

        def test_tokenstorage_remove_token(self):
            expected = {
                self.user1.username: {"data": self.user1, "tokens": [self.oauthtoken1]}
            }

            self.empty_storage.addTokenToUser(self.oauthtoken1, self.user1, Force=True)
            self.assertEqual(
                self.empty_storage._storage,
                expected,
                msg=f"Storage {self.empty_storage}",
            )

            expected[self.user1.username]["tokens"].append(self.oauthtoken3)
            self.empty_storage.addTokenToUser(self.oauthtoken3, self.user1)

            self.assertEqual(
                self.empty_storage._storage,
                expected,
                msg=f"Storage {self.empty_storage}",
            )

            del expected[self.user1.username]["tokens"][1]

            self.empty_storage.removeToken(self.user1, self.oauthtoken3)
            self.assertEqual(self.empty_storage.storage, expected)

    return Test_TokenStorage


class StorageTestCase(make_test_case()):
    pass


class StorageRedisBackedTestCase(make_test_case(use_redis=True)):
    def test_deprov_data(self):
        expected = {
            self.user1.username: {"data": self.user1, "tokens": [self.oauthtoken1]}
        }

        self.empty_storage.addTokenToUser(self.oauthtoken1, self.user1, Force=True)
        self.assertEqual(
            self.empty_storage._storage,
            expected,
            msg=f"Storage {self.empty_storage}",
        )

        # this is obviously long time ago
        self.empty_storage._timestamps[self.user1.username] = 0

        self.empty_storage.deprovizionize()

        with self.assertRaises(UserNotExistsError):
            self.empty_storage.getTokens(self.user1)
        with self.assertRaises(KeyError):
            self.empty_storage._timestamps[self.user1.username]
