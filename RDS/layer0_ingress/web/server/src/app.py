import logging
from .TracingHandler import TracingHandler
from opentracing_instrumentation.client_hooks import install_all_patches
from jaeger_client import Config as jConfig
from jaeger_client.metrics.prometheus import (
    PrometheusMetricsFactory,
)
from flask import request
from functools import wraps
import opentracing
from flask_opentracing import FlaskTracing
from prometheus_flask_exporter.multiprocess import GunicornPrometheusMetrics
import redis_pubsub_dict
from rediscluster import RedisCluster
from flask import Flask
import uuid
import os
import json
from flask_socketio import SocketIO
from flask_session import Session

from pathlib import Path
from dotenv import load_dotenv
env_path = Path('..') / '.env'
load_dotenv(dotenv_path=env_path)

use_predefined_user = (os.getenv('DEV_USE_PREDEFINED_USER', 'False') == 'True')
use_tests_folder = (os.getenv('DEV_USE_TESTS_FOLDER', 'False') == 'True')

use_embed_mode = (os.getenv('EMBED_MODE', 'False') == 'True')
use_proxy = (os.getenv('DEV_USE_PROXY', 'False') == 'True')
redirect_url = os.getenv("OWNCLOUD_OAUTH_CLIENT_REDIRECT")
authorize_url = os.getenv("OWNCLOUD_OAUTH_CLIENT_AUTHORIZE_URL")


redirect_url = "{}?response_type=token&client_id={}&redirect_uri={}".format(
    authorize_url,
    os.getenv("OWNCLOUD_OAUTH_CLIENT_ID"),
    redirect_url
)


startup_nodes = [
    {
        "host": "{}-master".format(os.getenv("REDIS_HELPER_HOST", "localhost")),
        "port": os.getenv("REDIS_HELPER_PORT", "6379"),
    }
]


try:
    from redis import Redis

    rc = Redis(
        **(startup_nodes[0]),
        db=0,
        decode_responses=True,
    )
except:
    rc = None

clients = {}
flask_config = {
    'SESSION_TYPE': 'filesystem',
    "SECRET_KEY": os.getenv("SECRET_KEY", uuid.uuid4().hex),
    "REMEMBER_COOKIE_HTTPONLY": False,
    "SESSION_PERMANENT": True,
    'DEBUG': True
}

if os.getenv("USE_LOCAL_DICTS", "False") == "True":
    user_store = {}
else:
    startup_nodes_cluster = [
        {
            "host": os.getenv("REDIS_HOST", "localhost"),
            "port": os.getenv("REDIS_PORT", "6379"),
        }
    ]

    rcCluster = RedisCluster(
        startup_nodes=startup_nodes_cluster,
        skip_full_coverage_check=True,
        cluster_down_retry_attempts=1,
    )

    rcCluster.cluster_info()  # provoke an error message
    user_store = redis_pubsub_dict.RedisDict(rcCluster, "web_userstore")
    # clients = redis_pubsub_dict.RedisDict(rcCluster, "web_clients")

    flask_config['SESSION_TYPE'] = 'redis'
    flask_config["SESSION_REDIS"] = rcCluster

app = Flask(__name__,
            static_folder=os.getenv(
                "FLASK_STATIC_FOLDER", "/usr/share/nginx/html")
            )

### Tracing begin ###
tracer_config = {
    "sampler": {"type": "const", "param": 1, },
    "local_agent": {
        "reporting_host": "jaeger-agent",
        "reporting_port": 5775,
    },
    "logging": True,
}

config = jConfig(
    config=tracer_config,
    service_name=f"RDSWebConnexionPlus",
    metrics_factory=PrometheusMetricsFactory(
        namespace=f"RDSWebConnexionPlus"
    ),
)


tracer_obj = config.initialize_tracer()
tracing = FlaskTracing(tracer_obj, True, app)
install_all_patches()

# add a TracingHandler for Logging
gunicorn_logger = logging.getLogger("gunicorn.error")
app.logger.handlers.extend(gunicorn_logger.handlers)
app.logger.addHandler(TracingHandler(tracer_obj))
app.logger.setLevel(gunicorn_logger.level)
### Tracing end ###

app.config.update(flask_config)

try:
    metrics = GunicornPrometheusMetrics(app)
except:
    print("error in prometheus setup")
Session(app)

socketio = SocketIO(
    app,
    cors_allowed_origins=json.loads(os.getenv("FLASK_ORIGINS")),
    manage_session=False
)
