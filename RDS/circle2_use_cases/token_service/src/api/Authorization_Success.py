from flask import jsonify

def index():
    return jsonify({"success": True})
