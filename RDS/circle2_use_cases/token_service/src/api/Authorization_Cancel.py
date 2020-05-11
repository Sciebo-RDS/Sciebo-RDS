from flask import jsonify
from connexion_plus.Optimizer import FlaskOptimize


@FlaskOptimize.do_not_minify()
def index():
    return """
    <html>
    <body>
    <center>There was an error. You can close this window now. <button onclick="window.close()">Close</button></center>
    </body>
    </html>
    """
