import os
import requests
import logging
from webdav3.client import Client

logger = logging.getLogger()


def loadAccessToken(userId: str, service: str):
    tokenStorageURL = os.getenv(
        "USE_CASE_SERVICE_PORT_SERVICE", "http://localhost:3000"
    )
    # load access token from token-storage
    result = requests.get(f"{tokenStorageURL}/user/{userId}/service/{service}")

    if result.status_code > 200:
        return None

    access_token = result.json()
    logger.debug(f"got: {access_token}")

    if "type" in access_token and access_token["type"].endswith("Token"):
        access_token = access_token["data"]["access_token"]

    logger.debug(
        "userId: {}, token: {}, service: {}".format(userId, access_token, service)
    )

    return access_token


class OwncloudUser:
    """
    This represents an owncloud user. It initialize only one connection to owncloud for one user and holds the current access token.
    """

    _access_token = None
    _user_id = None

    def __init__(self, userId, apiKey=None):
        self._user_id = userId
        self._access_token = (
            apiKey if apiKey is not None else loadAccessToken(userId, "Owncloud")
        )

        options = {
            "webdav_hostname": "{}/remote.php/webdav".format(
                os.getenv("OWNCLOUD_INSTALLATION_URL", "http://localhost:3000")
            ),
            "webdav_token": self._access_token,
        }
        self.client = Client(options)

    def getFolder(self, foldername):
        """Returns the files within the foldername. If a folder is in there, it returns all files within recursive.

        Args:
            foldername (str): Represents the searched foldername

        Returns:
            list: Represents all files as strings in a list.
        """
        logger.debug("foldername {}".format(foldername))

        from urllib.parse import quote, unquote

        if unquote(foldername) is not foldername:
            foldername = unquote(foldername)
        files = self.client.list(foldername)

        logger.debug("found files: {}".format(files))

        # remove the first element, because this is the searched folder.
        del files[0]

        indexList = []
        #TODO: needs tests.
        for index, file in enumerate(files):
            if file.endsWith("/"):
                # save index for later removal, because we do not want the folderpaths
                indexList.append(index)
                fullname = file
                logger.debug(f"recursive getFolder for inner folders: {fullname}")
                tmpFiles = self.getFolder(fullname)

                for appendFile in tmpFiles:
                    # add full filepath in context of folder
                    files.append(fullname + appendFile)

        for index in indexList:
            del files[index]

        return files

    def getFile(self, filename):
        """
        Returns bytesIO content from specified owncloud filepath. The path does not start with /.
        """

        logger.debug("filename {}".format(filename))

        from urllib.parse import quote, unquote

        # check if string is already urlencoded
        # if unquote is equal to string, then it is not urlencoded (unquote respects plus sign)
        if unquote(filename) != filename:
            filename = unquote(filename)

        from io import BytesIO

        buffer = BytesIO(b"")

        res1 = self.client.resource(filename)
        res1.write_to(buffer)
        buffer.seek(0)

        logger.debug("file content: {}".format(buffer.getvalue()))

        return buffer
