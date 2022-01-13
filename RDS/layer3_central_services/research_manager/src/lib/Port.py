class Port():
    def __init__(self, portName, fileStorage=False, metadata=False, customProperties: list = None):
        """
        This initialize the a port with a name, which has to start with "port-", so the rds system can access the portname as domain to the corresponding microservice.

        fileStorage and metadata are booleans to enable this port as fileStorage or as metadata storage.

        With customProperties, you can save other informations about connections.
        """
        if not isinstance(portName, str):
            raise ValueError("Portname has to be string.")

        self.port = portName
        self.fileStorage = fileStorage
        self.metadata = metadata
        self.customProperties = customProperties

    @property
    def portname(self):
        return self.port

    def setProperty(self, portType, value):
        """
        Returns True, if portType was found and set to value. Otherwise false.

        portType has to be a string, value can be anything.
        """
        if not isinstance(portType, str):
            raise ValueError("parameter \"portType\" is not of type string.")

        if not isinstance(value, bool):
            if portType != "customProperties":
                raise ValueError("parameter \"value\" is not of type boolean.")

        if portType == "fileStorage":
            self.fileStorage = value
        elif portType == "metadata":
            self.metadata = value
        elif portType == "customProperties":
            self.customProperties = value
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

        if self.customProperties is not None:
            obj["properties"].append({
                "portType": "customProperties",
                "value": self.customProperties
            })

        return obj

    @classmethod
    def fromDict(cls, portDict):
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

        return cls(portName, fileStorage=fileStorage, metadata=metadata, customProperties=customProperties)

    def __eq__(self, obj):
        if not isinstance(obj, Port):
            return False

        return (self.getDict() == obj.getDict())
