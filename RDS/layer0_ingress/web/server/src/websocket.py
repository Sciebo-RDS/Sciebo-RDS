import enum
from time import time
from flask import request, session
from flask_socketio import emit, disconnect, Namespace
from flask_login import current_user, logout_user
from .Util import (
    parseResearch,
    parseResearchBack,
    parsePortBack,
    removeDuplicates,
    checkForEmpty,
    applyFilters,
    isServiceInLastServicelist,
)
from .EasierRDS import parseDict
from .app import (
    socketio,
    clients,
    rc,
    app,
    trans_tbl,
    research_progress,
    verify_ssl,
    timestamps
)
from .Describo import getSessionId
import logging
import functools
import os
import json
import requests
import jwt
from .SyncResearchProcessStatusEnum import ProcessStatus



def refreshUserServices():
    emit("UserServiceList", httpManager.makeRequest("getUserServices"))


def refreshProjects():
    emit("ProjectList", httpManager.makeRequest("getAllResearch"))


url = os.getenv("RDS_INSTALLATION_DOMAIN")

data = {
    os.getenv("USE_CASE_SERVICE_PORT_SERVICE", f"{url}/port-service"): [
        ("getUserServices", "{url}/user/{userId}/service"),
        (
            "getServicesList",
            "{url}/service",
            "get",
            None,
            lambda x: applyFilters(removeDuplicates(x)),
        ),
        ("getService", "{url}/service/{servicename}"),
        ("getServiceForUser", "{url}/user/{userId}/service/{servicename}"),
        (
            "removeServiceForUser",
            "{url}/user/{userId}/service/{servicename}",
            "delete",
            None,
            refreshUserServices,
        ),
        ("createProject", "{url}/user/{userId}/service/{servicename}/projects", "post"),
    ],
    os.getenv("USE_CASE_SERVICE_EXPORTER_SERVICE", f"{url}/exporter"): [
        ("getAllFiles", "{url}/user/{userId}/research/{researchIndex}"),
        (
            "triggerFileSynchronization",
            "{url}/user/{userId}/research/{researchIndex}",
            "post",
        ),
        ("removeAllFiles", "{url}/user/{userId}/research/{researchIndex}", "delete"),
    ],
    os.getenv("CENTRAL_SERVICE_RESEARCH_MANAGER", f"{url}/research"): [
        ("getAllResearch", "{url}/user/{userId}", "get", None, checkForEmpty, True),
        (
            "getResearch",
            "{url}/user/{userId}/research/{researchIndex}",
            "get",
            None,
            parseResearch,
        ),
        ("createResearch", "{url}/user/{userId}", "post", None, refreshProjects),
        ("removeAllResearch", "{url}/user/{userId}", "delete", None, refreshProjects),
        (
            "removeResearch",
            "{url}/user/{userId}/research/{researchIndex}",
            "delete",
            None,
            refreshProjects,
        ),
        (
            "addImport",
            "{url}/user/{userId}/research/{researchIndex}/imports",
            "post",
            parsePortBack,
        ),
        (
            "addExport",
            "{url}/user/{userId}/research/{researchIndex}/exports",
            "post",
            parsePortBack,
        ),
        (
            "removeImport",
            "{url}/user/{userId}/research/{researchIndex}/imports/{portId}",
            "delete",
        ),
        (
            "removeExport",
            "{url}/user/{userId}/research/{researchIndex}/exports/{portId}",
            "delete",
        ),
    ],
    os.getenv("USE_CASE_SERVICE_METADATA_SERVICE", f"{url}/metadata"): [
        (
            "finishResearch",
            "{url}/user/{userId}/research/{researchIndex}",
            "put",
            None,
            refreshProjects,
        ),
        (
            "triggerMetadataSynchronization",
            "{url}/user/{userId}/research/{researchIndex}",
            "patch",
        ),
    ],
}

httpManager = parseDict(data, socketio=socketio)


def exchangeCodeData(data):

    # check if service was in latest servicelist, because otherwise we have a sideways request.
    # this is okay, because if the state is invalid, exchange will be failed nevertheless.
    # So if we accept here a service from a malicious state data, it will be declined by port service.
    try:
        servicename = jwt.decode(
            data["state"], algorithms="HS256", options={"verify_signature": False}
        )["servicename"]
        result = isServiceInLastServicelist(servicename)

        app.logger.debug(
            "Is servicename in servicelist:\n service: {}\n: result: {}".format(
                servicename, result
            )
        )
        if not result:
            return False
    except (jwt.ExpiredSignatureError, KeyError) as e:
        app.logger.error(e, exc_info=True)
        return False

    body = {
        "servicename": "port-owncloud-{}".format(session["servername"]),
        "code": data["code"],
        "state": data["state"],
        "userId": current_user.userId,
    }

    oauth_secret = session["oauth"].get("OAUTH_CLIENT_SECRET") or os.getenv(
        "OWNCLOUD_OAUTH_CLIENT_SECRET"
    )
    jwtEncode = jwt.encode(body, oauth_secret, algorithm="HS256")

    urlPort = os.getenv("USE_CASE_SERVICE_PORT_SERVICE", f"{url}/port-service")

    req = requests.post(
        f"{urlPort}/exchange",
        json={"jwt": jwtEncode},
        verify=verify_ssl,
    )
    app.logger.debug(req.text)

    return req.status_code < 400



def authenticated_only(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        app.logger.debug(
            "logged? {}, {}, {}".format(current_user.is_authenticated, args, kwargs)
        )

        emit(
            "LoginStatus",
            json.dumps(
                {"status": current_user.is_authenticated, "user": current_user.userId}
            ),
        )

        if not current_user.is_authenticated:
            disconnect()
        else:
            return f(*args, **kwargs)

    return wrapped


def saveResearch(research):
    researchUrl = "{}/user/{}/research/{}".format(
        os.getenv("CENTRAL_SERVICE_RESEARCH_MANAGER", f"{url}/research"),
        research["userId"],
        research["researchIndex"],
    )

    try:
        for portUrl, portType in {"imports": "portIn", "exports": "portOut"}.items():
            for port in research[portType]:
                req = requests.post(
                    f"{researchUrl}/{portUrl}",
                    json=port,
                    verify=verify_ssl,
                )
                app.logger.debug(
                    "sent port: {}, status code: {}".format(port, req.status_code)
                )

        return True
    except Exception as e:
        app.logger.error("Error: {}".format(e), exc_info=True)
        return False


class RDSNamespace(Namespace):
    @authenticated_only
    def on_connect(self, data):
        current_user.websocketId = request.sid
        clients[current_user.userId] = current_user
        
        sideInformations = session["oauth"]
        app.logger.debug("set side-informations {}".format(sideInformations))

        emit("ServerName", {"servername": session["servername"]})
        emit("SupportEmail", {"supportEmail": session["oauth"]["SUPPORT_EMAIL"]})
        emit("ManualUrl", {"manualUrl": session["oauth"]["MANUAL_URL"]})
        emit("ServiceList", httpManager.makeRequest("getServicesList"))
        emit("UserServiceList", httpManager.makeRequest("getUserServices"))
        emit("ProjectList", httpManager.makeRequest("getAllResearch"))

        timestamps[current_user.userId] = time()

    def on_disconnect(self):
        app.logger.info("disconnected")

        try:
            app.logger.debug("LOGOUT")
            # logout_user()
            del clients[current_user.userId]
        except Exception as e:
            app.logger.error(e, exc_info=True)

    def __update_research_process(self, research):
        research_progress[research["researchId"]] = research

    def __get_research_process(self, research):
        return research_progress.get(research["researchId"])

    def __delete_research(self, research):
        del research_progress[research["researchId"]]

    @authenticated_only
    def on_triggerSynchronization(self, jsonData):
        try:
            app.logger.debug("trigger synch, data: {}".format(jsonData))

            research = self.__load_research(jsonData)
            research = self.__reload_research_status(research)
            self.__update_research_process(research)

            app.logger.debug(
                "start synchronization\nresearch before: {}".format(research)
            )
            projectId = self.__trigger_project_creation(research)
            emit("projectCreatedInService", {
                "researchIndex": jsonData["researchIndex"],
                "projectId": projectId
            })

            app.logger.debug("research after: {}".format(parseResearchBack(research)))

            saveResearch(parseResearchBack(research))

            metadataSynced = self.__trigger_metadatasync(jsonData, research)
            emit("metadataSynced", {
                "researchIndex": jsonData["researchIndex"],
                "metadataSynced": metadataSynced
            })

            fileUploadStatus = self.__trigger_filesync(jsonData, research)
            if type(fileUploadStatus) is dict:
                fileUploadStatus["researchIndex"] = jsonData["researchIndex"]
            emit("FileUploadStatus", fileUploadStatus)

            if (
                research["synchronization_process_status"]
                == ProcessStatus.FILEDATA_SYNCHRONIZED.value
            ):
                self.__trigger_finish_sync(jsonData, research)
                app.logger.debug("done synchronization, research: {}".format(research))

                return True # fileUploadStatus["success"]
        except Exception as e:
            app.logger.error(f"error in sync: {e}", exc_info=True)

        return False

    def __load_research(self, jsonData):
        research = json.loads(httpManager.makeRequest("getResearch", data=jsonData))
        research["synchronization_process_status"] = ProcessStatus.START.value

        for index, port in enumerate(research["portOut"]):
            research["portOut"][index]["status"] = ProcessStatus.START.value
        return research

    def __reload_research_status(self, research):
        tmp_research = self.__get_research_process(research)
        if tmp_research is not None:
            return tmp_research
        return research

    def __trigger_finish_sync(self, jsonData, research, index=0):
        identifier = json.loads(
            httpManager.makeRequest("finishResearch", data=jsonData)
        )

        app.logger.debug("got response from __trigger_finish_sync: Type: {}, payload: {}".format(type(identifier), identifier))

        if "customProperties" not in research["portOut"][index]:
            research["portOut"][index]["properties"]["customProperties"] = {}

        if identifier is not None:
            research["portOut"][index]["properties"]["customProperties"].update(
                identifier
            )

        research["synchronization_process_status"] = ProcessStatus.FINISHED.value
        self.__update_research_process(research)
        self.__delete_research(research)

        # refresh projectlist for user
        emit("ProjectList", httpManager.makeRequest("getAllResearch"))

    def __trigger_project_creation(self, research):
        for index, port in enumerate(research["portOut"]):
            if port["status"] != ProcessStatus.START.value:
                continue

            projectId = self.__trigger_project_creation_for_port(research, index, port)

            return projectId

    def __trigger_project_creation_for_port(self, research, index, port):
        parsedBackPort = parsePortBack(port)
        parsedBackPort["servicename"] = port["port"]

        try:
            createProjectResp = json.loads(
                httpManager.makeRequest("createProject", data=parsedBackPort)
            )

            app.logger.debug("got response: {}".format(createProjectResp))

            if "customProperties" not in research["portOut"][index]:
                research["portOut"][index]["properties"]["customProperties"] = {}

            research["portOut"][index]["properties"]["customProperties"].update(
                createProjectResp
            )

            research["portOut"][index]["status"] = ProcessStatus.PROJECT_CREATED.value
            self.__update_research_process(research)

            if "projectId" in createProjectResp:
                return createProjectResp["projectId"]
        
        except:
            app.logger.debug(
                "no project were created for {}".format(parsedBackPort["servicename"])
            )

    def __trigger_metadatasync(self, jsonData, research):
        try:
            if research["synchronization_process_status"] == ProcessStatus.START.value:
                httpManager.makeRequest("triggerMetadataSynchronization", data=jsonData)

                research[
                    "synchronization_process_status"
                ] = ProcessStatus.METADATA_SYNCHRONIZED.value
                self.__update_research_process(research)
                return True
            
            return False
        except:
            app.logger.debug(
                "project does not support metadata sync for data {}".format(jsonData)
            )
            return False

    def __trigger_filesync(self, jsonData, research):
        if (
            research["synchronization_process_status"]
            == ProcessStatus.METADATA_SYNCHRONIZED.value
        ):
            result = httpManager.makeRequest("triggerFileSynchronization", data=jsonData)
            if result[0]:
                research[
                    "synchronization_process_status"
                ] = ProcessStatus.FILEDATA_SYNCHRONIZED.value
                self.__update_research_process(research)
            return result
        
        return False, ["Something unexpected happened"]

    @authenticated_only
    def on_addCredentials(self, jsonData):
        jsonData = json.loads(jsonData)

        body = {
            "servicename": jsonData["servicename"],
            "username": jsonData["username"],
            "password": jsonData["password"],
            "userId": current_user.userId,
        }

        if not body["username"]:
            body["username"] = "---"

        urlPort = os.getenv("USE_CASE_SERVICE_PORT_SERVICE", f"{url}/port-service")
        req = requests.post(
            f"{urlPort}/credentials",
            json=body,
            verify=verify_ssl,
        )
        app.logger.debug(req.text)

        # update userserviceslist on client
        emit("UserServiceList", httpManager.makeRequest("getUserServices"))

        return req.status_code < 300

    @authenticated_only
    def on_exchangeCode(self, jsonData):
        jsonData = json.loads(jsonData)

        req = exchangeCodeData(jsonData)
        app.logger.debug("exchange code result: {}".format(req.text))

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
        urlResearch = os.getenv("CENTRAL_SERVICE_RESEARCH_MANAGER", f"{url}/research")

        requests.put(
            f"{urlResearch}/user/{user}/research/{researchIndex}/researchname",
            json={"researchname": jsonData["researchname"]},
            verify=verify_ssl,
        )

    @authenticated_only
    def on_changePorts(self, jsonData):
        """
        return {
            researchIndex: researchIndex,
            import: {
                add: [{servicename: "port-owncloud", filepath:"/photosForschung/"}],
            },
            export: {
                add: [{servicename: "port-zenodo"} ],
                remove: [{servicename: "port-reva"}, {servicename: "port-osf"}],
                change: [{name: "port-owncloud", filepath:"/photosForschung/"},
                    {name: "port-zenodo", projectId:"12345"}]
            }
        }"""
        if jsonData is None:
            return

        jsonData = json.loads(jsonData)
        researchIndex = jsonData["researchIndex"]

        user = current_user.userId
        urlResearch = os.getenv("CENTRAL_SERVICE_RESEARCH_MANAGER", f"{url}/research")

        def transformPorts(portList):
            data = []
            for port in portList:
                obj = {"port": port["servicename"], "properties": []}

                if "filepath" in port:
                    obj["properties"].append({"portType": "fileStorage", "value": True})
                    obj["properties"].append(
                        {
                            "portType": "customProperties",
                            "value": [{"key": "filepath", "value": port["filepath"]}],
                        }
                    )
                else:
                    obj["properties"].append({"portType": "metadata", "value": True})

                if "projectId" in port:
                    obj["properties"].append(
                        {
                            "portType": "customProperties",
                            "value": [{"key": "projectId", "value": port["projectId"]}],
                        }
                    )
                data.append(obj)
            app.logger.debug(f"transform data: {data}")
            return data

        crossPort = {"import": "imports", "export": "exports"}

        for portOutLeft, portOutRight in crossPort.items():
            for method in ["add", "change"]:
                for port in transformPorts(jsonData[portOutLeft][method]):
                    requests.post(
                        f"{urlResearch}/user/{user}/research/{researchIndex}/{portOutRight}",
                        json=port,
                        verify=verify_ssl,
                    )

        def getIdPortListForRemoval(portList):
            """Get Id Port list
            Works only with remove command.
            """
            retPortList = []
            for portType in crossPort.values():
                ports = requests.get(
                    f"{urlResearch}/user/{user}/research/{researchIndex}/{portType}",
                    verify=verify_ssl,
                ).json()
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
                    verify=verify_ssl,
                )

        emit("ProjectList", httpManager.makeRequest("getAllResearch"))

    def on_requestSessionId(self, jsonData=None):
        app.logger.debug("got request for describo sessionId, data: {}", jsonData)
        
        global rc
        if jsonData is None:
            jsonData = {}

        sessionId = None

        try:
            informations = session["informations"]
            _, _, servername = str(informations.get("cloudID")).rpartition("@")
            servername = servername.translate(trans_tbl)
            app.logger.debug("go to take token from tokenstore")

            token = json.loads(
                httpManager.makeRequest(
                    "getServiceForUser", {"servicename": f"port-owncloud-{servername}"}
                )
            )["data"]["access_token"]
            
            app.logger.debug("got token")
            describoObj = getSessionId(token, folder=jsonData.get("folder"), metadataProfile=jsonData.get("metadataProfile"))
            sessionId = describoObj["sessionId"]

            app.logger.debug(f"send sessionId: {sessionId}")

            emit("SessionId", sessionId)
            try:
                app.logger.debug("try to save sessionId in redis")
                rc.set(current_user.userId, json.dumps(describoObj))
            except Exception as e:
                app.logger.debug("saving sessionId in redis gone wrong")
                app.logger.error(e, exc_info=True)
        except Exception as e:
            app.logger.error(e, exc_info=True)

        app.logger.debug(f"return sessionId: {sessionId}")
        return sessionId
