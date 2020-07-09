from lib.Service import Service
from pathos.multiprocessing import ProcessingPool as Pool
import requests
import logging
import zipfile
from io import BytesIO
import os

logger = logging.getLogger()


class Research:
    def __init__(self, userId=None, researchIndex=None, researchId=None, testing=False):
        if (userId is None or researchIndex is None) and researchId is None:
            raise ValueError("(userId or researchIndex) and researchId are None.")

        self.importServices = []
        self.exportServices = []

        self.userId = userId
        self.researchIndex = researchIndex
        self.researchId = researchId

        self.status = None

        self.autoSync = False
        self.applyChanges = True

        self.testing = testing
        self.address = (
            "http://circle3-research-manager" if testing is False else testing
        )

        self.reload()

    def reload(self):
        req = requests.get(
            f"{self.address}/research/user/{self.userId}/research/{self.researchIndex}",
            verify=(os.environ.get("VERIFY_SSL", "True") == "True"),
        )

        json = req.json()

        self.importServices = []
        for port in json.get("portIn"):
            svc = Service.fromDict(
                port,
                userId=self.userId,
                researchIndex=self.researchIndex,
                testing=self.testing,
            )
            self.importServices.append(svc)

        self.exportServices = []
        for port in json.get("portOut"):
            svc = Service.fromDict(
                port,
                userId=self.userId,
                researchIndex=self.researchIndex,
                testing=self.testing,
            )
            self.exportServices.append(svc)

        self.status = json.get("status")

        logger.debug(
            "import: {},\nexport: {}".format(
                [x.getJSON() for x in self.importServices],
                [x.getJSON() for x in self.exportServices],
            )
        )

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
            b = self.removeAllFiles()
            logger.debug("Removed all files? {}".format(b))

        for svc in self.importServices:
            logger.debug("import service: {}".format(svc.getJSON()))

            saveContent = False

            if isFolderInFiles(svc.getFiles()):
                logger.debug("use zipfile, because the folder holds folders again")
                saveContent = True

            if saveContent:
                mem_zip = BytesIO()
                zip = zipfile.ZipFile(
                    mem_zip, mode="w", compression=zipfile.ZIP_DEFLATED
                )

            for fileTuple in svc.getFiles(getContent=True):
                logger.debug(
                    "file: {}, content: {}".format(fileTuple[0], len(fileTuple[1]))
                )

                # TODO: needs tests
                if saveContent:
                    zip.writestr(*fileTuple)

                # saveContent skips services, which needs zip, if folder in folder found.
                self.addFile(folderInFolder=saveContent, *fileTuple)

            if saveContent:
                results = [
                    exportSvc.addFile(
                        "Files_from_{}.zip".format(svc.servicename), mem_zip.getvalue(),
                    )
                    for exportSvc in self.exportServices
                    if exportSvc.zipForFolder
                ]

                zip.close()

    def addFile(self, folderInFolder=False, *args, **kwargs):
        """
        Wrapper function to call addFile in all export services objects with parameters.

        folderInFolder (bool): Only if folderInFolder is True, then it will be checked, if service needs a zip for folders in folder upload.

        Returns:
            list: Returns list of booleans, if it succeeds or not. The order follows the self.exportServices order.
        """
        logger.debug("args: {}, kwargs: {}".format(args, kwargs))

        """
        argLeft = [args[0]]
        argRight = [args[1]]

        with Pool() as pool:
            pool.map(Service.addFile, self.exportServices, argLeft *
                     len(self.exportServices), argRight*len(self.exportServices))
        """

        return [
            svc.addFile(*args, **kwargs)
            for svc in self.exportServices
            if not (folderInFolder and svc.zipForFolder)
        ]

    def removeAllFiles(self):
        """
        Remove all files in export services.

        Returns a boolean.
        """

        logger.debug("remove all files in export files")

        """
        with Pool() as pool:
            return not (False in pool.map(Service.removeAllFiles, self.exportServices))
        """
        return not (False in [svc.removeAllFiles() for svc in self.exportServices])

    def removeFile(self, filepath):
        """
        Remove file with given filepath in all export services.
        """

        logger.debug("remove file {}".format(filepath))

        """
        with Pool() as pool:
            pool.map(Service.removeFile, self.exportServices, filepath)
        """

        return [svc.removeFile(filepath) for svc in self.exportServices]

    def removeFileFromService(self, file_id, service):
        """
        Remove file with id in export service.
        """
        # TODO
        raise NotImplementedError()

    def getFiles(self):
        from functools import reduce

        return list(
            set(
                reduce(
                    lambda x, y: x + y, [svc.getFiles() for svc in self.importServices]
                )
            )
        )


def isFolderInFiles(files):
    for file in files:
        if "/" in file or "\\" in file:
            return True

    return False
