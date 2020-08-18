from lib.EnumStatus import Status
from lib.Port import Port
import json
import logging

logger = logging.getLogger()


class Project:
    def __init__(self, user, status=Status.CREATED, portIn=None, portOut=None):
        if portIn is None:
            portIn = []

        if portOut is None:
            portOut = []

        self.user = user
        self.status = status

        self.portIn = []
        self.portOut = []

        # test, if the port can be converted to port object
        try:
            for port in portIn:
                self.portIn.append(Port.fromDict(port))
            for port in portOut:
                self.portOut.append(Port.fromDict(port))
        except:
            self.portIn = portIn
            self.portOut = portOut

    def addPortIn(self, port):
        self.addPort(port, self.portIn)

    def addPortOut(self, port):
        self.addPort(port, self.portOut)

    def removePortIn(self, port):
        self.removePort(port, self.portIn)

    def removePortOut(self, port):
        self.removePort(port, self.portOut)

    @staticmethod
    def addPort(port, portList):
        """
        Adds port (type `Port`) to given portList.
        """
        portList.append(port)

    @staticmethod
    def removePort(port, portList):
        """
        Remove port from portList.
        Port can be `int` as index or an object with type `Port`.
        """
        if isinstance(port, int):
            try:
                del portList[port]
                return True
            except:
                return False

        index = None
        for i, current in enumerate(portList):
            if current == port:
                index = i
                break

        if index is not None:
            del portList[index]
            return True

        return False

    def getPortIn(self):
        return self.portIn

    def getPortOut(self):
        return self.portOut

    def nextStatus(self):
        """
        Set the next status and returns the new value.
        It returns the same value, if you already at the last state.
        """
        if self.status.hasNext():
            self.status = self.status.succ()
        return self.status

    def setDone(self):
        """
        Set the status of this project to done.
        If already done or deleted, then return False. Otherwise True.
        """

        if self.status == Status.DONE or self.status == Status.DELETED:
            return False

        self.status = Status.DONE
        return True

    def getJSON(self):
        return json.dumps(self.getDict())

    @classmethod
    def fromJSON(cls, dataJson: str):
        dataList = json.loads(dataJson)

        l = []
        for data in dataList:
            fixedData = json.loads(data)
            fixedData["user"] = fixedData["userId"]
            del fixedData["userId"]

            fixedData["status"] = Status(fixedData["status"])

            try:
                researchId = fixedData["researchId"]
                researchIndex = fixedData["researchIndex"]

                del fixedData["researchId"]
                del fixedData["researchIndex"]
            except Exception as e:
                logger.error("{}, data: {}".format(e, fixedData))
                logger.debug("no researchIndex or Id found")

            project = cls(**fixedData)

            try:
                project.researchId = researchId
                project.researchIndex = researchIndex
            except Exception as e:
                logger.error("{}, data: {}".format(e, project.dict))

            l.append(project)

        return l

    def getDict(self):
        return self.dict

    @property
    def dict(self):
        obj = {
            "userId": self.user,
            "status": self.status.value,
            "portIn": [port.getDict() for port in self.portIn],
            "portOut": [port.getDict() for port in self.portOut],
        }

        try:
            obj["researchId"] = self.researchId
            obj["researchIndex"] = self.researchIndex
        except:
            pass

        return obj

    def __eq__(self, obj):
        if not isinstance(obj, Project):
            return False

        d1 = self.getDict()
        d2 = obj.getDict()

        # check if one dict is subset of the other dict, so we can ignore if there is set projectId etc. through projectService
        return (d1.items() <= d2.items()) or (d1.items() >= d2.items())
