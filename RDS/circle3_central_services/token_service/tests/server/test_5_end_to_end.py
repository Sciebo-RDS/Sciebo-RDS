import unittest
import os
import json
import requests
import logging
from datetime import datetime, timedelta
from lib.User import User
from lib.Service import OAuth2Service
from lib.Token import Token, OAuth2Token
from lib.Storage import Storage
from Util import initialize_object_from_json
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys

logger = logging.getLogger()

@unittest.skipUnless(os.getenv("CI_DEFAULT_BRANCH") is not None, "This should not be executed locally because we use selenium and firefox webdriver.")
class test_end_to_end(unittest.TestCase):
    driver = None

    def setUp(self):
        server = "http://selenium:4444/wd/hub"
        self.driver = webdriver.Remote(command_executor=server,
                                       desired_capabilities=DesiredCapabilities.FIREFOX)
        self.driver.implicitly_wait(5)

    def tearDown(self):
        self.driver.quit()

    def test_owncloud(self):

        # prepare service
        storage = Storage()

        redirect = "http://sciebords-dev.uni-muenster.de/oauth2/redirect"
        owncloud = OAuth2Service(
            "owncloud-local",
            "http://10.14.28.90/owncloud/index.php/apps/oauth2/authorize?response_type=code&client_id={}&redirect_uri={}".format(
                os.getenv("OWNCLOUD_OAUTH_CLIENT_ID"),
                redirect
            ),
            "http://10.14.28.90/owncloud/index.php/apps/oauth2/api/v1/token",
            os.getenv("OWNCLOUD_OAUTH_CLIENT_ID"),
            os.getenv("OWNCLOUD_OAUTH_CLIENT_SECRET")
        )

        storage.addService(owncloud)

        # prepare user, which wants to make the whole oauth workflow
        user1 = User("user")

        token1 = Token(owncloud.servicename, "user")

        storage.addUser(user1)
        storage.addTokenToUser(token1, user1)

        def get_acces_token(user, token):
            nonlocal owncloud, storage

            self.driver.get(owncloud.authorize_url)

            if self.driver.current_url.startswith("http://10.14.28.90/owncloud/index.php/login"):
                # it redirects to login form
                field_username = self.driver.find_element_by_xpath(
                    "//*[@id=\"user\"]")
                field_password = self.driver.find_element_by_xpath(
                    "//*[@id=\"password\"]")
                field_username.clear()
                field_username.send_keys(user.username)

                field_password.clear()
                field_password.send_keys(token.access_token)
                field_password.send_keys(Keys.RETURN)

            btn = self.driver.find_element_by_xpath(
                "/html/body/div[1]/div/span/form/button"
            )
            btn.click()

            url = self.driver.current_url

            self.driver.delete_all_cookies()  # remove all cookies

            from urllib.parse import urlparse, parse_qs
            code = parse_qs(urlparse(url).query)["code"]

            data = {
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": redirect
            }

            req = requests.post(owncloud.refresh_url, data=data, auth=(
                owncloud.client_id, owncloud.client_secret)).json()
            oauthtoken = OAuth2Token(
                owncloud.servicename, req["access_token"], req["refresh_token"], datetime.now() + timedelta(seconds=req["expires_in"]))
            return oauthtoken

        oauthtoken1 = get_acces_token(user1, token1)
        storage.addTokenToUser(oauthtoken1, user1, Force=True)

        ######## test a refresh token #######
        # prepare user, which wants to get a refresh token

        oauthuser2 = User("user_refresh")

        # check if there is already a file, which has an oauth2token to reuse it.
        oauthtoken2 = None
        filepath = "https://zivgitlab.uni-muenster.de/{}/{}/-/jobs/artifacts/{}/raw/{}?job={}".format(
            os.getenv("CI_PROJECT_NAMESPACE"),
            os.getenv("CI_PROJECT_NAME"),
            os.getenv("CI_COMMIT_REF_NAME"),
            os.getenv("FOLDER"),
            os.getenv("CI_JOB_NAME"))
        try:
            req = requests.get(filepath).content
            oauthtoken2 = initialize_object_from_json(req)
            logger.info("Refresh token found in artifacts, use it now.")
        except:
            logger.warning("No refresh token from previous test run was found, so we collect a new one. \nFilepath: {}".format(filepath))
            # initialize like user1 with password
            token2 = Token(owncloud.servicename, "user_refresh")

            # generate an oauthtoken like before and overwrite oauthtoken1
            oauthtoken2 = get_acces_token(oauthuser2, token2)

        storage.addUser(oauthuser2)
        storage.addTokenToUser(oauthtoken2, oauthuser2)

        # try to refresh it now
        storage.refresh_service(owncloud)
        tokens = storage.getTokens(oauthuser2)
        checkToken = tokens[0]
        self.assertGreater(checkToken.expiration_date,
                           oauthtoken2.expiration_date)
        self.assertEqual(checkToken, oauthtoken2)

        # safe the current oauthtoken for reuse to test refresh token after a bigger period.
        with open("user_refresh.token", "w") as f:
            f.write(json.dumps(checkToken))

    # TODO implement me
    @unittest.skip("Currently not implemented")
    def test_zenodo(self):
        return
        if self.driver is None:
            return

        zenodo = OAuth2Service(
            "sandbox.zenodo.org",
            "https://sandbox.zenodo.org/oauth/authorize?scope=deposit%3Awrite+deposit%3Aactions&state=CHANGEME&redirect_uri=http%3A%2F%2Flocalhost%3A8080&response_type=code&client_id=feYfqBVCfNDJTQyQRXWiJ8eoga99GxKzXYAZXvbm",
            "https://sandbox.zenodo.org/oauth/token",
            os.getenv("ZENODO_OAUTH_CLIEND_ID"),
            os.getenv("ZENODO_OAUTH_CLIENT_SECRET")
        )
        self.driver.get(zenodo.authorize_url)
        btn = self.driver.find_element_by_xpath(
            "/html/body/div[2]/div[2]/div/div/div/div/div[2]/div[2]/form/button[1]")
        btn.click()
