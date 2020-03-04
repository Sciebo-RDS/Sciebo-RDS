import requests
import logging
from src.lib.Project import Project

logger = logging.getLogger()


class Metadata():
    def __init__(self, testing: str = None):
        """
        This is the constructor. No needed parameters.

        Testing has to be valid url string without protocol schema (e.g. http),
        so this class use the given address for all requests.
        """
        self.testing = None

        if testing is not None:
            self.testing = testing

    def getProjectId(self, userId, projectIndex):
        """
        This method returns the corresponding projectId to the given userId and projectIndex.
        """
        return Project(testing=self.testing, userId=userId, projectIndex=projectIndex).projectId

    def getPortString(self, port: str):
        res = f"circle1-{port}"

        if self.testing:
            res = self.testing

        return res

    def getMetadataForProject(self, userId: str = None, projectIndex: int = None, projectId: int = None):
        """
        This method returns the metadata from all available ports for specified projectId.
        """
        allMetadata = []

        logger.debug("start get metadata method for project")

        ports = Project(testing=self.testing,
                        userId=userId, projectIndex=projectIndex, projectId=projectId).ports

        logger.debug(f"got ports {ports}")

        # FIXME: parallize me
        for port in ports:
            logger.debug(f"work on port {port}")
            port = port["port"]
            metadata = self.getMetadataForProjectFromPort(port, projectId)
            d = {
                port: metadata
            }
            allMetadata.append(d)

        return allMetadata

    def getMetadataForProjectFromPort(self, port: str, projectId: int):
        """
        This method returns the metadata from given port for specified projectId.
        Returns a dict, which was described in the metadata api endpoint "/metadata/project/{project-id}" or an empty one.
        """
        # pull all metadata from given port for projectId

        req = requests.get(
            f"http://{self.getPortString(port)}/metadata/project/{projectId}")

        if req.status_code == 200:
            return req.json()

        logger.exception(Exception(f"Metadata model req: {req.content()}"))
        return {}

    def updateMetadataForProject(self, projectId: int, updateMetadata: dict):
        """
        This method changes the metadata in all available ports to the given metadata values in given dict for specified projectId.
        """
        # get all ports registered to projectId
        allMetadata = []

        # get all ports registered to projectId
        logger.debug("start update for project method")
        ports = Project(testing=self.testing, projectId=projectId).ports
        logger.debug("project ports: {}".format(ports))

        # FIXME: parallize me
        for port in ports:
            logger.debug("work on port {}".format(port))
            port = port["port"]

            metadata = self.updateMetadataForProjectFromPort(
                port, projectId, updateMetadata)
            d = {
                    port: metadata
            }
            allMetadata.append(d)

        return allMetadata

    def updateMetadataForProjectFromPort(self, port: str, projectId: int, updateMetadata: dict):
        """
        This method changes the metadata in given port to the given metadata values in given dict for specified projectId.
        Returns the current metadata data, so you can check, if the update was successful or not.

        The given updateMetadata has to be a dict with the following struct:
        {
            "Creator": {
                "creatorName": "Max Mustermann", 
                ...
            }, 
            "Publisher": {
                    "publisher": "Lorem Ipsum"
            },
            ...
        }

        The struct of a metadata model have to be the same as described in the metadata api.
        """

        port = str(port).lower()

        # FIXME: parallize me
        for key, value in updateMetadata.items():
            key = str(key).lower()
            req = requests.patch(
                f"http://{self.getPortString(port)}/metadata/project/{projectId}/{key}", json=value)

            if req.status_code >= 300:
                logger.exception(
                    Exception(f"Update metadata for \"{key}\" failed with value \"{value}\""))

        return self.getMetadataForProjectFromPort(port, projectId)
