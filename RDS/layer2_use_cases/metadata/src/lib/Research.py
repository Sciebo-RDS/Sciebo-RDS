import requests
import logging, os

logger = logging.getLogger()


class Research:
    """
    This class enables metadataservice to reuse requests and let it easier to use.
    *Currently* only for get requests.
    """

    def __init__(
        self,
        userId: str = None,
        researchIndex: int = None,
        researchId: int = None,
        testing: str = None,
    ):
        """
        This constructor loads all research relevant informations.

        The parameter testing enables the unittest to make requests to a mock server.
        """

        self.researchManager = "layer3-research-manager"

        if testing is not None and testing is not False:
            self.researchManager = testing

        self.researchObj = self.reload(
            userId=userId, researchIndex=researchIndex, researchId=researchId
        )

    @property
    def researchId(self):
        return self.researchObj.get("researchId", None)

    @property
    def researchIndex(self):
        return self.researchObj.get("researchIndex", None)

    @property
    def userId(self):
        return self.researchObj.get("userId", None)

    @property
    def portIn(self):
        """
        This property returns all ports, which functions as input in RDS.
        """
        return self.researchObj.get("portIn", [])

    @property
    def portOut(self):
        """
        This property returns all ports, which functions as output in RDS.
        """
        return self.researchObj.get("portOut", [])

    def getPorts(self, metadata=True):
        """
        This method returns only the ports with metadata as type. No duplicates.
        Set parameter `metadata` to False to get all ports. Duplicates ports, which are set as input and output. 
        """
        if metadata:
            ports = []
            for port in self.portIn + self.portOut:
                for prop in port["properties"]:
                    if prop["portType"] == "metadata" and port not in ports:
                        ports.append(port)
                        break
            return ports

        return self.portIn + self.portOut

    def getPortsWithProjectId(self, metadata=True):
        """
        This method returns a list of tuple with (port, projectId) with metadata as type. No duplicates.
        Set parameter `metadata` to False to get all ports. Duplicates ports, which are set as input and output.
        If no projectId was found, it is None.

        This method is useful, if you want to redirect a call to all ports which are configured for a research project in RDS.
        """
        ports = self.getPorts(metadata=metadata)
        result = []

        for port in ports:
            projectId = None
            for prop in port["properties"]:
                if prop.get("portType", "") == "customProperties":
                    for customVal in prop["value"]:
                        try:
                            if customVal["key"] == "projectId":
                                projectId = customVal["value"]
                                break
                        except:
                            pass
            result.append((port, projectId))

        return result

    @property
    def ports(self):
        """
        This property returns only the ports with metadata as type. No duplicates.
        """
        return self.getPorts()

    def reload(
        self, userId: str = None, researchIndex: int = None, researchId: int = None
    ):
        """
        This method catches the research information from the central service research manager.
        userId and researchIndex are only used together. You can provide researchId,
        so you do not need to enter userId and researchIndex for convenience.
        """

        if researchId is not None:
            req = requests.get(
                f"http://{self.researchManager}/research/id/{researchId}",
                verify=(os.environ.get("VERIFY_SSL", "True") == "True"),
            )

            if req.status_code == 200:
                return req.json()

        if userId is not None and researchIndex is not None:
            req = requests.get(
                f"http://{self.researchManager}/research/user/{userId}/research/{researchIndex}",
                verify=(os.environ.get("VERIFY_SSL", "True") == "True"),
            )

            if req.status_code < 300:
                return req.json()

            logger.debug(req.content)
            return {}

        raise ValueError(
            "userId and researchIndex or researchId are needed parameters."
        )
