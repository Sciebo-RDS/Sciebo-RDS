import json


class File:
    def __init__(self, id, path):
        self.id = id
        self.path = path

    def to_dict(self):
        return {
            "id": self.id,
            "path": self.path
        }

    @classmethod
    def from_dict(cls, fileDict):
        return cls(fileDict.id, fileDict.path)

    def to_json(self):
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, fileJSON):
        return cls.from_dict(json.loads(fileJSON))
