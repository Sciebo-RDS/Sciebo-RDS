from flask import jsonify


def get():
    data = {"needsZip": True}
    return jsonify(data)
