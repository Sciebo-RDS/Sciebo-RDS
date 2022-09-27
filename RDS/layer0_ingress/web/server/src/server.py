from flask_cors import CORS
from flask import (
    Response,
    stream_with_context,
    session,
    request,
    redirect,
    url_for,
    jsonify,
)
from flask_login import (
    LoginManager,
    login_user,
    UserMixin,
    login_required,
    logout_user,
    current_user,
)
from .app import (
    app,
    socketio,
    user_store,
    use_predefined_user,
    use_embed_mode,
    use_proxy,
    redirect_url,
    trans_tbl,
    domains_dict,
    origins,
    verify_ssl,
)
from .websocket import exchangeCodeData, RDSNamespace
import json
import requests
import uuid
import os
import os
import jwt

CORS(app, origins=origins, supports_credentials=True)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "index"
socketio.on_namespace(RDSNamespace("/"))


def proxy(host, path):
    req = requests.get(f"{host}{path}", stream=True, timeout=1)
    return Response(
        stream_with_context(req.iter_content(chunk_size=1024)),
        content_type=req.headers["content-type"],
    )


class User(UserMixin):
    def to_dict(self):
        return {
            "id": self.id,
            "websocketId": self.websocketId,
            "userId": self.userId,
            "token": self.token,
            "servername": self.servername,
        }

    @classmethod
    def from_dict(cls, obj):
        return cls(**obj)

    def __init__(
        self, servername=None, id=None, userId=None, websocketId=None, token=None
    ):
        super().__init__()
        if id is None:
            raise ValueError("id needs to be set-")

        self.id = id
        self.websocketId = websocketId
        self.userId = userId
        self.token = token
        self.servername = servername

        if use_embed_mode and use_predefined_user:
            return

        if userId is None and token is not None:
            headers = {"Authorization": f"Bearer {token}"}

            for key, domain in domains_dict.items():
                url = domain["ADDRESS"] or os.getenv(
                    "OWNCLOUD_URL", "https://localhost/index.php"
                )

                req = requests.get(
                    f"{url}/index.php/apps/rds/api/1.0/informations",
                    headers=headers,
                    verify=verify_ssl,
                )

                if req.status_code == 200:
                    text = req.json()["jwt"]

                    data = jwt.decode(
                        text, domains_dict.get_publickey(key), algorithms=["RS256"]
                    )
                    app.logger.debug(data)

                    self.userId = data["cloudID"]
                    self.servername = key
                    return

            raise ValueError


@app.route("/informations")
def informations():
    data = {}

    if redirect_url is not None:
        data["redirectUrl"] = redirect_url

    return json.dumps(data)


@app.route("/faq")
def questions():
    from .questions import questions
    from string import Template

    return json.dumps(
        {
            lang: {
                category: {
                    quest: Template(answer).substitute(**(session["oauth"]))
                    for quest, answer in quests.items()
                }
                for category, quests in categories.items()
            }
            for lang, categories in questions.items()
        }
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return ("", 200) if (current_user.is_authenticated) else ("", 401)

    try:
        reqData = request.get_json()
    except Exception as e:
        app.logger.error(e, exc_info=True)
        reqData = request.form
    app.logger.debug("reqdata: {}".format(reqData))

    data = reqData.get("informations", "")
    unverified = jwt.decode(data, options={"verify_signature": False})

    _, _, servername = unverified["cloudID"].rpartition("@")
    servername = servername.translate(trans_tbl)

    publickey = domains_dict.get_publickey(servername)

    user = None
    try:
        decoded = jwt.decode(data, publickey, algorithms=["RS256"])

        user = User(
            id=str(uuid.uuid4()), userId=decoded["cloudID"], servername=servername
        )

        session["informations"] = decoded
        session["servername"] = servername
        session["oauth"] = domains_dict[servername]

        # check if everything is given for later usage
        keys = ["email", "UID", "cloudID"]
        values_from_keys = [decoded.get(key) for key in keys]

        if None in values_from_keys:
            error = {
                "error": "Missing key: email or UID or cloudID is missing in given informations.",
                "errorCode": "MissingKey",
                "key": keys[values_from_keys.index(None)],
            }
            return jsonify(error), 401
    except Exception as e:
        app.logger.error(e, exc_info=True)

    if user is not None:
        user_store[user.get_id()] = user.to_dict()
        login_user(user)
        app.logger.info("logged? {}".format(current_user.is_authenticated))

        return "", 201

    error = {
        "error": "Given informations weren`t valid or some keys were missing.",
        "errorCode": "UserInformationsNotValid",
    }
    app.logger.error("error occured: {}".format(error))
    return jsonify(error), 401


@login_manager.user_loader
def load_user(user_id):
    return User.from_dict(user_store.get(user_id))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/", defaults={"path": "index.html"})
@app.route("/<path:path>")
def index(path):
    # only for testing condition
    if use_embed_mode and use_predefined_user:
        app.logger.debug("skip authentication")
        servername = next(iter(domains_dict.values()))["ADDRESS"]
        user = User(
            id=str(uuid.uuid4()),
            userId=os.getenv("DEV_FLASK_USERID"),
            servername=servername,
        )
        session["servername"] = servername
        session["oauth"] = {
            "SUPPORT_EMAIL": os.getenv("SUPPORT_EMAIL"),
            "MANUAL_URL": os.getenv("MANUAL_URL"),
        }
        session["informations"] = {
            "UID" : "1234",
            "email" : "user@user.com",
            "name" : "someUser" ,
            "cloudID" : "cloud@cloud@localhost:8000"
        }
        user_store[user.get_id()] = user.to_dict()
        login_user(user)

    if "access_token" in request.args:
        user = User(id=str(uuid.uuid4()), token=request.args["access_token"])
        user_store[user.get_id()] = user.to_dict()
        login_user(user)
        return redirect("/")

    if current_user.is_authenticated:
        if "code" in request.args and "state" in request.args:
            if exchangeCodeData(request.args):
                return app.send_static_file("exchangeCode.html")
            return app.send_static_file("exchangeCode_error.html")

    if use_embed_mode or current_user.is_authenticated:
        if use_proxy:
            return proxy(os.getenv("DEV_WEBPACK_DEV_SERVER_HOST"), request.path)

    if use_embed_mode:
        return app.send_static_file(path)

    return redirect(redirect_url)
