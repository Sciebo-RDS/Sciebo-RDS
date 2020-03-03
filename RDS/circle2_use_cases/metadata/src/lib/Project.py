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

    def getPorts(self):
        """
        This method returns all ports.
        """
        return self.getPortIn() + self.getPortOut()

    def getPortIn(self):
        """
        This method returns all ports, which functions as input in RDS.
        """
        return self.projectObj.get("portIn", [])

    def getPortOut(self):
        """
        This method returns all ports, which functions as output in RDS.
        """
        return self.projectObj.get("portOut", [])

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
        return self.projectObj.get("portIn", [])

    @property
    def portOut(self):
        return self.projectObj.get("portOut", [])

    @property
    def ports(self):
        return self.portIn + self.portOut

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
                f"http://{self.projectManager}/projects/{userId}/project/{projectIndex}")

            if req.status_code < 300:
                return req.json()

            logger.debug(req.content)
            return {}
        else:
            raise ValueError(
                "userId and projectIndex or projectId are needed parameters.")
