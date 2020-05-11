from flask import jsonify


def index():
    return """
    <html>
    <body>
    <center>All wents fine. You can close this window now. <button click=\"close();\">Close</button></center>
    </body>
    </html>
    """