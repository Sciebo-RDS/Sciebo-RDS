from lib.Service import Service
import requests
import logging
import zipfile
from io import BytesIO
import os
import threading
from RDS import FileTransferMode
from .Util import threadsafe_iter

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
        self.applyChanges = False

        self.testing = testing
        self.address = "http://layer3-research-manager" if testing is False else testing

        self.reload()

    def reload(self):
        req = requests.get(
            f"{self.address}/research/user/{self.userId}/research/{self.researchIndex}",
            verify=(os.environ.get("VERIFY_SSL", "True") == "True"),
        )

        json = req.json()
        logger.debug("reload in Research got: {}".format(json))

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
            try:
                b = self.removeAllFiles()
                logger.debug("Removed all files? {}".format(b))
            except Exception as e:
                logger.exception(e)

        try:
            self.triggerPassivePorts()
        except Exception as e:
            logger.exception(e)

        try:
            self.processPassivePortsWithShares()
        except Exception as e:
            logger.exception(e)

        try:
            self.processActivePorts()
        except Exception as e:
            logger.exception(e)

        return True

    def processPassivePortsWithShares(self):
        from Service import InvalidFiletransferMode, CannotCreateSharelink

        for importSvc in self.importServices:
            result = [
                (svc, svc.triggerPassiveMode(importSvc))
                for svc in self.getExportServices(mode=FileTransferMode.passiveWithLink)
            ]

            if not all(map(result, lambda x: x[1])):
                logger.warning(
                    f"Error in exportservice with sharelink \nimportservice: {importSvc} \nresult: {result}"
                )

    def processActivePorts(self):
        if len(self.getExportServices()) == 0:
            logger.debug("No active exportservice available")
            return False

        for svc in self.importServices:
            logger.debug("import service: {}".format(svc.getJSON()))

            useZipForContent = False

            if isFolderInFiles(svc.getFiles()):
                useZipForContent = True

            logger.debug(
                "use zipfile, because the folder holds folders again? {}".format(
                    useZipForContent
                )
            )

            if useZipForContent:
                mem_zip = BytesIO()
                zip = zipfile.ZipFile(mem_zip, mode="w", compression=zipfile.ZIP_STORED)

            for fileTuple in svc.getFiles(getContent=True):
                logger.debug(
                    "file: {}, contentlength: {}".format(
                        fileTuple[0], fileTuple[1].getbuffer().nbytes
                    )
                )

                logger.debug("write to zipfile? {}".format(useZipForContent))

                # TODO: needs tests
                if useZipForContent:
                    zip.writestr(fileTuple[0], fileTuple[1].read())
                    logger.debug("done writing to zipfile")

                # useZipForContent skips services, which needs zip, if folder in folder found.
                self.addFile(folderInFolder=useZipForContent, *fileTuple)

            if useZipForContent:
                import re

                def urlify(s):

                    # Remove all non-word characters (everything except numbers and letters)
                    s = re.sub(r"[^\w\s]", "", s)

                    # Replace all runs of whitespace with a single dash
                    s = re.sub(r"\s+", "-", s)

                    return s

                zip.close()

                results = [
                    exportSvc.addFile(
                        "{}_{}.zip".format(svc.servicename, urlify(svc.getFilepath())),
                        mem_zip,
                    )
                    for exportSvc in self.getExportServices()
                    if (exportSvc.zipForFolder)
                ]
        return True

    def triggerPassivePorts(self):
        if len(self.getExportServices(mode=FileTransferMode.passive)) == 0:
            logger.debug("No passive exportservice available")
            return False

        for importSvc in self.importServices:
            for exportSvc in [
                svc for svc in self.getExportServices(mode=FileTransferMode.passive)
            ]:
                exportSvc.triggerPassiveMode(importSvc)

    def getExportServices(self, mode=FileTransferMode.active):
        return [svc for svc in self.exportServices if svc.fileTransferMode == mode]

    def addFile(self, *args, **kwargs):
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

        try:
            folderInFolder = kwargs["folderInFolder"]
            del kwargs["folderInFolder"]
        except:
            folderInFolder = False

        logger.debug("folderInFolder: {}".format(folderInFolder))

        return [
            svc.addFile(*args, **kwargs)
            for svc in self.getExportServices()
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
        if str(file).endswith("/") or str(file).endswith("\\"):
            return True

    return False
