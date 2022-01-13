import OnedriveAuthenticatorComponent from "./onedrive.component.vue";
import OnedriveFilePreviewComponent from "./preview.component.vue";
import AuthManager from "./auth-manager.service";
export default {
    install(Vue, options) {
        Vue.mixin({});

        let log = options.log;
        log.debug("instantiate onedrive auth manager and attach to prototype");
        Vue.prototype.onedriveAuthenticationManager = new AuthManager({
            configuration: options.configuration,
            clientId: options.clientId,
            redirectUri: options.redirectUri,
            tenantId: options.tenantId,
            log: options.log,
            httpService: options.$http,
        });
        Vue.component("OnedriveAuthenticatorComponent", OnedriveAuthenticatorComponent);
        Vue.component("OnedriveFilePreviewComponent", OnedriveFilePreviewComponent);
    },
};
