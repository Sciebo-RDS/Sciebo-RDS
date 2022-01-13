import VueSocketIO from 'vue-socket.io-extended';
import { io } from 'socket.io-client';
import store from "./store"
import config from "../config.js"

export default {
    install: function (Vue) {
        console.log(`connect socket to ${config.config.socket.server} ${config.config.socket.path}`)
        const ioInstance = io(config.config.socket.server, {
            path: config.config.socket.path,
            reconnection: true,
            reconnectionDelay: 3000,
            maxReconnectionAttempts: Infinity,
            transports: ["websocket"],
            autoConnect: false,
            withCredentials: true
        });

        Vue.use(VueSocketIO, ioInstance, {
            store,
            actionPrefix: 'SOCKET_',
            mutationPrefix: 'SOCKET_',
            eventToActionTransformer: (actionName) => actionName // cancel camel case
        })

    }
}
