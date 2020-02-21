from src.lib.EnumStatus import Status


class Project():
    def __init__(self, user, portIn=[], portOut=[]):
        self.user = user
        self.status = Status.CREATED
        self.portIn = portIn
        self.portOut = portOut

    def addPortIn(self, port):
        self.portIn.append(port)

    def addPortOut(self, port):
        self.portOut.append(port)

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
            "user": self.user,
            "status": self.status,
            "portIn": self.portIn,
            "portOut": self.portOut
        }

        return obj
