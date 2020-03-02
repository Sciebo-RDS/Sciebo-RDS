import requests


class Metadata():
    def __init__(self, testing=None):
        self.project_manager = "circle3-project-manager"
        if testing is not None:
            self.project_manager = testing

    def getProjectId(self, userId, projectIndex):
        """
        This method returns the corresponding projectId to the given userId and projectIndex.
        """
        return self.getProject(userId=userId, projectIndex=projectIndex).get("projectId", -1)

    def getProject(self, userId: str = None, projectIndex: int = None, projectId: int = None):
        """
        This method catches the project information from the central service project manager.
        userId and projectIndex are only used together. You can provide projectId,
        so you do not need to enter userId and projectIndex for convenience.
        """
        if userId is None and projectIndex is None:
            if projectId is not None:
                req = requests.get(
                    f"{self.project_manager}/projects/id/{projectIndex}")
                if req.status_code == 200:
                    data = req.json()
                    userId = data["userId"]
                    projectIndex = data["projectIndex"]
            else:
                raise ValueError(
                    "userId and projectIndex or projectId are needed parameters.")

        req = requests.get(
            f"{self.project_manager}/projects/{userId}/project/{projectIndex}")

        if req.status_code == 200:
            return req.json()

        return {}

    def getPortIn(self, userId, projectIndex):
        """
        This method returns all ports, which functions as input in RDS.
        """
        return self.getProject(userId=userId, projectIndex=projectIndex).get("portIn", [])

    def getPortOut(self, userId, projectIndex):
        """
        This method returns all ports, which functions as output in RDS.
        """
        return self.getProject(userId=userId, projectIndex=projectIndex).get("portOut", [])

    def getMetadataForProject(self, projectId: int):
        """
        This method returns the metadata from all available ports for specified projectId.
        """
        allMetadata = []

        # get all ports registered to projectId
        ports = []

        # TODO: parallize me
        for port in ports:
            metadata = self.getMetadataForProjectFromPort(port, projectId)
            d = {
                "port": port,
                "metadata": metadata
            }
            allMetadata.append(d)

        return allMetadata

    def getMetadataForProjectFromPort(self, port: str, projectId: int):
        """
        This method returns the metadata from given port for specified projectId.
        """
        # pull all metadata from given port for projectId
        return {}

    def updateMetadataForProject(self, projectId: int, updateMetadata: dict):
        """
        This method changes the metadata in all available ports to the given metadata values in given dict for specified projectId.
        """
        # get all ports registered to projectId
        allMetadata = []

        # get all ports registered to projectId
        ports = []

        # TODO: parallize me
        for port in ports:
            metadata = self.updateMetadataForProjectFromPort(
                port, projectId, updateMetadata)
            d = {
                "port": port,
                "metadata": metadata
            }
            allMetadata.append(d)

        return allMetadata

    def updateMetadataForProjectFromPort(self, port: str, projectId: int, updateMetadata: dict):
        """
        This method changes the metadata in given port to the given metadata values in given dict for specified projectId.
        """

        # TODO: updates all metadata in givne dict for received ports for projectId
        return {}
