export default class AuthManager {
    constructor({ clientId, redirectUri, log, httpService, configuration, oauthToken }) {
        this.$log = log;
        this.config = {
            auth: { clientId, redirectUri },
            configurationEndpoint: configuration,
            oauthTokenEndpoint: oauthToken,
            cache: {
                cacheLocation: "sessionStorage",
            },
        };
        this.tokenKey = "owncloudAccessToken";
        this.accountKey = "owncloudAccount";
        this.serviceKey = "owncloudService";
        this.httpService = httpService;
    }

    async getConfiguration() {
        let response = await this.httpService.get({
            route: this.config.configurationEndpoint,
        });
        return await response.json();
    }

    async getOauthCode({ server }) {
        this.$log.debug("Getting owncloud oauth code");
        window.sessionStorage.setItem(this.serviceKey, JSON.stringify(server));
        let url = `${server.url}${server.oauthAuthoriseEndpoint}?response_type=code&client_id=${server.clientId}&redirect_uri=${server.redirectUri}&scope=read`;
        window.location.href = url;
    }

    async getOauthToken({ code }) {
        this.$log.debug("Getting owncloud oauth token");

        if (code) {
            let server = JSON.parse(window.sessionStorage.getItem(this.serviceKey));
            let response = await this.httpService.post({
                route: this.config.oauthTokenEndpoint,
                body: {
                    host: server.url,
                    code,
                },
            });
            if (response.status !== 200) {
                // can't get access token using code
                throw new Error("Unable to log into owncloud at this time");
            }
            return response.json();
        }
    }
}
