import OwncloudAuthenticatorComponent from "./owncloud.component.vue";
import OwncloudCallbackComponent from "./owncloud-callback.component.vue";
import AuthManager from "./auth-manager.service";

export default {
    install(Vue, options) {
        Vue.mixin({});

        let log = options.log;
        log.debug("instantiate owncloud plugin");
        Vue.prototype.owncloudAuthenticationManager = new AuthManager({
            log: options.log,
            httpService: options.$http,
            configuration: options.configuration,
            oauthToken: options.oauthToken,
        });
        Vue.component("OwncloudAuthenticatorComponent", OwncloudAuthenticatorComponent);
        Vue.component("OwncloudCallbackComponent", OwncloudCallbackComponent);

        options.router.addRoutes([
            {
                path: "/owncloud-callback",
                component: OwncloudCallbackComponent,
            },
        ]);
    },
};
