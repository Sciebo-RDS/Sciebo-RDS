from pickle import NONE
from typing_extensions import Self
import requests
import os
import logging
from RDS import (
    Util,
    FileTransferMode,
    FileTransferArchive,
    LoginService,
    OAuth2Service,
    LoginMode,
)

logger = logging.getLogger()


class Service:
    def __init__(
        self,
        servicename,
        userId,
        researchIndex,
        fileStorage=False,
        metadata=False,
        customProperties: list = None,
        testing=False,
    ):
        self.files = []

        self.servicename = servicename

        if not servicename.startswith("port-"):
            servicename = "port-" + servicename.lower()

        self.portaddress = f"http://layer1-{servicename}"

        self.testing = None
        if testing is not False:
            self.portaddress = testing
            self.testing = testing

        self.userId = userId
        self.researchIndex = researchIndex

        self.fileTransferMode = None
        self.fileTransferArchive = None
        self.loginMode = None

        self.port = servicename
        self.fileStorage = fileStorage
        self.metadata = metadata
        self.customProperties = customProperties

        logger.debug("got customProperties: {}".format(customProperties))

        self.useZipForFolder = False

        self.reload()

    @property
    def zipForFolder(self):
        return self.useZipForFolder

    def reload(self):
        if self.fileStorage:
            data = {"filepath": self.getFilepath(), "userId": self.userId}
            req = requests.get(
                f"{self.portaddress}/storage/folder",
                json=data,
                verify=(os.environ.get("VERIFY_SSL", "True") == "True"),
            )

            if req.status_code >= 300:
                # for convenience
                data.update(Util.parseToken(Util.loadToken(self.userId, self.port)))
                req = requests.get(
                    f"{self.portaddress}/storage/folder",
                    json=data,
                    verify=(os.environ.get("VERIFY_SSL", "True") == "True"),
                )

                if req.status_code >= 300:
                    return False

            json = req.json()

            logger.debug("reload fileStorage in Service got: {}".format(json))

            self.files = json.get("files")

        if self.metadata:
            # TODO: metadata ports can also response with files
            self.reloadInformations()

    def reloadInformations(self):
        """Updates all metadata informations from port."""

        json = requests.get(
            "{}/service/{}".format(
                os.getenv(
                    "USE_CASE_SERVICE_PORT_SERVICE",
                    "{}/port-service".format(self.portaddress),
                ),
                self.port,
            )
        ).json()

        logger.debug("reload metadata informations: got {}".format(json))

        svc = Util.getServiceObject(json["informations"])

        self.useZipForFolder = svc.fileTransferArchive == FileTransferArchive.zip
        self.fileTransferMode = svc.fileTransferMode
        self.fileTransferArchive = svc.fileTransferArchive

        if isinstance(svc, LoginService):
            self.loginMode = LoginMode.credentials
            self.credentials = svc.to_dict().get("credentials", {})
        elif isinstance(svc, OAuth2Service):
            self.loginMode = LoginMode.oauth
        else:
            self.loginMode = LoginMode.none

        logger.debug("got svc: {}, loginmode: {}".format(svc.to_dict(), self.loginMode))

    def createShareLink(self):
        if self.fileTransferMode != FileTransferMode.passiveWithLink:
            raise InvalidFiletransferMode

        data = {"filepath": self.getFilepath()}

        response_to = requests.post(
            f"{self.portaddress}/storage/folder",
            json=data,
            verify=(os.environ.get("VERIFY_SSL", "True") == "True"),
        )

        if response_to.status_code >= 300:
            data.update(Util.parseToken(Util.loadToken(self.userId, self.port)))
            logger.debug("request data {}".format(data))
            response_to = requests.post(
                f"{self.portaddress}/storage/folder",
                json=data,
                verify=(os.environ.get("VERIFY_SSL", "True") == "True"),
            )

        if response_to.status_code >= 300:
            raise CannotCreateSharelink

        cnt = response_to.json()
        return cnt["sharelink"]

    def getFilepath(self):
        filepath = self.getProperty("filepath")

        if str(filepath).endswith("/"):
            filepath = filepath[:-1]

        return filepath

    def getProjectId(self):
        return self.getProperty("projectId")

    def getFiles(self, getContent=False):
        """
        Returns a generator to iterate over.

        Returns the filepath string and the content of the file in the current used service.
        """
        for index, file in enumerate(self.files):
            if getContent:
                logger.debug(
                    "get file {} from service {}".format(file, self.servicename)
                )
                content = self.getFile(index)

                yield file, content
            else:
                yield file

    def getProperty(self, key):
        if self.customProperties is not None:
            for prop in self.customProperties:
                if prop["key"] == key:
                    return prop["value"]

        return None

    def getFile(self, file_id):
        from io import BytesIO

        file = self.files[file_id]

        if self.fileStorage:
            # this condition is for ports, which does not comply to the doc for urls
            path = "{}/{}".format(self.getFilepath(), file)
            if str(file).startswith(self.getFilepath()):
                path = file

            data = {
                "userId": self.userId,
                "filepath": path,
            }

            logger.debug("request data {}".format(data))

            response_to = requests.get(
                f"{self.portaddress}/storage/file",
                json=data,
                verify=(os.environ.get("VERIFY_SSL", "True") == "True"),
            )

            if response_to.status_code >= 300:
                data.update(Util.parseToken(Util.loadToken(self.userId, self.port)))

                logger.debug("request data {}".format(data))

                response_to = requests.get(
                    f"{self.portaddress}/storage/file",
                    json=data,
                    verify=(os.environ.get("VERIFY_SSL", "True") == "True"),
                )

            cnt = response_to.content
            logger.debug("got content size: {}".format(len(cnt)))

            return BytesIO(cnt)

        if self.metadata:
            # TODO: metadata can respond with files too.
            pass

        return BytesIO(b"")

    def triggerPassiveMode(self, importService: Self):
        """Trigger passive upload for given folder

        Args:
            importService (Service): The service which will be used to pull all needed informations.

        Returns:
            bool: Return True, if the trigger was successfully, otherwise False.
        """
        data = {
            "folder": importService.getFilepath(),
            "service": importService.servicename,
            "username": self.userId,
        }

        if importService.fileTransferMode == FileTransferMode.passiveWithLink:
            try:
                sharedlink = importService.createShareLink()
                data.update(
                    {"sharedlink": sharedlink, "filelist": importService.getFiles()}
                )
            except (InvalidFiletransferMode, CannotCreateSharelink) as e:
                logger.exception(f"Error while creating sharelink: {e}")
                return False

        data.update(Util.parseToken(Util.loadToken(self.userId, self.port)))

        logger.debug(
            "start passive mode with data {} in service {}".format(data, self.getJSON())
        )

        if self.metadata:
            response_to = requests.post(
                f"{self.portaddress}/metadata/project/{self.getProjectId()}/files",
                data=data,
                verify=(os.environ.get("VERIFY_SSL", "True") == "True"),
            )

            if response_to.status_code >= 300:
                logger.error(response_to.json())
                return False

        if self.fileStorage:
            # TODO maybe needed somedays
            pass

        return True

    def addFile(self, filename, fileContent):
        """Adds given file with filename to this service.

        Args:
            filename (str): Set the filename of this file.
            fileContent (io.BytesIO): Set the content of this file.

        Returns:
            bool: Return True, if the file was uploaded successfully, otherwise False.
        """
        data = Util.parseToken(Util.loadToken(self.userId, self.port))
        files = {"file": (filename, fileContent.getvalue())}
        data["filename"] = filename

        logger.debug(
            "add file {} with data {} in service {}".format(files, data, self.getJSON())
        )

        if self.metadata:
            response_to = requests.post(
                f"{self.portaddress}/metadata/project/{self.getProjectId()}/files",
                files=files,
                data=data,
                verify=(os.environ.get("VERIFY_SSL", "True") == "True"),
            )

            if response_to.status_code >= 300:
                logger.error(response_to.json())
                return False

        if self.fileStorage:
            # TODO: fileStorage can also add files
            return False

        return True

    def removeFile(self, file_id):
        found = False

        file = self.files[file_id]

        data = Util.parseToken(Util.loadToken(self.userId, self.port))

        if self.fileStorage:
            data["filepath"] = "{}/{}".format(self.getFilepath(), file)
            req = requests.delete(
                f"{self.portaddress}/storage/file",
                json=data,
                verify=(os.environ.get("VERIFY_SSL", "True") == "True"),
            )

            if req.status_code < 300:
                found = True

        if self.metadata:
            req = requests.delete(
                f"{self.portaddress}/metadata/project/{self.getProjectId()}/files/{file_id}",
                json=data,
                verify=(os.environ.get("VERIFY_SSL", "True") == "True"),
            )

            if req.status_code < 300:
                found = True

        if found:
            del self.files[file_id]
            return True

        return False

    def removeAllFiles(self):
        data = Util.parseToken(Util.loadToken(self.userId, self.port))

        logger.debug("remove files in service {}".format(self.servicename))

        found = False

        if self.fileStorage:
            # todo: implements me
            found = True

        if self.metadata:
            req = requests.delete(
                f"{self.portaddress}/metadata/project/{self.getProjectId()}/files",
                json=data,
                verify=(os.environ.get("VERIFY_SSL", "True") == "True"),
            )

            if req.status_code < 300:
                found = True

        if found:
            self.reload()

        return found

    def getJSON(self):
        import json

        return json.dumps(self.getDict())

    def getDict(self):

        obj = {"servicename": self.port, "files": [x for x in self.getFiles()]}

        return obj

    @classmethod
    def fromDict(cls, portDict, userId=None, researchIndex=None, testing=None):
        logger.debug("initialize service from dict, got dict: {}".format(portDict))

        portName = portDict["port"]
        fileStorage = False
        metadata = False
        customProperties = None

        for prop in portDict["properties"]:
            if prop["portType"] == "metadata":
                metadata = prop["value"]
            elif prop["portType"] == "fileStorage":
                fileStorage = prop["value"]
            elif prop["portType"] == "customProperties":
                customProperties = prop["value"]

        return cls(
            portName,
            userId=userId,
            researchIndex=researchIndex,
            fileStorage=fileStorage,
            metadata=metadata,
            customProperties=customProperties,
            testing=testing,
        )

    def __eq__(self, obj):
        if not isinstance(obj, Service):
            return False

        return self.getDict() == obj.getDict()


class InvalidFiletransferMode(Exception):
    pass


class CannotCreateSharelink(Exception):
    pass
