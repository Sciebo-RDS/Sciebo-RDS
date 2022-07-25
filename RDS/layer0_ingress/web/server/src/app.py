from urllib.parse import urlparse
import logging
from flask import request
from functools import wraps
import redis_pubsub_dict
from flask import Flask
import uuid
import requests
import os
import json
from flask_socketio import SocketIO
from flask_session import Session

from pathlib import Path
from dotenv import load_dotenv

env_path = Path("..") / ".env"
load_dotenv(dotenv_path=env_path)

use_predefined_user = (
    os.getenv("DEV_USE_PREDEFINED_USER", "False").capitalize() == "True"
)
use_tests_folder = os.getenv("DEV_USE_DUMPS_FOLDER", "False").capitalize() == "True"
verify_ssl = os.getenv("VERIFY_SSL", "False").capitalize() == "True"

use_embed_mode = os.getenv("EMBED_MODE", "False").capitalize() == "True"
use_proxy = os.getenv("DEV_USE_PROXY", "False").capitalize() == "True"
redirect_url = os.getenv("OWNCLOUD_OAUTH_CLIENT_REDIRECT")
authorize_url = os.getenv("OWNCLOUD_OAUTH_CLIENT_AUTHORIZE_URL")


redirect_url = "{}?response_type=token&client_id={}&redirect_uri={}".format(
    authorize_url, os.getenv("OWNCLOUD_OAUTH_CLIENT_ID"), redirect_url
)


startup_nodes = [
    {
        "host": os.getenv(
            "REDIS_HELPER_MASTER_SERVICE_HOST",
            "{}-master".format(os.getenv("REDIS_HELPER_HOST", "localhost")),
        ),
        "port": os.getenv("REDIS_HELPER_MASTER_SERVICE_PORT", "6379"),
    }
]

repl = ".:"
trans_tbl = "".maketrans(repl, "-" * len(repl))

from collections import UserDict


class DomainsDict(UserDict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.cache = {}

    def get_publickey(self, key):
        """Returns publickey. If not already cached, get it from the efss instance.

        Args:
            key (str): The key, equals to the same as domains key, to look up.

        Raises:
            ValueError: If the instance is not accessible, it raises ValueError

        Returns:
            str: the requested publickey
        """

        try:
            return self.cache[key]
        except KeyError:
            status_code = 500
            req = None
            url = self[key]["ADDRESS"]
            count = 5

            while status_code > 200 and count > 0:
                req = requests.get(
                    f"{url}/index.php/apps/rds/api/1.0/publickey",
                    verify=verify_ssl,
                )

                status_code = req.status_code
                count -= 1

            if status_code > 200:
                raise ValueError

            req = req.json()

            val = req.get("publickey", "").replace("\\n", "\n")
            self.cache[key] = val
            return val


# This handles also the single installation, because it is a one entry list in this case.
with open("domains.json") as f:
    domains = json.load(f)

domains_dict = DomainsDict({val["name"].translate(trans_tbl): val for val in domains})


try:
    from redis import Redis

    rc = Redis(
        **(startup_nodes[0]),
        db=0,
        health_check_interval=30,
        decode_responses=True,
    )
except:
    rc = None

clients = {}
timestamps = {}
flask_config = {
    "SESSION_TYPE": "filesystem",
    "SECRET_KEY": os.getenv("SECRET_KEY", uuid.uuid4().hex),
    "REMEMBER_COOKIE_HTTPONLY": False,
    "SESSION_PERMANENT": True,
    "DEBUG": True,
    "SESSION_COOKIE_HTTPONLY": True,
    "SESSION_COOKIE_SAMESITE": "None",
    "SESSION_COOKIE_SECURE": True,
    # "SERVER_NAME": os.getenv("RDS_OAUTH_REDIRECT_URI", os.getenv("SOCKETIO_HOST", "https://localhost")).replace("https://", "" ).replace("http://", "")
}

if os.getenv("USE_LOCAL_DICTS", "False").capitalize() == "True":
    user_store = {}
    research_progress = {}
else:
    from redis.cluster import RedisCluster, ClusterNode

    nodes = [ClusterNode(os.getenv("REDIS_SERVICE_HOST", "localhost"), os.getenv("REDIS_SERVICE_PORT", "6379"))]
    rcCluster = RedisCluster(
        startup_nodes=nodes,
        skip_full_coverage_check=True,
        cluster_down_retry_attempts=1,
    )

    rcCluster.cluster_info()  # provoke an error message
    user_store = redis_pubsub_dict.RedisDict(rcCluster, "web_userstore")
    research_progress = redis_pubsub_dict.RedisDict(rcCluster, "web_research_progress")
    # clients = redis_pubsub_dict.RedisDict(rcCluster, "web_clients")
    timestamps = redis_pubsub_dict.RedisDict(rcCluster, "tokenstorage_access_timestamps")

    flask_config["SESSION_TYPE"] = "redis"
    flask_config["SESSION_REDIS"] = rcCluster

app = Flask(
    __name__, static_folder=os.getenv("FLASK_STATIC_FOLDER", "/usr/share/nginx/html")
)

# add a TracingHandler for Logging
gunicorn_logger = logging.getLogger("gunicorn.error")
app.logger.handlers.extend(gunicorn_logger.handlers)
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
origins.update(
    {
        "{}://{}".format(v.scheme, v.netloc)
        for v in [urlparse(v["ADDRESS"]) for v in domains_dict.values()]
    }
)

socketio = SocketIO(
    app,
    cors_allowed_origins=origins,
    manage_session=False,
    logger=True,
    engineio_logger=True,
)
