from flask import jsonify


def index():
    return """
    <html>
    <body>
    <center>There was an error. You can close this window now. <button click=\"close();\">Close</button></center>
    </body>
    </html>
    """
