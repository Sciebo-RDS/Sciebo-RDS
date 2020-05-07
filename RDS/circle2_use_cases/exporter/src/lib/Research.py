from lib.Service import Service
import multiprocessing
import requests
import logging

logger = logging.getLogger()


class Research():
    def __init__(self, userId=None, researchIndex=None, researchId=None, testing=False):
        if (userId is None or researchIndex is None) and researchId is None:
            raise ValueError(
                "(userId or researchIndex) and researchId are None.")

        self.importServices = []
        self.exportServices = []

        self.userId = userId
        self.researchIndex = researchIndex
        self.researchId = researchId

        self.status = None

        self.autoSync = False
        self.applyChanges = True

        self.testing = testing
        self.address = "http://circle3-research-manager" if testing is False else testing

        self.reload()

    def reload(self):
        req = requests.get(
            f"{self.address}/research/user/{self.userId}/research/{self.researchIndex}")

        json = req.json()

        self.importServices = []
        for port in json.get("portIn"):
            svc = Service.fromDict(port, userId=self.userId,
                                   researchIndex=self.researchIndex, testing=self.testing)
            self.importServices.append(svc)

        self.exportServices = []
        for port in json.get("portOut"):
            svc = Service.fromDict(port, userId=self.userId,
                                   researchIndex=self.researchIndex, testing=self.testing)
            self.exportServices.append(svc)

        self.status = json.get("status")

        logger.debug("import: {},\nexport: {}".format([x.getJSON(
        ) for x in self.exportServices], [x.getJSON() for x in self.exportServices]))

        return True

    def getServices(self):
        """
        Returns all services, which are currently configured in the research project.
        """
        return self.importServices + self.exportServices

    def getServicesImport(self):
        """
        Returns all services, which are currently configured as import in the research project.
        """

        return self.importServices

    def getServicesExport(self):
        """
        Returns all services, which are currently configured as export in the research project.
        """

        return self.exportServices

    def synchronization(self):
        """
        Synchronize all files between import services and export services.
        """

        if self.applyChanges:
            self.removeAllFiles()

        for svc in self.importServices:
            logger.debug("import service: {}".format(svc.getJSON()))

            for fileTuple in svc.getFiles(getContent=True):
                self.addFile(*fileTuple)

    def addFile(self, *args, **kwargs):
        """
        Wrapper function to call addFile in all export services objects with parameters.
        """

        with multiprocessing.Pool() as pool:
            pool.map(Service.addFile(args, kwargs), self.exportServices)

    def removeAllFiles(self):
        """
        Remove all files in export services.

        Returns a boolean.
        """

        with multiprocessing.Pool() as pool:
            return not (False in pool.map(Service.removeAllFiles, self.exportServices))

    def removeFile(self, filepath):
        """
        Remove file with given filepath in all export services.
        """
        def wrapper(*args, **kwargs):
            def func(svc):
                return svc.removeFile(args, kwargs)
            return func

        with multiprocessing.Pool() as pool:
            pool.map(wrapper(filepath), self.exportServices)

    def removeFileFromService(self, file_id, service):
        """
        Remove file with id in export service.
        """
        # TODO
        raise NotImplementedError()

    def getFiles(self):
        from functools import reduce

        return list(set(reduce(lambda x, y: x + y, [svc.getFiles() for svc in self.importServices])))
