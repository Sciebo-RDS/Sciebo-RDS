from flask import jsonify
from connexion_plus.Optimizer import FlaskOptimize


@FlaskOptimize.do_not_minify()
def index():
    return """
    <html>
    <body>
    <center>You are good to go. You can close this window now. <button click=\"close();\">Close</button></center>
    </body>
    </html>
    """
