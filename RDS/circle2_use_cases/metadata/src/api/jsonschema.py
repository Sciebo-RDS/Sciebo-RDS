from lib.Metadata import Metadata
from flask import jsonify
import json


def index():
    # taken from https://raw.githubusercontent.com/datacite/schema/master/source/json/kernel-4.3/datacite_4.3_schema.json
    with open("../../datacite_4.3_schema.json", "r") as file:
        return jsonify({
            "kernelversion": "4.3",
            "schema": json.load(file)
        })
