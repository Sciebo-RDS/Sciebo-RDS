import requests
import os
import logging

logger = logging.getLogger()


class Service():
    def __init__(self, servicename, userId, researchIndex, fileStorage=False, metadata=False, customProperties: list = None, testing=False):
        self.files = []

        self.servicename = servicename

        if not servicename.startswith("port-"):
            servicename = "port-" + servicename.lower()

        self.portaddress = f"http://circle1-{servicename.lower()}"

        if testing is not False:
            self.portaddress = testing

        self.userId = userId
        self.researchIndex = researchIndex

        self.fileStorage = False
        self.metadata = False

        self.port = servicename
        self.fileStorage = fileStorage
        self.metadata = metadata
        self.customProperties = customProperties

        self.reload()

    def reload(self):
        if self.fileStorage:
            data = {
                "filepath": self.getFilepath(),
                "userId": self.userId
            }
            json = requests.get(
                f"{self.portaddress}/storage/folder", json=data).json()

            self.files = json.get("files")

        if self.metadata:
            # TODO: metadata ports can also response with files
            pass

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
                    "get file {} from service {}".format(file, self.servicename))
                content = self.getFile(index)

                logger.debug("got content: {}".format(
                    content.getvalue().decode()))

                yield file, content
            else:
                yield file

    def getProperty(self, key):
        for prop in self.customProperties:
            if prop["key"] == key:
                return prop["value"]

        return None

    def getFile(self, file_id):
        from io import BytesIO

        file = self.files[file_id]

        if self.fileStorage:
            data = {
                "userId": self.userId,
                "filepath": "{}/{}".format(self.getFilepath(), file)
            }

            logger.debug("request data {}".format(data))

            response_to = requests.get(
                f"{self.portaddress}/storage/file", json=data)

            cnt = response_to.content
            logger.debug("got bytes {}".format(cnt))

            return BytesIO(cnt)

        if self.metadata:
            # TODO: metadata can respond with files too.
            pass

        return BytesIO(b'')

    def addFile(self, filename, fileContent):
        files = {
            "file": (filename, fileContent.getvalue())
        }
        data = {
            "userId": self.userId,
            "filename": filename
        }

        logger.debug("add file {} with data {} in service {}".format(
            files, data, self.getJSON()))

        if self.metadata:
            response_to = requests.post(
                f"{self.portaddress}/metadata/project/{self.getProjectId()}/files", files=files, data=data)

            if response_to.status_code >= 300:
                logger.error(response_to.json())
                return False

        if self.fileStorage:
            # TODO: fileStorage can also add files
            pass

        return True

    def removeFile(self, file_id):
        found = False

        file = self.files[file_id]

        data = {
            "filepath": "{}/{}".format(self.getFilepath(), file),
            "userId": self.userId
        }
        if self.fileStorage:
            req = requests.delete(
                f"{self.portaddress}/storage/file", json=data)

            if req.status_code < 300:
                found = True

        if self.metadata:
            req = requests.delete(
                f"{self.portaddress}/metadata/project/{self.getProjectId()}/files/{file_id}", json=data)

            if req.status_code < 300:
                found = True

        if found:
            del self.files[file_id]
            return True

        return False

    def removeAllFiles(self):
        logger.debug("remove files in service {}".format(self.servicename))
        for index, _ in enumerate(self.files):
            if not self.removeFile(index):
                return False

        self.reload()
        return True

    def getJSON(self):
        import json
        return json.dumps(self.getDict())

    def getDict(self):

        obj = {
            "servicename": self.servicename,
            "files": [x for x in self.getFiles()]
        }

        return obj

    @classmethod
    def fromDict(cls, portDict, userId=None, researchIndex=None, testing=None):
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

        return cls(portName, userId=userId, researchIndex=researchIndex, fileStorage=fileStorage, metadata=metadata, customProperties=customProperties, testing=testing)

    def __eq__(self, obj):
        if not isinstance(obj, Service):
            return False

        return (self.getDict() == obj.getDict())
