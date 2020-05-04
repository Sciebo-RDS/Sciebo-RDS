from lib.Service import Service
import multiprocessing
import requests


class Research():
    def __init__(self, userId=None, researchIndex=None, researchId=None, testing_address=None):
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

        self.address = "circle3-research-manager" if testing_address is None else testing_address

        self.reload()

    def reload(self):
        req = requests.get(
            f"{self.address}/user/{self.userId}/research/{self.researchIndex}")

        json = req.json

        self.importServices = []
        for port in json.get("portIn"):
            svc = Service.fromDict(port, userId=self.userId,
                                   researchIndex=self.researchIndex)
            self.importServices.append(svc)

        self.exportServices = []
        for port in json.get("portOut"):
            svc = Service.fromDict(port, userId=self.userId,
                                   researchIndex=self.researchIndex)
            self.exportServices.append(svc)

        self.status = json.get("status")

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
            self.addFile(svc.getFiles())

    def addFile(self, *args, **kwargs):
        """
        Wrapper function to call addFile in all export services objects with parameters.
        """

        def wrapper(*args, **kwargs):
            def func(svc):
                return svc.addFile(args, kwargs)
            return func

        with multiprocessing.Pool() as pool:
            pool.map(wrapper(args, kwargs), self.exportServices)

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
        pass

    def getFiles(self):
        from functools import reduce

        return set(reduce((lambda x, y: x + y, [svc.files for svc in self.importServices])))
