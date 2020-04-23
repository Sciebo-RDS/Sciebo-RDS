from jsonschema import validate
import requests
import json

schema = requests.get(
    "https://raw.githubusercontent.com/Sciebo-RDS/Sciebo-RDS/connnectUI/RDS/circle2_use_cases/metadata/datacite_4.3_schema.json").json()


class Datacite:
    def __init__(self, dataciteMetadata):
        validate(instance=dataciteMetadata, schema=schema)
        self.data = dataciteMetadata

    def toJson(self):
        return json.dumps(self.data)

    def toDict(self):
        return self.data

    def toZenodoApi(self):
        # TODO: implement here the transformation from datacite to zenodo api
        newZenodoDict = self.data
        return newZenodoDict

    @classmethod
    def fromZenodoApi(cls, zenodoApiMetadata):
        # TODO: implement here the transformation from zenodo api to datacite
        newDict = zenodoApiMetadata
        return cls(newDict)
