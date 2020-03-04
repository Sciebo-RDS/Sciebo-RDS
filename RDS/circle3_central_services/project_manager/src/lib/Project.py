from lib.EnumStatus import Status


class Project():
    def __init__(self, user, portIn=None, portOut=None):
        if portIn is None:
            portIn = []

        if portOut is None:
            portOut = []

        self.user = user
        self.status = Status.CREATED
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
            if current is port:
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

    def getJSON(self):
        import json
        return json.dumps(self.getDict())

    def getDict(self):
        obj = {
            "userId": self.user,
            "status": self.status.value,
            "portIn": [port.getDict() for port in self.portIn],
            "portOut": [port.getDict() for port in self.portOut]
        }

        return obj

    def __eq__(self, obj):
        if not isinstance(obj, Project):
            return False

        d1 = self.getDict()
        d2 = obj.getDict()

        p1 = d1.get("projectId")
        p2 = d2.get("projectId")

        if p1 is None and p2 is not None:
            del d2["projectId"]

        elif p1 is not None and p2 is None:
            del d1["projectId"]

        return (d1 == d2)
