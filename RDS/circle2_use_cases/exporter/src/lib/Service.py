from lib.File import File
import requests
import os
import logging

logger = logging.getLogger()


class Service():
    def __init__(self, servicename, userId, researchIndex, fileStorage=False, metadata=False, customProperties: list = None):
        self.files = []

        self.portaddress = "circle1-port-" + servicename.lower()

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
                f"{self.portaddress}/folder", json=data).json()
            self.files = json.get("files", [])

        # TODO: metadata ports can also be response with files

    def getFilepath(self):
        filepath = ""

        for prop in self.customProperties:
            if prop["key"] == "filepath":
                return prop["filepath"]

        return filepath

    def getFiles(self):
        """
        Returns a generator to iterate over.

        Returns the file object and the content of the file in the current used service.
        """
        for index, file in enumerate(self.files):
            yield file, self.getFile(index)

    def getFile(self, file_id):
        def getContent(file):
            pass

        return getContent(self.files[file_id])

    def addFile(self, filepath, fileContent):
        file = {
            "file": (os.path.basename(filepath), fileContent, "multipart/form-data")
        }

        response_to = requests.post(
            f"{self.portaddress}/{file}", files=file, data={"userId": self.userId})

        if response_to.status_code >= 300:
            logger.error(response_to.json())
            return False

        return True

    def removeFile(self, file_id):
        def removeFile(file):
            for file in self.files:
                req = requests.delete(
                    f"{self.portaddress}/{file}")
                if req.status_code != 200:
                    return False

        b = removeFile(self.files[file_id])

        if b:
            del self.files[file_id]

        return b

    def removeAllFiles(self):
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
            "port": self.port,
            "properties": []
        }

        if self.fileStorage:
            obj["properties"].append({
                "portType": "fileStorage",
                "value": self.fileStorage
            })

        if self.metadata:
            obj["properties"].append({
                "portType": "metadata",
                "value": self.metadata
            })

        if self.customProperties is not None:
            obj["properties"].append({
                "portType": "customProperties",
                "value": self.customProperties
            })

        return obj

    @classmethod
    def fromDict(cls, portDict, userId=None, researchIndex=None):
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

        return cls(portName, userId=userId, researchIndex=researchIndex, fileStorage=fileStorage, metadata=metadata, customProperties=customProperties)

    def __eq__(self, obj):
        if not isinstance(obj, Service):
            return False

        return (self.getDict() == obj.getDict())
