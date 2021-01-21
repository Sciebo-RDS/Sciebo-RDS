import unittest
import sys
import os
import json
import logging
from pactman import Consumer, Provider
from src import bootstrap

from lib.TokenService import TokenService

import Util
import jwt
import datetime
from RDS import User, OAuth2Service, BaseService, OAuth2Token, Token

func = [Util.initialize_object_from_json, Util.initialize_object_from_dict]
load_object = Util.try_function_on_dict(func)

address = "http://localhost:3000"

logger = logging.getLogger()


def create_app():
    # creates a test client
    app = bootstrap(
        use_optimizer={"compress": False, "minify": False},
        use_default_error=True,
        testing=address,
    ).app
    # propagate the exceptions to the test client
    app.config.update({"TESTING": True})

    return app


pact = Consumer("UseCaseTokenStorage").has_pact_with(
    Provider("CentralServiceTokenStorage"), port=3000
)


class Test_TokenServiceServer(unittest.TestCase):
    def run(self, result=None):
        # this make pact as context in every test available.
        with pact as p:
            super(Test_TokenServiceServer, self).run(result)

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    @staticmethod
    def zipStatusGET(pact, service: str, status: bool):
        pact.given(
            f"set zipStatus for service {service}, if it needs zip for folder in folder"
        ).upon_receiving("service responds with zipStatus").with_request(
            "GET", f"/metadata/informations"
        ).will_respond_with(
            200, body={
                "fileTransferArchive": "zip",
                "fileTransferMode": 0,
                "loginMode": 1
            }
        )

    def test_redirect(self):
        code = "XYZABC"
        user = User("user")
        service = OAuth2Service(
            "local",
            implements=["metadata"],
            authorize_url=f"{Util.tokenService.address}/oauth/authorize",
            refresh_url=f"{Util.tokenService.address}/oauth/token",
            client_id="ABC",
            client_secret="XYZ",
        )

        body = {
            "access_token": "1vtnuo1NkIsbndAjVnhl7y0wJha59JyaAiFIVQDvcBY2uvKmj5EPBEhss0pauzdQ",
            "token_type": "Bearer",
            "expires_in": 3600,
            "refresh_token": "7y0wJuvKmj5E1vjVnhlPBEhha59JyaAiFIVQDvcBY2ss0pauzdQtnuo1NkIsbndA",
            "user_id": user.username,
            "message_url": "https://www.example.org/owncloud/index.php/apps/oauth2/authorization-successful",
        }

        # test returned state jwt object
        pact.given("An oauthservice was registered.").upon_receiving(
            "A request to get this oauthservice."
        ).with_request("GET", f"/service/{service.servicename}").will_respond_with(
            200, body=service.to_json()
        )

        pact.given(
            f"set zipStatus for service {service}, if it needs zip for folder in folder"
        ).upon_receiving("service responds with zipStatus").with_request(
            "GET", "/metadata/informations"
        ).will_respond_with(
            200, body={
                "fileTransferArchive": "zip",
                "fileTransferMode": 0,
                "loginMode": 1
            }
        )

        with pact:
            response = self.client.get(
                f"/port-service/service/{service.servicename}")
        self.assertEqual(response.status_code, 200,
                         msg=response.get_data(as_text=True))

        # ignore signature
        resp_state = jwt.decode(response.json["jwt"], "secret", algorithms="HS256", options={
                                "verify_signature": False})
        logger.info(resp_state)

        self.assertEqual(resp_state["servicename"], service.servicename)
        self.assertEqual(resp_state["authorize_url"], service.authorize_url)

        date = resp_state["date"]

        # following request should not be needed a new pact, because its cached and date shuld be the same.
        response = self.client.get(
            f"/port-service/service/{service.servicename}")
        self.assertEqual(response.status_code, 200,
                         msg=response.get_data(as_text=True))

        # ignore signature
        resp_state = jwt.decode(response.json["jwt"], "secret", algorithms="HS256", options={
                                "verify_signature": False})
        logger.info(resp_state)

        self.assertEqual(resp_state["servicename"], service.servicename)
        self.assertEqual(resp_state["authorize_url"], service.authorize_url)

        key = Util.tokenService.secret

        data = {
            "servicename": service.servicename,
            "authorize_url": service.authorize_url,
            "date": str(datetime.datetime.now()),
        }
        import base64
        import json

        stateReal = jwt.encode(data, key, algorithm="HS256")
        state = base64.b64encode(
            json.dumps(
                {"jwt": stateReal, "user": user.username}
            ).encode("utf-8")
        )

        pluginDict = {
            "servicename": service.servicename,
            "state": stateReal,
            "userId": user.username,
            "code": code,
        }
        jwtEncode = jwt.encode(
            pluginDict, service.client_secret, algorithm="HS256")

        # need pact for exchange for code
        pact.given("Client ID and secret was registered.").upon_receiving(
            "A request to exchange the given auth code to get access token and refresh token."
        ).with_request("POST", f"/oauth/token").will_respond_with(200, body=body)

        # currently not needed
        # expected = OAuth2Token(user, service, body["access_token"], body["refresh_token"], datetime.datetime.now(
        # ) + datetime.timedelta(seconds=body["expires_in"]))

        # need pact for save the access and refresh token in Token Storage
        pact.given("No token was registered for not registered user").upon_receiving(
            "A request to add an oauthtoken."
        ).with_request("POST", f"/user/{user.username}/token").will_respond_with(
            201, body={"success": True}
        )

        with pact:
            response = self.client.post(
                "/port-service/exchange", json={"jwt": jwtEncode}
            )

        self.assertEqual(response.status_code, 204, msg=response.get_data())

        # TODO: add tests here for redirects to cancel page
        # test for no service found
        # test for invalid code
        # test for token, which not saved in token storage

    @unittest.skip
    def test_user(self):
        # TODO test /user
        pass

    @unittest.skip
    def test_user_service(self):
        # TODO test /user/{user-id}/service
        pass

    @unittest.skip
    def test_service_all(self):
        # TODO test /service (do not test /service/{servicename}, because its tested in redirect)
        pass

    @unittest.skip
    def test_serviceprojects_index(self):
        # TODO test /user/{user-id}/service/{servicename}/projects
        pass

    @unittest.skip
    def test_serviceprojects_get(self):
        # TODO test /user/{user-id}/service/{servicename}/projects/{projects-id}

        self.assertFalse(True)

    def test_serviceprojects_add(self):
        proj1 = {"projectId": 0, "metadata": {}}
        proj2 = {"projectId": 1, "metadata": {}}

        userId = "admin"
        servicename = "zenodo"

        expected_project = proj1

        pact.given("one searched token was registered.").upon_receiving(
            "a request to get a specific token for service from user."
        ).with_request("GET", f"/user/{userId}/token/{servicename}").will_respond_with(
            200, body=json.dumps(Token(User(userId), BaseService(servicename, implements=["metadata"]), "ABC"))
        )

        pact.given("service with project support").upon_receiving(
            "try to create a project"
        ).with_request("POST", f"/metadata/project").will_respond_with(
            200, body=expected_project
        )

        with pact:
            code = self.client.post(
                "/port-service/user/{}/service/{}/projects".format(
                    userId, servicename)
            ).status_code

        self.assertEqual(code, 204)

        pact.given("one searched token was registered.").upon_receiving(
            "a request to get a specific token for service from user."
        ).with_request("GET", f"/user/{userId}/token/{servicename}").will_respond_with(
            200, body=json.dumps(Token(User(userId), BaseService(servicename, implements=["metadata"]), "ABC"))
        )

        pact.given("Given token to access port").upon_receiving(
            "invalid request"
        ).with_request("POST", "/metadata/project").will_respond_with(500, body="")

        with pact:
            code = self.client.post(
                "/port-service/user/{}/service/{}/projects".format(
                    userId, servicename)
            ).status_code

        self.assertEqual(code, 500)

    def test_serviceprojects_delete(self):
        proj1 = {"projectId": 0, "metadata": {}}

        userId = "admin"
        servicename = "zenodo"

        pact.given("one searched token was registered.").upon_receiving(
            "a request to get a specific token for service from user."
        ).with_request("GET", f"/user/{userId}/token/{servicename}").will_respond_with(
            200, body=json.dumps(Token(User(userId), BaseService(servicename, implements=["metadata"]), "ABC"))
        )

        pact.given("Given token to access port").upon_receiving(
            "try to delete {}".format(proj1["projectId"])
        ).with_request(
            "DELETE", "/metadata/project/{}".format(proj1["projectId"])
        ).will_respond_with(
            404, body=""
        )

        with pact:
            code = self.client.delete(
                "/port-service/user/{}/service/{}/projects/{}".format(
                    userId, servicename, proj1["projectId"]
                )
            ).status_code

        self.assertGreaterEqual(code, 404)

        pact.given("one searched token was registered.").upon_receiving(
            "a request to get a specific token for service from user."
        ).with_request("GET", f"/user/{userId}/token/{servicename}").will_respond_with(
            200, body=json.dumps(Token(User(userId), BaseService(servicename, implements=["metadata"]), "ABC"))
        )

        pact.given("Given token to access port").upon_receiving(
            "a call to delete {}".format(proj1["projectId"])
        ).with_request(
            "DELETE", "/metadata/project/{}".format(proj1["projectId"])
        ).will_respond_with(
            204, body=""
        )

        with pact:
            code = self.client.delete(
                "/port-service/user/{}/service/{}/projects/{}".format(
                    userId, servicename, proj1["projectId"]
                )
            ).status_code

        self.assertEqual(code, 204)


if __name__ == "__main__":
    unittest.main()
