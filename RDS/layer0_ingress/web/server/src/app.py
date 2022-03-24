from urllib.parse import urlparse
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
import redis_pubsub_dict
from rediscluster import RedisCluster
from flask import Flask
import uuid
import requests
import os
import json
from flask_socketio import SocketIO
from flask_session import Session

from pathlib import Path
from dotenv import load_dotenv
env_path = Path('..') / '.env'
load_dotenv(dotenv_path=env_path)

use_predefined_user = (os.getenv('DEV_USE_PREDEFINED_USER', 'False') == 'True')
use_tests_folder = (os.getenv('DEV_USE_DUMPS_FOLDER', 'False') == 'True')

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
        "host": os.getenv("REDIS_HELPER_MASTER_SERVICE_HOST", "{}-master".format(os.getenv("REDIS_HELPER_HOST", "localhost"))),
        "port": os.getenv("REDIS_HELPER_MASTER_SERVICE_PORT", "6379"),
    }
]

repl = ".:"
trans_tbl = "".maketrans(repl, "-" * len(repl))

# This handles also the single installation, because it is a one entry list in this case.
with open("domains.json") as f:
    domains = json.load(f)

for i in range(len(domains)):
    url = domains[i]["ADDRESS"]
    req = requests.get(
        f"{url}/apps/rds/api/1.0/publickey",
        verify=os.getenv("VERIFY_SSL", "False") == "True"
    ).json()

    domains[i]["publickey"] = req.get("publickey", "").replace("\\n", "\n")

domains = {val["name"].translate(trans_tbl): val for val in domains}


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
    'DEBUG': True,
    "SESSION_COOKIE_HTTPONLY": True,
    "SESSION_COOKIE_SAMESITE": "None",
    "SESSION_COOKIE_SECURE": True,
    #"SERVER_NAME": os.getenv("RDS_OAUTH_REDIRECT_URI", os.getenv("SOCKETIO_HOST", "https://localhost")).replace("https://", "" ).replace("http://", "")
}

if os.getenv("USE_LOCAL_DICTS", "False") == "True":
    user_store = {}
else:
    startup_nodes_cluster = [
        {
            "host": os.getenv("REDIS_SERVICE_HOST", "localhost"),
            "port": os.getenv("REDIS_SERVICE_PORT", "6379"),
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
    from prometheus_flask_exporter.multiprocess import GunicornPrometheusMetrics
    metrics = GunicornPrometheusMetrics(app)
except Exception as e:
    print(f"error in prometheus setup: {e}")
Session(app)

origins = set(json.loads(os.getenv("FLASK_ORIGINS")))
origins.update({"{}://{}".format(v.scheme, v.netloc)
                for v in [urlparse(v["ADDRESS"])
                          for v in domains.values()
                          ]
                })

socketio = SocketIO(
    app,
    cors_allowed_origins=origins,
    manage_session=False,
    logger=True, engineio_logger=True
)
