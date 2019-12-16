from flask import jsonify

def index():
    return jsonify({"success": False, "error": "Authorization was not successful, because it was canceled."})