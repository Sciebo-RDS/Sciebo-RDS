from jsonschema import validate
import requests
import json, os

schema = requests.get(
    "https://raw.githubusercontent.com/datacite/schema/master/source/json/kernel-4.2/datacite_4.2_schema.json",
    verify=(os.environ.get("VERIFY_SSL", "True") == "True"),
).json()

"""
This class represents a valid datacite metadata collection.

Initialization:
    `dc = Datacite(dataciteMetadata)`
    dataciteMetadata needs to be a valid datacite schema, because otherwise it will throw a validation exception, because we validates it.

    When you have a zenodo api metadata schema, you can initialize the corresponding datacite model:
    `dc = Datacite.fromZenodoApi(zenodoMetadata)`

Access Creators Attribute:
    `dc.creators`

Get ZenodoApi Metadata schema:
    `dc.toZenodoApi()`
"""


class Datacite:
    def __init__(self, dataciteMetadata):
        validate(instance=dataciteMetadata, schema=schema)

        for key, value in dataciteMetadata.items():
            setattr(self, key, value)

    def toJson(self):
        return json.dumps(self.__dict__)

    def toDict(self):
        return self.__dict__

    def toZenodoApi(self):
        # TODO: implement here the transformation from datacite to zenodo api
        newZenodoDict = self.toDict()
        return newZenodoDict

    @classmethod
    def fromZenodoApi(cls, zenodoApiMetadata):
        # TODO: implement here the transformation from zenodo api to datacite
        newDict = zenodoApiMetadata
        return cls(newDict)
