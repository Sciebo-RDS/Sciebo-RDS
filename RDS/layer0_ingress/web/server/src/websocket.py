from flask import request
from flask_socketio import emit, disconnect, Namespace
from flask_login import current_user, logout_user
from .Util import parseResearch, parseResearchBack, parsePortBack, removeDuplicates, checkForEmpty
from .EasierRDS import parseDict
from .app import socketio, clients, rc, tracing, tracer_obj, app
from .Describo import getSessionId
import logging
import functools
import os
import json
import requests
import jwt


def refreshUserServices():
    emit("UserServiceList", httpManager.makeRequest("getUserServices"))


def refreshProjects():
    emit("ProjectList", httpManager.makeRequest("getAllResearch"))


url = os.getenv("RDS_INSTALLATION_DOMAIN")

data = {
    os.getenv("USE_CASE_SERVICE_PORT_SERVICE", f"{url}/port-service"): [
        ("getUserServices", "{url}/user/{userId}/service"),
        ("getServicesList", "{url}/service", "get", None, removeDuplicates),
        ("getService", "{url}/service/{servicename}"),
        ("getServiceForUser", "{url}/user/{userId}/service/{servicename}"),
        ("removeServiceForUser",
         "{url}/user/{userId}/service/{servicename}", "delete", None, refreshUserServices),
        ("createProject",
         "{url}/user/{userId}/service/{servicename}/projects", "post"),
    ],
    os.getenv("USE_CASE_SERVICE_EXPORTER_SERVICE", f"{url}/exporter"): [
        ("getAllFiles", "{url}/user/{userId}/research/{researchIndex}"),
        ("triggerFileSynchronization",
         "{url}/user/{userId}/research/{researchIndex}", "post"),
        ("removeAllFiles",
         "{url}/user/{userId}/research/{researchIndex}", "delete")
    ],
    os.getenv("CENTRAL_SERVICE_RESEARCH_MANAGER", f"{url}/research"): [
        ("getAllResearch", "{url}/user/{userId}",
         "get", None, checkForEmpty, True),
        ("getResearch",
         "{url}/user/{userId}/research/{researchIndex}", "get", None, parseResearch),
        ("createResearch", "{url}/user/{userId}",
         "post", None, refreshProjects),
        ("removeAllResearch", "{url}/user/{userId}",
         "delete", None, refreshProjects),
        ("removeResearch",
         "{url}/user/{userId}/research/{researchIndex}", "delete", None, refreshProjects),
        ("addImport",
         "{url}/user/{userId}/research/{researchIndex}/imports", "post", parsePortBack),
        ("addExport",
         "{url}/user/{userId}/research/{researchIndex}/exports", "post", parsePortBack),
        ("removeImport",
         "{url}/user/{userId}/research/{researchIndex}/imports/{portId}", "delete"),
        ("removeExport",
         "{url}/user/{userId}/research/{researchIndex}/exports/{portId}", "delete")
    ],
    os.getenv("USE_CASE_SERVICE_METADATA_SERVICE", f"{url}/metadata"): [
        ("finishResearch",
         "{url}/user/{userId}/research/{researchIndex}", "put", None, refreshProjects),
        ("triggerMetadataSynchronization",
         "{url}/user/{userId}/research/{researchIndex}", "patch")
    ]
}

httpManager = parseDict(data, socketio=socketio)


def exchangeCodeData(data):
    body = {
        'servicename': "port-owncloud",
        'code': data["code"],
        'state': data["state"],
        "userId": current_user.userId
    }

    # TODO exchange it in the background for user and redirect to wizard / projects

    jwtEncode = jwt.encode(body, os.getenv(
        "OWNCLOUD_OAUTH_CLIENT_SECRET"), algorithm="HS256")

    urlPort = os.getenv("USE_CASE_SERVICE_PORT_SERVICE", f"{url}/port-service")

    req = requests.post(f"{urlPort}/exchange", json={"jwt": jwtEncode},
                        verify=os.getenv("VERIFY_SSL", "False") == "True")
    app.logger.debug(req.text)

    return req.status_code < 400


def trace_this(fn):
    @functools.wraps(fn)
    def wrapped(*args, **kwargs):
        with tracer_obj.start_active_span(f'Websocket {fn.__name__}') as scope:
            app.logger.debug("start tracer span")
            res = fn(*args, **kwargs)
            app.logger.debug("finish tracer span")
            return res

    return wrapped


def authenticated_only(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        app.logger.debug("logged? {}, {}, {}".format(
            current_user.is_authenticated, args, kwargs))

        emit("LoginStatus", json.dumps({
            "status": current_user.is_authenticated,
            "user": current_user.userId
        }))

        if not current_user.is_authenticated:
            disconnect()
        else:
            fn = trace_this(f)
            return fn(*args, **kwargs)

    return wrapped


def saveResearch(research):
    researchUrl = "{}/user/{}/research/{}".format(
        os.getenv("CENTRAL_SERVICE_RESEARCH_MANAGER", f"{url}/research"),
        research["userId"],
        research["researchIndex"]
    )

    try:
        for portUrl, portType in {"imports": "portIn", "exports": "portOut"}.items():
            for port in research[portType]:
                req = requests.post(f"{researchUrl}/{portUrl}", json=port,
                                    verify=os.getenv("VERIFY_SSL", "False") == "True")
                app.logger.debug("sent port: {}, status code: {}".format(
                    port, req.status_code
                ))

        return True
    except Exception as e:
        app.logger.error("Error: {}".format(e), exc_info=True)
        return False


class RDSNamespace(Namespace):
    @authenticated_only
    def on_connect(self, data):
        current_user.websocketId = request.sid
        clients[current_user.userId] = current_user

        emit("ServiceList", httpManager.makeRequest("getServicesList"))
        emit("UserServiceList", httpManager.makeRequest("getUserServices"))
        emit("ProjectList", httpManager.makeRequest("getAllResearch"))

    def on_disconnect(self):
        app.logger.info("disconnected")

        try:
            app.logger.debug("LOGOUT")
            # logout_user()
            del clients[current_user.userId]
        except Exception as e:
            app.logger.error(e, exc_info=True)

    @authenticated_only
    def on_triggerSynchronization(self, jsonData):
        try:
            app.logger.debug("trigger synch, data: {}".format(jsonData))

            research = json.loads(httpManager.makeRequest(
                "getResearch", data=jsonData))

            app.logger.debug(
                "start synchronization, research: {}".format(research))

            for index, port in enumerate(research["portOut"]):
                parsedBackPort = parsePortBack(port)
                parsedBackPort["servicename"] = port["port"]

                try:
                    createProjectResp = json.loads(httpManager.makeRequest(
                        "createProject", data=parsedBackPort))

                    app.logger.debug(
                        "got response: {}".format(createProjectResp))

                    if "customProperties" not in research["portOut"][index]:
                        research["portOut"][index]["properties"]["customProperties"] = {}

                    research["portOut"][index]["properties"]["customProperties"].update(
                        createProjectResp
                    )
                except:
                    app.logger.debug("no project were created for {}".format(
                        parsedBackPort["servicename"]))

            app.logger.debug("research before: {}, \nafter: {}".format(
                research, parseResearchBack(research)))
            saveResearch(parseResearchBack(research))

            try:
                httpManager.makeRequest(
                    "triggerMetadataSynchronization", data=jsonData)
            except:
                app.logger.debug(
                    "project does not support metadata sync for data {}".format(jsonData))

            httpManager.makeRequest(
                "triggerFileSynchronization", data=jsonData)
            httpManager.makeRequest("finishResearch", data=jsonData)

            # refresh projectlist for user
            emit("ProjectList", httpManager.makeRequest("getAllResearch"))

            app.logger.debug(
                "done synchronization, research: {}".format(research))

            return True

        except Exception as e:
            app.logger.error(f"error in sync: {e}", exc_info=True)
            return False

    @authenticated_only
    def on_addCredentials(self, jsonData):
        jsonData = json.loads(jsonData)

        body = {
            "servicename": jsonData["servicename"],
            "username": jsonData["username"],
            "password": jsonData["password"],
            "userId": current_user.userId
        }

        if not body["username"]:
            body["username"] = "---"

        urlPort = os.getenv("USE_CASE_SERVICE_PORT_SERVICE",
                            f"{url}/port-service")
        req = requests.post(f"{urlPort}/credentials", json=body,
                            verify=os.getenv("VERIFY_SSL", "False") == "True")
        app.logger.debug(req.text)

        # update userserviceslist on client
        emit("UserServiceList", httpManager.makeRequest("getUserServices"))

        return req.status_code < 300

    @authenticated_only
    def on_exchangeCode(self, jsonData):
        jsonData = json.loads(jsonData)

        req = exchangeCodeData(jsonData)
        app.logger.debug(req.text)

        # update userserviceslist on client
        emit("UserServiceList", httpManager.makeRequest("getUserServices"))

        return req.status_code < 300

    @authenticated_only
    def on_changeResearchname(self, jsonData):
        if jsonData is None:
            return

        jsonData = json.loads(jsonData)
        researchIndex = jsonData["researchIndex"]
        user = current_user.userId
        urlResearch = os.getenv(
            "CENTRAL_SERVICE_RESEARCH_MANAGER", f"{url}/research")

        requests.put(
            f"{urlResearch}/user/{user}/research/{researchIndex}/researchname",
            json={"researchname": jsonData["researchname"]},
            verify=os.getenv("VERIFY_SSL", "False") == "True"
        )

    @authenticated_only
    def on_changePorts(self, jsonData):
        """
        return {
            researchIndex: researchIndex,
            import: {
                add: [{name: "port-owncloud", filepath:"/photosForschung/"}],
            },
            export: {
                add: [{name: "port-zenodo"} ],
                remove: ["port-reva", "port-osf"],
                change: [{name: "port-owncloud", filepath:"/photosForschung/"},
                    {name: "port-zenodo", projectId:"12345"}]
            }
        }"""
        if jsonData is None:
            return

        jsonData = json.loads(jsonData)
        researchIndex = jsonData["researchIndex"]

        user = current_user.userId
        urlResearch = os.getenv(
            "CENTRAL_SERVICE_RESEARCH_MANAGER", f"{url}/research")

        def transformPorts(portList):
            data = []
            for port in portList:
                obj = {
                    "port": port["servicename"],
                    "properties": []
                }

                if "filepath" in port:
                    obj["properties"].append(
                        {
                            "portType": "fileStorage",
                            "value": True
                        }
                    )
                    obj["properties"].append({
                        "portType": "customProperties",
                        "value": [{
                            "key": "filepath",
                            "value": port["filepath"]
                        }]
                    })
                else:
                    obj["properties"].append(
                        {
                            "portType": "metadata",
                            "value": True
                        }
                    )

                if "projectId" in port:
                    obj["properties"].append({
                        "portType": "customProperties",
                        "value": [{
                            "key": "projectId",
                            "value": port["projectId"]
                        }]
                    })
                data.append(obj)
            app.logger.debug(f"transform data: {data}")
            return data

        crossPort = {
            "import": "imports",
            "export": "exports"
        }

        for portOutLeft, portOutRight in crossPort.items():
            for method in ["add", "change"]:
                for port in transformPorts(jsonData[portOutLeft][method]):
                    requests.post(
                        f"{urlResearch}/user/{user}/research/{researchIndex}/{portOutRight}",
                        json=port,
                        verify=os.getenv("VERIFY_SSL", "False") == "True"
                    )

        def getIdPortListForRemoval(portList):
            """Get Id Port list
            Works only with remove command.
            """
            retPortList = []
            for portType in crossPort.values():
                ports = requests.get(
                    f"{urlResearch}/user/{user}/research/{researchIndex}/{portType}",
                    verify=os.getenv("VERIFY_SSL", "False") == "True").json()
                for index, port in enumerate(ports):
                    for givenPort in portList:
                        if port["port"] == givenPort["servicename"]:
                            retPortList.append((portType, index))
                            break
            return retPortList

        for t in crossPort.keys():
            for portType, portId in getIdPortListForRemoval(jsonData[t]["remove"]):
                app.logger.debug(f"type: {portType}, id: {portId}")
                requests.delete(
                    f"{urlResearch}/user/{user}/research/{researchIndex}/{portType}/{portId}",
                    verify=os.getenv("VERIFY_SSL", "False") == "True")

        emit("ProjectList", httpManager.makeRequest("getAllResearch"))

    def on_requestSessionId(self, jsonData=None):
        global rc
        if jsonData is None:
            jsonData = {}

        sessionId = None

        try:
            token = json.loads(httpManager.makeRequest(
                "getServiceForUser", {
                    "servicename": "port-owncloud"
                }
            ))["data"]["access_token"]
            describoObj = getSessionId(token, jsonData.get("folder"))
            sessionId = describoObj["sessionId"]

            app.logger.debug(f"send sessionId: {sessionId}")

            emit("SessionId", sessionId)
        except Exception as e:
            app.logger.error(e, exc_info=True)

        try:
            app.logger.debug("try to save sessionId in redis")
            rc.set(current_user.userId, json.dumps(describoObj))
        except Exception as e:
            app.logger.debug("saving sessionId in redis gone wrong")
            app.logger.error(e, exc_info=True)

        app.logger.debug(f"return sessionId: {sessionId}")
        return sessionId
