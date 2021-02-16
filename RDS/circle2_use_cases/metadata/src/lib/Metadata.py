import requests
import logging
import json
import os
from lib.Research import Research
from RDS import Util

logger = logging.getLogger()


class Metadata:
    def __init__(self, testing: str = None):
        """
        This is the constructor. No needed parameters.

        Testing has to be valid url string without protocol schema (e.g. http),
        so this class use the given address for all requests.
        """
        self.testing = None

        if testing is not None and testing is not False:
            self.testing = testing

    def getResearchId(self, userId, researchIndex):
        """
        This method returns the corresponding researchId to the given userId and researchIndex.
        """
        return Research(
            testing=self.testing, userId=userId, researchIndex=researchIndex
        ).researchId

    def getPortString(self, port: str):
        res = f"circle1-{port}"

        if self.testing:
            res = self.testing

        return res

    def getMetadataForResearch(
        self,
        userId: str = None,
        researchIndex: int = None,
        researchId: int = None,
        metadataFields=None,
    ):
        """
        This method returns the metadata from all available ports for specified researchId.
        """
        allMetadata = []

        logger.debug("start get metadata method for research")

        research = Research(
            testing=self.testing,
            userId=userId,
            researchIndex=researchIndex,
            researchId=researchId,
        )

        ports = research.getPortsWithProjectId()

        logger.debug(f"got ports {ports}")

        # FIXME: parallize me
        for port, projectId in ports:
            # beware, that projectId could also be a string or sth else
            if projectId is None:
                continue

            portname = port["port"]

            if not portname.startswith("port-"):
                portname = "port-{}".format(portname)

            token = Util.loadToken(
                research.userId, portname
            )

            data = Util.parseToken(token)
            data["metadata"] = metadataFields

            logger.debug(f"work on port {port} with apiKey {token}")
            port = port["port"]
            metadata = self.getMetadataForProjectFromPort(
                port,
                projectId,
                apiKeyMetadata=data,
            )
            d = {"port": port, "metadata": metadata}
            allMetadata.append(d)

        return allMetadata

    def getMetadataForProjectFromPort(
        self, port: str, projectId: int, apiKeyMetadata=None
    ):
        """
        This method returns the metadata from given port for specified projectId.
        Beware that the projectId comes from the service, which is connected throug the port.
        Returns a dict, which was described in the metadata api endpoint "/metadata/research/{research-id}" or an empty one.

        Be careful to use apiKeyMetadata only with the struct: {apiKey: userAPIKey, metadata: metadata}
        """
        # pull all metadata from given port for researchId

        if apiKeyMetadata is not None:
            req = requests.get(
                f"http://{self.getPortString(port)}/metadata/project/{projectId}",
                json=apiKeyMetadata,
                verify=(os.environ.get("VERIFY_SSL", "True") == "True"),
            )

        else:
            req = requests.get(
                f"http://{self.getPortString(port)}/metadata/project/{projectId}",
                verify=(os.environ.get("VERIFY_SSL", "True") == "True"),
            )

        if req.status_code == 200:
            return req.json()

        logger.exception(Exception(f"Metadata model req: {req.content}"))
        return {}

    def updateMetadataForResearch(self, researchId: int, updateMetadata: dict):
        """
        This method changes the metadata in all available ports to the given metadata values in given dict for specified researchId.
        """
        # get all ports registered to researchId
        allMetadata = []

        # get all ports registered to researchId
        logger.debug("start update for research method")

        research = Research(testing=self.testing, researchId=researchId)
        ports = research.getPortsWithProjectId()
        logger.debug("research ports: {}".format(ports))

        # FIXME: parallize me
        for (port, projectId) in ports:
            if projectId is None:
                continue

            portname = port["port"]

            if not portname.startswith("port-"):
                portname = "port-{}".format(portname)

            token = Util.loadToken(
                research.userId, portname
            )

            logger.debug("work on port {}".format(port))
            port = portname

            data = Util.parseToken(token)
            data["metadata"] = updateMetadata

            metadata = self.updateMetadataForResearchFromPort(
                port, projectId, data
            )
            d = {"port": port, "metadata": metadata}
            allMetadata.append(d)

        return allMetadata

    def updateMetadataForResearchFromPort(
        self, port: str, projectId: int, updateMetadata: dict
    ):
        """
        This method changes the metadata in given port to the given metadata values in given dict for specified projectId.
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

        The struct of a metadata model have to be the same as described in the metadata api with the following addition.

        Be careful to use updateMetadata only with the struct: {apiKey: userAPIKey, metadata: metadata}
        """

        port = str(port).lower()

        headers = {"content-type": "application/json"}

        req = requests.patch(
            f"http://{self.getPortString(port)}/metadata/project/{projectId}",
            data=json.dumps(updateMetadata),
            headers=headers,
            verify=(os.environ.get("VERIFY_SSL", "True") == "True"),
        )

        if req.status_code >= 300:
            logger.exception(
                Exception(f'Update metadata for "{updateMetadata}" failed')
            )

        return req.json()

    def publish(self, researchId: int = None):
        """Publishes research in all configured export services.
        This function implements the parameters like self.getProjects.
        If you provide only user, then all researches will be published at once. 
        Otherwise only the given research with Index or Id.

        Args:
            researchId (int, optional): Defaults to None.
        """
        # TODO: needs tests

        def publishInPort(port, projectId, token):
            headers = {"content-type": "application/json"}

            data = Util.parseToken(token)

            req = requests.put(
                "http://{}/metadata/project/{}".format(
                    self.getPortString(port), projectId
                ),
                data=json.dumps(data),
                headers=headers,
                verify=(os.environ.get("VERIFY_SSL", "True") == "True"),
            )

            if req.status_code >= 300:
                logger.exception(
                    Exception(f'Publishing fails')
                )

            return req.status_code == 200

        research = Research(testing=self.testing, researchId=researchId)
        ports = research.getPortsWithProjectId()
        logger.debug("research ports: {}".format(ports))

        # FIXME: parallize me
        for (port, projectId) in ports:
            if projectId is None:
                continue

            portname = port["port"]

            if not portname.startswith("port-"):
                portname = "port-{}".format(portname)

            apiKey = Util.loadToken(
                research.userId, portname
            ).access_token

            logger.debug("work on port {}".format(port))
            port = port["port"]

            publishInPort(port, projectId, apiKey)

        return True
