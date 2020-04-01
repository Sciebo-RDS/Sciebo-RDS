from flask import request, jsonify


def index(project_id):

    return jsonify({})


def get(project_id, file_id):

    return jsonify({})


def patch(project_id):
    req = request.json

    jsonify({})
