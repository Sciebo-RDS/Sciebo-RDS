const getDefaultState = () => {
    return {
        userservicelist: [],
        servicelist: [],
        projectlist: [],
        sessionID: null
    }
}

export default {
    getDefaultState,
    name: "RDSStore",
    state: getDefaultState(),
    getters: {
        getUserServiceList: (state) => state.userservicelist,
        getServiceList: (state) => state.servicelist,
        getProjectlist: (state) => state.projectlist,
        getSessionId: (state) => state.sessionID
    },
    mutations: {
        setUserServiceList: (state, payload) => { state.userservicelist = payload.servicelist },
        setServiceList: (state, payload) => { state.servicelist = payload.servicelist },
        setProjectList: (state, payload) => { state.projectlist = payload.projectlist },
        setSessionId: (state, payload) => { state.sessionID = payload.sessionID },
        resetState(state) {
            Object.assign(state, getDefaultState())
        },
    },
    actions: {
        SOCKET_UserServiceList(context, state) {
            let servicelist = []
            try {
                servicelist = JSON.parse(state).list.map(el => el.informations)
            } catch (error) {
                console.log("UserServiceList is invalid: ", error, "state: ", state)
            }
            context.commit('setUserServiceList', {
                servicelist
            })
        },
        SOCKET_ServiceList(context, state) {
            let servicelist = []
            try {
                servicelist = JSON.parse(state).map(el => {
                    el.informations.state = el.jwt
                    return el.informations
                })
            } catch (error) {
                console.log("ServiceList is invalid: ", error, "state: ", state)
            }
            context.commit('setServiceList', {
                servicelist
            })
        },
        SOCKET_ProjectList(context, state) {
            let projectlist = []
            try {
                projectlist = JSON.parse(state)
            } catch (error) {
                console.log("ProjectList is invalid: ", error, "state: ", state)
            }
            context.commit('setProjectList', {
                projectlist
            })
        },
        SOCKET_SessionId(context, state) {
            console.log("got describo sessionId: ", state)
            context.commit('setSessionId', {
                sessionID: state
            })
        },
        requestSessionId(context) {
            this._vm.$socket.client.emit("requestSessionId", (sessionId) => {
                console.log("got describo sessionId: ", sessionId)
                context.commit('setSessionId', {
                    sessionID: sessionId
                })
            })
        },
        setLocation(context, data) {
            // TODO get and remove port-owncloud first and add it with new location!
            const location = data.filePath
            const projectId = data.projectId
            this._vm.$socket.client.emit("setLocation", data);
        },
        createProject() {
            this._vm.$socket.client.emit("createResearch");
        },
        saveProject(context, data) {
            data.researchIndex = data.id
            this._vm.$socket.client.emit("saveResearch", data);
        },
        removeProject(context, data) {
            data.researchIndex = data.id
            this._vm.$socket.client.emit("removeResearch", data);
        },
        changePorts(context, data) {
            this._vm.$socket.client.emit("changePorts", JSON.stringify(data))
        },
        changeResearchname(context, data) {
            this._vm.$socket.client.emit("changeResearchname", JSON.stringify(data))
        },
        triggerSynchronization(context, data, fn) {
            console.log("trigger sync data: ", data)
            this._vm.$socket.client.emit("triggerSynchronization", JSON.stringify(data), (response) => {
                console.log("got response: ", response)
                fn(response)
            })
        },
        requestUserServiceList(context) {
            this._vm.$socket.client.emit("getUserServices", (response) => {
                context.dispatch("SOCKET_UserServiceList", response)
            });
        },
        requestServiceList(context) {
            this._vm.$socket.client.emit("getServicesList", (response) => {
                context.dispatch("SOCKET_ServiceList", response)
            });
        },
        requestProjectList(context) {
            this._vm.$socket.client.emit("getAllResearch", (response) => {
                context.dispatch("SOCKET_ProjectList", response)
            });
        },
        exchangeCode(context, data) {
            if (!!data.code && !!data.state) {
                this._vm.$socket.client.emit("exchangeCode", JSON.stringify(data), (response) => {
                    console.log("exchangeCode response", response)
                });
            }
        },
        addServiceWithCredentials(context, service) {
            this._vm.$socket.client.emit("addCredentials", JSON.stringify(service), (response) => {
                console.log("credentials response", response)
            });
        },
        removeService(context, service) {
            this._vm.$socket.client.emit("removeServiceForUser", JSON.stringify(service));
        },
    },

}