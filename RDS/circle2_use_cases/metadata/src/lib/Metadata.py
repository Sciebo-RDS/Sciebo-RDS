import requests
import logging
from lib.Research import Research

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

    def getResearchId(self, userId, researchIndex):
        """
        This method returns the corresponding researchId to the given userId and researchIndex.
        """
        return Research(testing=self.testing, userId=userId, researchIndex=researchIndex).researchId

    def getPortString(self, port: str):
        res = f"circle1-{port}"

        if self.testing:
            res = self.testing

        return res

    def getMetadataForResearch(self, userId: str = None, researchIndex: int = None, researchId: int = None):
        """
        This method returns the metadata from all available ports for specified researchId.
        """
        allMetadata = []

        logger.debug("start get metadata method for research")

        ports = Research(testing=self.testing,
                        userId=userId, researchIndex=researchIndex, researchId=researchId).ports

        logger.debug(f"got ports {ports}")

        # FIXME: parallize me
        for port in ports:
            logger.debug(f"work on port {port}")
            port = port["port"]
            metadata = self.getMetadataForResearchFromPort(port, researchId)
            d = {
                "port": port,
                "metadata": metadata
            }
            allMetadata.append(d)

        return allMetadata

    def getMetadataForResearchFromPort(self, port: str, researchId: int):
        """
        This method returns the metadata from given port for specified researchId.
        Returns a dict, which was described in the metadata api endpoint "/metadata/research/{research-id}" or an empty one.
        """
        # pull all metadata from given port for researchId

        req = requests.get(
            f"http://{self.getPortString(port)}/metadata/research/{researchId}")

        if req.status_code == 200:
            return req.json()

        logger.exception(Exception(f"Metadata model req: {req.content()}"))
        return {}

    def updateMetadataForResearch(self, researchId: int, updateMetadata: dict):
        """
        This method changes the metadata in all available ports to the given metadata values in given dict for specified researchId.
        """
        # get all ports registered to researchId
        allMetadata = []

        # get all ports registered to researchId
        logger.debug("start update for research method")
        ports = Research(testing=self.testing, researchId=researchId).ports
        logger.debug("research ports: {}".format(ports))

        # FIXME: parallize me
        for port in ports:
            logger.debug("work on port {}".format(port))
            port = port["port"]

            metadata = self.updateMetadataForResearchFromPort(
                port, researchId, updateMetadata)
            d = {
                "port": port,
                "metadata": metadata
            }
            allMetadata.append(d)

        return allMetadata

    def updateMetadataForResearchFromPort(self, port: str, researchId: int, updateMetadata: dict):
        """
        This method changes the metadata in given port to the given metadata values in given dict for specified researchId.
        Returns the current metadata data, so you can check, if the update was successful or not.

        The given updateMetadata has to be a dict with the following struct:
        {
            "Creator": [{
                "creatorName": "Max Mustermann", 
                ...
            }], 
            "Publisher": {
                    "publisher": "Lorem Ipsum"
            },
            ...
        }

        The struct of a metadata model have to be the same as described in the metadata api.
        """

        port = str(port).lower()

        reqMetadata = {}

        # FIXME: parallize me
        for key, value in updateMetadata.items():
            keyL = str(key).lower()
            req = requests.patch(
                f"http://{self.getPortString(port)}/metadata/research/{researchId}/{keyL}", json=value)

            if req.status_code >= 300:
                logger.exception(
                    Exception(f"Update metadata for \"{keyL}\" failed with value \"{value}\""))

            reqMetadata[key] = req.json()

        return reqMetadata
