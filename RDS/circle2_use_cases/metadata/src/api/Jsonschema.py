from lib.Metadata import Metadata
from flask import jsonify
import json


def index():
    # taken from https://raw.githubusercontent.com/datacite/schema/master/source/json/kernel-4.3/datacite_4.3_schema.json
    # https://sandbox.zenodo.org//schemas/deposits/records/legacyrecord.json
    # example can be found here: https://raw.githubusercontent.com/datacite/schema/master/source/json/kernel-4.3/example/datacite-example-HasMetadata-v4.json
    with open("zenodo_schema.json", "r") as file:
        return jsonify({
            "kernelversion": "zenodo",
            "schema": json.dumps(json.load(file))
        })
