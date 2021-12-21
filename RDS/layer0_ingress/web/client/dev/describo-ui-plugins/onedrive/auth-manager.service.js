import * as msal from "@azure/msal-browser";

export default class AuthManager {
    constructor({ clientId, redirectUri, tenantId, configuration, log, httpService }) {
        this.$log = log;
        this.config = {
            auth: {
                clientId,
                redirectUri,
                authority: `https://login.microsoftonline.com/${tenantId ? tenantId : "common"}`,
            },
            configurationEndpoint: configuration,
            cache: {
                cacheLocation: "sessionStorage",
            },
        };
        this.scopes = [
            "Files.Read",
            "Files.ReadWrite",
            "Files.Read.All",
            "Files.ReadWrite.All",
            "offline_access",
            "Sites.Read.All",
        ];
        this.graphEndpoint = "https://graph.microsoft.com/v1.0";
        this.tokenKey = "onedriveAccessToken";
        this.accountKey = "onedriveAccount";
        this.tokenRefreshHandle = undefined;
        this.refreshTokenIn = 50 * 60 * 1000; // 50 minutes in milliseconds
        this.configuration = undefined;
        this.msalInstance = undefined;
        let account = this.getAccount();
        this.account = account ? account : undefined;
        this.httpService = httpService;
    }

    getAccount() {
        return JSON.parse(window.sessionStorage.getItem(this.accountKey));
    }

    getToken() {
        return JSON.parse(window.sessionStorage.getItem(this.tokenKey));
    }

    async refreshToken() {
        this.$log.debug("Refreshing onedrive token");

        this.msalInstance = new msal.PublicClientApplication(this.config);

        const request = {
            scopes: this.scopes,
            loginHint: this.account?.username,
        };
        let loginResponse;
        if (!this.account?.name) {
            loginResponse = await this.msalInstance.loginPopup(request);
        }
        this.account = this.msalInstance.getAllAccounts().pop();
        window.sessionStorage.setItem(this.accountKey, JSON.stringify(this.account));

        request.account = this.account;
        let token;
        try {
            token = await this.msalInstance.acquireTokenSilent(request);
        } catch (error) {
            token = await this.msalInstance.acquireTokenPopup(request);
        }

        window.sessionStorage.setItem(this.tokenKey, JSON.stringify(token));

        if (this.tokenRefreshHandle) {
            clearTimeout(this.tokenRefreshHandle);
        }
        this.tokenRefreshHandle = setTimeout(this.refreshToken.bind(this), this.refreshTokenIn);

        if (this.httpService && this.api && this.configuration) {
            let configuration = {
                token: {
                    access_token: this.getToken().accessToken,
                    expires: this.getToken().expiresOn,
                },
            };
            this.save({ configuration });
        }

        return { account: this.account, token };
    }

    async login() {
        await this.refreshToken();
    }

    async loadDrives() {
        // get user drive
        let drives = await this.client({ endpoint: "/me/drives" });
        drives = drives.value;
        try {
            drives = drives.filter((d) => !d.webUrl.match("PreservationHoldLibrary"));
        } catch (error) {
            // likely personal drive so use as is
        }
        return { drives };
    }

    async logout() {
        const config = {
            ...this.config,
            postLogoutRedirectUri: window.location.origin,
        };
        const msalApplication = new UserAgentApplication(config);
        const logoutRequest = {
            account: this.account.userName,
        };
        msalApplication.logout(logoutRequest);
    }

    async save({ configuration }) {
        this.$log.debug("Saving onedrive configuration back to the API");
        if (configuration) this.configuration = configuration;
        await this.httpService.post({
            route: this.config.configurationEndpoint,
            body: this.configuration,
        });
    }

    async client({ endpoint, method = "GET", body = {} }) {
        const bearer = `Bearer ${this.getToken().accessToken}`;
        endpoint = `${this.graphEndpoint}${endpoint}`;

        const headers = new Headers();
        headers.append("Authorization", bearer);
        headers.append("Content-Type", "application/json");

        const options = {
            method,
            headers: headers,
        };
        if (method !== "GET") options.body = JSON.stringify(body);

        // console.log(`request made to Graph API ${endpoint}: ` + new Date().toString());

        try {
            let response = await fetch(endpoint, options);
            if (response.status !== 200) {
                //  handle error
                // console.log("error", response);
            }
            return await response.json();
        } catch (error) {
            // console.log(error);
        }
    }
}
