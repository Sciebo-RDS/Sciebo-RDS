import json
import os

class File:
    def __init__(self, path):
        self.path = path

    def to_dict(self):
        return {
            "path": self.path
        }

    @classmethod
    def from_dict(cls, fileDict):
        return cls(**fileDict)

    def to_json(self):
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, fileJSON):
        return cls.from_dict(json.loads(fileJSON))
