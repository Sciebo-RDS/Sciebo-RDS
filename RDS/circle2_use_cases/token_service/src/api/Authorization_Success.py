from flask import jsonify


def index():
    return "<html><body><center>It works. You can close this window now. <button click=\"close();\">Close</button></center</body></html>"
