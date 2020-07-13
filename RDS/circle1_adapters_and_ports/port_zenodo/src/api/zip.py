from flask import jsonify


def index():
    data = {"needsZip": True}
    return jsonify(data)
