
const getDefaultState = () => {
  return {
    userservicelist: [],
    servicelist: [],
    projectlist: [],
    sessionID: null,
    ownCloudServerName: "",
    loadedProject: null,
    supportEmail: null,
    manualUrl: null,
  };
};

export default {
  getDefaultState,
  name: "RDSStore",
  state: getDefaultState(),
  
  getters: {
    getUserServiceList: (state) => state.userservicelist,
    getServiceList: (state) => state.servicelist,
    getProjectlist: (state) => state.projectlist,
    getSessionId: (state) => state.sessionID,
    getOwnCloudServername: (state) => state.ownCloudServerName,
    getLoadedProject: (state) => state.loadedProject,
    getLoadedResearchName: (state) => state.loadedProject["researchname"],
    getLoadedFilePath(state) {
      try {
      return state.loadedProject.portIn[0]["properties"]["customProperties"]["filepath"]}
      catch {
        return null
      }
    },
    getOriginalFilePathForLoadedProject(state) {
      let p =  state.projectlist.filter((i) => i.researchIndex == state.loadedProject.researchIndex)[0]
      try {
      return p.portIn[0]["properties"]["customProperties"]["filepath"]}
      catch {
        return null
      }
    },
    getLoadedPortIn: (state) => state.loadedProject["portIn"],
    getLoadedPortOut: (state) => state.loadedProject["portOut"],
    getLoadedResearchId: (state) => state.loadedProject["researchId"],
    getOriginalResearchNameForLoadedProject(state) {
      let p =  state.projectlist.filter((i) => i.researchIndex == state.loadedProject.researchIndex)[0]
      return p.researchname
    },
    getOriginalPortOutForLoadedProject(state) {
      let p =  state.projectlist.filter((i) => i.researchIndex == state.loadedProject.researchIndex)[0]
      return p["portOut"]
    },
    getOriginalPortInForLoadedProject(state) {
      let p =  state.projectlist.filter((i) => i.researchIndex == state.loadedProject.researchIndex)[0]
      return p.portIn
    },
    getSupportEmail: (state) => state.supportEmail,
    getManualUrl: (state) => state.manualUrl,
  },

  mutations: {
    setUserServiceList: (state, payload) => {
      state.userservicelist = payload.servicelist;
    },
    setServiceList: (state, payload) => {
      state.servicelist = payload.servicelist;
    },
    setProjectList: (state, payload) => {
      state.projectlist = payload.projectlist;
    },
    setSessionId: (state, payload) => {
      state.sessionID = payload.sessionID;
    },
    resetState(state) {
      Object.assign(state, getDefaultState());
    },
    setOwnCloudServername(state, payload) {
      // this resets the state, if serverName is different as before
      // fixes https://github.com/Sciebo-RDS/Sciebo-RDS/issues/183
      if (state.ownCloudServerName !== payload.serverName) {
        Object.assign(state, getDefaultState());
      }
      state.ownCloudServerName = payload.serverName;
    },
    setLoadedProject(state, payload) {
        state.loadedProject = {...payload, researchname: (payload.researchname ? payload.researchname : "")};
      },
    setLoadedResearchName: (state, payload) => {
      state.loadedProject["researchname"] = payload;
    },
    setLoadedFilePath: (state, payload) => {
      if (!state.loadedProject) {
        return
      }
      // extend this in case of multiple inPorts.
      if (state.loadedProject.portIn.length == 0) {
        console.log("state.loadedProject.portIn.length == 0")
        state.loadedProject.portIn.push({"properties": {"customProperties": {"filepath": payload}, "type" : ['fileStorage']}, "port": "port-owncloud-" + state.getOwnCloudServername})
      } else if (state.loadedProject.portIn.length == 1) {
        console.log("state.loadedProject.portIn.length == 1")
        state.loadedProject.portIn[0].properties.customProperties["filepath"] = payload
      }

    },
    setLoadedPortIn: (state, payload) => {
      state.loadedProject["portIn"] = payload;
    },
    setLoadedPortOut: (state, payload) => {
      state.loadedProject["portOut"] = payload;
    },
    resetLoadedProject(state) {
      state.loadedProject = null;
    },
    setSupportEmail: (state, payload) => {
      state.supportEmail = payload.supportEmail;
    },
    setManualUrl: (state, payload) => {
      state.manualUrl = payload.manualUrl;
    },
  },
  actions: {
    SOCKET_SupportEmail(context, state) {
      context.commit("setSupportEmail", {
        supportEmail: state.supportEmail,
      });
    },
    SOCKET_ManualUrl(context, state) {
      context.commit("setManualUrl", {
        manualUrl: state.manualUrl,
      });
    },
    SOCKET_ServerName(context, state) {
      context.commit("setOwnCloudServername", {
        serverName: state.servername,
      });
    },
    SOCKET_UserServiceList(context, state) {
      let servicelist = [];
      try {
        servicelist = JSON.parse(state).list.map((el) => el.informations);
      } catch (error) {
        console.log("UserServiceList is invalid: ", error, "state: ", state);
      }
      context.commit("setUserServiceList", {
        servicelist,
      });
    },
    SOCKET_ServiceList(context, state) {
      let servicelist = [];
      try {
        servicelist = JSON.parse(state).map((el) => {
          el.informations.state = el.jwt;
          return el.informations;
        });
      } catch (error) {
        console.log("ServiceList is invalid: ", error, "state: ", state);
      }
      context.commit("setServiceList", {
        servicelist,
      });
    },
    SOCKET_ProjectList(context, state) {
      let projectlist = [];
      try {
        projectlist = JSON.parse(state);
      } catch (error) {
        console.log("ProjectList is invalid: ", error, "state: ", state);
      }
      context.commit("setProjectList", {
        projectlist,
      });
    },
    SOCKET_SessionId(context, state) {
      console.log("got describo sessionId: ", state);
      context.commit("setSessionId", {
        sessionID: state,
      });
    },
    requestSessionId(context) {
      this._vm.$socket.client.emit("requestSessionId", (sessionId) => {
        console.log("got describo sessionId: ", sessionId);
        context.commit("setSessionId", {
          sessionID: sessionId,
        });
      });
    },
    setLocation(context, data) {
      // TODO get and remove port-owncloud first and add it with new location!
      const location = data.filePath;
      const projectId = data.projectId;
      this._vm.$socket.client.emit("setLocation", data);
    },
    createProject() {
      this._vm.$socket.client.emit("createResearch");
    },
    saveProject(context, data) {
      data.researchIndex = data.id;
      this._vm.$socket.client.emit("saveResearch", data);
    },
    removeProject(context, data) {
      data.researchIndex = data.id;
      this._vm.$socket.client.emit("removeResearch", data);
    },
    changePorts(context, data) {
      this._vm.$socket.client.emit("changePorts", JSON.stringify(data));
    },
    changeResearchname(context, data) {
      this._vm.$socket.client.emit("changeResearchname", JSON.stringify(data));
      this.dispatch("requestProjectList");
    },
    triggerSynchronization(context, data, fn) {
      console.log("trigger sync data: ", data);
      this._vm.$socket.client.emit(
        "triggerSynchronization",
        JSON.stringify(data),
        (response) => {
          console.log("got response: ", response);
          fn(response);
        }
      );
    },
    requestUserServiceList(context) {
      this._vm.$socket.client.emit("getUserServices", (response) => {
        context.dispatch("SOCKET_UserServiceList", response);
      });
    },
    requestServiceList(context) {
      this._vm.$socket.client.emit("getServicesList", (response) => {
        context.dispatch("SOCKET_ServiceList", response);
      });
    },
    requestProjectList(context) {
      this._vm.$socket.client.emit("getAllResearch", (response) => {
        context.dispatch("SOCKET_ProjectList", response);
      });
    },
    exchangeCode(context, data) {
      if (!!data.code && !!data.state) {
        this._vm.$socket.client.emit(
          "exchangeCode",
          JSON.stringify(data),
          (response) => {
            console.log("exchangeCode response", response);
          }
        );
      }
    },
    addServiceWithCredentials(context, service) {
      this._vm.$socket.client.emit(
        "addCredentials",
        JSON.stringify(service),
        (response) => {
          console.log("credentials response", response);
        }
      );
    },
    removeService(context, service) {
      this._vm.$socket.client.emit(
        "removeServiceForUser",
        JSON.stringify(service)
      );
    },
  },
};
