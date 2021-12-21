<template>
    <div class="login flex flex-col">
        <div id="okta-signin-container"></div>
    </div>
</template>

<script>
import OktaSignIn from "@okta/okta-signin-widget";
import "@okta/okta-signin-widget/dist/css/okta-sign-in.min.css";
import { removeSessionSID } from "@/components/auth.service";

export default {
    data() {
        return {
            widget: undefined,
        };
    },
    async mounted() {
        removeSessionSID();
        const okta = this.$store.state.configuration.services.okta;
        this.$nextTick(function () {
            this.widget = new OktaSignIn({
                baseUrl: okta.domain,
                clientId: okta.clientId,
                redirectUri: okta.redirectUri,
                authParams: {
                    pkce: true,
                    issuer: okta.issuer,
                    display: "page",
                    // responseType: ['id_token', 'token'],
                    scopes: ["openid", "profile", "email"],
                },
                logo: this.$store.state.configuration.logo,
                i18n: {
                    en: {
                        "primaryauth.title": this.$store.state.configuration.siteName || "Describo",
                    },
                },
            });
            this.widget.renderEl(
                { el: "#okta-signin-container" },
                () => {
                    /**
                     * In this flow, the success handler will not be called because
                     * there's a redirect to the Okta org for the authentication workflow.
                     */
                },
                (err) => {
                    throw err;
                }
            );
        });
    },
    destroyed() {
        // Remove the widget from the DOM on path change
        this.widget.remove();
    },
};
</script>
