import requests
import logging

logger = logging.getLogger()


class Project():
    """
    This class enables metadataservice to reuse requests and let it easier to use.
    *Currently* only for get requests.
    """

    def __init__(self, userId: str = None, projectIndex: int = None, projectId: int = None, testing: str = None):
        """
        This constructor loads all project relevant informations.

        The parameter testing enables the unittest to make requests to a mock server.
        """

        self.testing = testing
        self.projectManager = "circle3-project-manager"

        if self.testing is not None:
            self.projectManager = self.testing

        self.projectObj = self.reload(
            userId=userId, projectIndex=projectIndex, projectId=projectId)

    @property
    def projectId(self):
        return self.projectObj.get("projectId", None)

    @property
    def projectIndex(self):
        return self.projectObj.get("projectIndex", None)

    @property
    def userId(self):
        return self.projectObj.get("userId", None)

    @property
    def portIn(self):
        """
        This property returns all ports, which functions as input in RDS.
        """
        return self.projectObj.get("portIn", [])

    @property
    def portOut(self):
        """
        This property returns all ports, which functions as output in RDS.
        """
        return self.projectObj.get("portOut", [])

    def getPorts(self, metadata=True):
        """
        This method returns only the ports with metadata as type. No duplicates.
        You can set the parameter `metadata` to False to get all ports. Duplicates ports, which are set as input and output. 
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

    @property
    def ports(self):
        """
        This property returns only the ports with metadata as type. No duplicates.
        """
        return self.getPorts()

    def reload(self, userId: str = None, projectIndex: int = None, projectId: int = None):
        """
        This method catches the project information from the central service project manager.
        userId and projectIndex are only used together. You can provide projectId,
        so you do not need to enter userId and projectIndex for convenience.
        """
        if userId is None and projectIndex is None:
            if projectId is not None:
                req = requests.get(
                    f"http://{self.projectManager}/projects/id/{projectId}")

                if req.status_code == 200:
                    return req.json()

        if userId is not None and projectIndex is not None:
            req = requests.get(
                f"http://{self.projectManager}/projects/user/{userId}/project/{projectIndex}")

            if req.status_code < 300:
                return req.json()

            logger.debug(req.content)
            return {}
        else:
            raise ValueError(
                "userId and projectIndex or projectId are needed parameters.")
