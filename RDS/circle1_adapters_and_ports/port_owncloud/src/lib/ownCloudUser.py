import os
import requests
import logging

logger = logging.getLogger()


def loadAccessToken(userId: str, service: str):
    tokenStorageURL = os.getenv(
        "USE_CASE_SERVICE_TOKEN_SERVICE", "http://localhost:3000")
    # load access token from token-storage
    result = requests.get(
        f"{tokenStorageURL}/user/{userId}/service/{service}")

    if result.status_code > 200:
        return None

    access_token = result.json()
    logger.debug(f"got: {access_token}")

    if "type" in access_token and access_token["type"].endswith("Token"):
        access_token = access_token["data"]["access_token"]

    logger.debug("userId: {}, token: {}, service: {}".format(
        userId, access_token, service))

    return access_token


class OwncloudUser():
    """
    This represents an owncloud user. It initialize only one connection to owncloud for one user and holds the current access token.
    """

    _access_token = None
    _user_id = None

    def __init__(self, userId, apiKey=None):
        self._user_id = userId
        self._access_token = apiKey if apiKey is not None else loadAccessToken(
            userId, "Owncloud")

    def getFile(self, filename):
        """
        Returns the given filename from specified owncloud. The path does not start with /.
        """

        logger.debug("filename {}".format(filename))

        from urllib.parse import quote, unquote

        # check if string is already urlencoded
        # if unquote is equal to string, then it is not urlencoded (unquote respects plus sign)
        if unquote(filename) is filename:
            filename = quote(filename)

        # TODO chunk download https://stackoverflow.com/questions/34503412/download-and-save-pdf-file-with-python-requests-module/34503421
        headers = {
            "Authorization": f"Bearer {self._access_token}"
        }
        url = "{}/remote.php/webdav/{}".format(os.getenv("OWNCLOUD_INSTALLATION_URL",
                                                         "http://localhost:3000"), filename)
        file = requests.get(url, headers=headers)

        # FIXME: if its utf-8, then we should return text
        # if file.encoding is "UTF-8":
        #    return file.text

        logger.debug("File is None? {}".format(file is None))
        from io import BytesIO

        return BytesIO(file.content)
