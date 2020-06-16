from enum import Enum, auto


class Status(Enum):
    """
    The order represents the workflow through the states. So the successor of each status is the next in line.
    """

    CREATED = auto()
    WORK = auto()
    DONE = auto()
    DELETED = auto()

    def succ(self):
        if self.hasNext():
            return Status(self.value + 1)
        raise IndexError("out of status. You are already at the last state.")

    def hasNext(self):
        return not (self.value is len(Status))

    def getDict(self):
        return self.value
