from flask import jsonify


def index():
    # TODO: This should be done with creation for subfolder, because OSF supports it.
    data = {"needsZip": True}
    return jsonify(data)
