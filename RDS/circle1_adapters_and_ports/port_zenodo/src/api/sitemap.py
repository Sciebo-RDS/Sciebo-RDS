import json
from flask import jsonify, current_app as app
from connexion_plus.Optimizer import FlaskOptimize

@FlaskOptimize.set_cache_timeout()
def index():
    """Generate sitemap.xml """
    pages = []
    # All pages registed with flask apps
    for rule in app.url_map.iter_rules():
        if "GET" in rule.methods:
            pages.append(rule.rule)

    return jsonify(pages)
