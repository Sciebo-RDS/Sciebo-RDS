class Metadata():
    def __init__(self):
        pass

    def getProjectId(self, userId, projectIndex):
        return 0

    def getPortIn(self, userId, projectIndex):
        return []

    def getPortOut(self, userId, projectIndex):
        return []

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

        # updates all metadata in givne dict for received ports for projectId
        return {}
