class Port():
    def __init__(self, portName, fileStorage=False, metadata=False):
        if not isinstance(portName, str):
            raise ValueError("Portname has to be string.")

        if not str(portName).startswith("port-"):
            raise ValueError(
                "portName has to starts with \"port-\" to use it as a domain.")

        self.port = portName
        self.fileStorage = fileStorage
        self.metadata = metadata

    def setProperty(self, portType, value):
        """
        Returns True, if portType was found and set to value. Otherwise false.

        portType has to be a string, value has to be boolean.
        """
        if not isinstance(portType, str):
            raise ValueError("parameter \"portType\" is not of type string.")

        if not isinstance(value, bool):
            raise ValueError("parameter \"value\" is not of type boolean.")

        if portType is "fileStorage":
            self.fileStorage = value
        elif portType is "metadata":
            self.metadata = value
        else:
            # if nothing was found, return false
            return False
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

        return obj

    @classmethod
    def fromDict(cls, portDict):
        portName = portDict["port"]
        fileStorage = False
        metadata = False

        for prop in portDict["properties"]:
            if prop["portType"] == "metadata":
                metadata = prop["value"]
            elif prop["portType"] == "fileStorage":
                fileStorage = prop["value"]

        return cls(portName, fileStorage=fileStorage, metadata=metadata)

    def __eq__(self, obj):
        if not isinstance(obj, Port):
            return False

        return (self.getDict() == obj.getDict())
