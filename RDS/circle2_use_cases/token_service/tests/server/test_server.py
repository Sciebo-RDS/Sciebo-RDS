
import unittest
import sys
import os
import json
import logging
from pactman import Consumer, Provider
from server import bootstrap

from lib.TokenService import TokenService
from lib.User import User
import Util
import jwt
import datetime
from lib.Service import OAuth2Service
from lib.Token import OAuth2Token

func = [Util.initialize_object_from_json, Util.initialize_object_from_dict]
load_object = Util.try_function_on_dict(func)

address = "http://localhost:3000"

logger = logging.getLogger()


def create_app():
    # set var for mock service
    os.environ["CENTRAL-SERVICE_TOKEN-STORAGE"] = address
    # creates a test client
    app = bootstrap(use_optimizer={"compress":False, "minify": False}, use_default_error=True, storage_address=address).app
    # propagate the exceptions to the test client
    app.config.update({"TESTING": True})

    return app


pact = Consumer('UseCaseTokenStorage').has_pact_with(
    Provider('CentralServiceTokenStorage'), port=3000)


class Test_TokenServiceServer(unittest.TestCase):

    def run(self, result=None):
        # this make pact as context in every test available.
        with pact as p:
            super(Test_TokenServiceServer, self).run(result)

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_redirect(self):
        code = "XYZABC"
        user = User("user")
        service = OAuth2Service("local", f"{Util.tokenService.address}/oauth/authorize",
                                f"{Util.tokenService.address}/oauth/token", "ABC", "XYZ")

        body = {
            "access_token": "1vtnuo1NkIsbndAjVnhl7y0wJha59JyaAiFIVQDvcBY2uvKmj5EPBEhss0pauzdQ",
            "token_type": "Bearer",
            "expires_in": 3600,
            "refresh_token": "7y0wJuvKmj5E1vjVnhlPBEhha59JyaAiFIVQDvcBY2ss0pauzdQtnuo1NkIsbndA",
            "user_id": user.username,
            "message_url": "https://www.example.org/owncloud/index.php/apps/oauth2/authorization-successful"
        }

        # test returned state jwt object
        pact.given(
            'An oauthservice was registered.'
        ).upon_receiving(
            'A request to get this oauthservice.'
        ).with_request(
            'GET', f"/service/{service.servicename}"
        ) .will_respond_with(200, body=service.to_json())

        response = self.client.get(f"/token-service/service/{service.servicename}")
        self.assertEqual(response.status_code, 200,
                         msg=response.get_data(as_text=True))

        # ignore signature
        resp_state = jwt.decode(response.json["jwt"], "secret", verify=False)
        logger.info(resp_state)

        self.assertEqual(resp_state["servicename"], service.servicename)
        self.assertEqual(resp_state["authorize_url"], service.authorize_url)

        date = resp_state["date"]

        # following request should not be needed a new pact, because its cached and date shuld be the same.
        response = self.client.get(f"/token-service/service/{service.servicename}")
        self.assertEqual(response.status_code, 200,
                         msg=response.get_data(as_text=True))

        # ignore signature
        resp_state = jwt.decode(response.json["jwt"], "secret", verify=False)
        logger.info(resp_state)

        self.assertEqual(resp_state["servicename"], service.servicename)
        self.assertEqual(resp_state["authorize_url"], service.authorize_url)
        self.assertEqual(resp_state["date"], date)

        key = Util.tokenService.secret

        data = {
            "servicename": service.servicename,
            "authorize_url": service.authorize_url,
            "date": str(datetime.datetime.now())
        }
        state = jwt.encode(data, key, algorithm="HS256")

        # need pact for service from Token Storage
        pact.given(
            'An oauthservice was registered.'
        ).upon_receiving(
            'A request to get this oauthservice.'
        ).with_request(
            'GET', f"/service/{service.servicename}"
        ) .will_respond_with(200, body=service.to_json())

        # need pact for exchange for code
        pact.given(
            'Client ID and secret was registered.'
        ).upon_receiving(
            'A request to exchange the given auth code to get access token and refresh token.'
        ).with_request(
            'POST', f"/oauth/token"
        ) .will_respond_with(200, body=body)

        expected = OAuth2Token(service.servicename, body["access_token"], body["refresh_token"], datetime.datetime.now(
        ) + datetime.timedelta(seconds=body["expires_in"]))

        # need pact for save the access and refresh token in Token Storage
        pact.given(
            'No token was registered for not registered user'
        ).upon_receiving(
            'A request to add an oauthtoken.'
        ).with_request(
            'POST', f"/user/{user.username}/token"
        ) .will_respond_with(201, body={"success": True})

        response = self.client.get(
            "/token-service/redirect", query_string={"code": code, "state": state})
        self.assertEqual(response.status_code, 302, msg=response.get_data())
        self.assertEqual(
            response.headers["location"], "http://localhost/token-service/authorization-success", msg=response.get_data())


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




if __name__ == '__main__':
    unittest.main()
