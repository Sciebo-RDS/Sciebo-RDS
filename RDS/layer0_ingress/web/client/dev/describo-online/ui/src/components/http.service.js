import { getSessionSID } from "./auth.service";
import Vue from "vue";

export default class HTTPService {
    constructor({}) {}

    async getHeaders() {
        let accessToken = getSessionSID();
        let authorization = "";
        if (accessToken) {
            authorization = `sid ${accessToken}`;
        } else {
            let token = window.localStorage.getItem("okta-token-storage");
            if (token) {
                token = JSON.parse(token).accessToken.accessToken;
                authorization = `okta ${token}`;
            }
        }
        return {
            authorization,
            "Content-Type": "application/json",
        };
    }

    async get({ route }) {
        let headers = await this.getHeaders();
        let response = await fetch(`/api${route}`, {
            method: "GET",
            headers,
        });
        return response;
    }

    async post({ route, body }) {
        let response = await fetch(`/api${route}`, {
            method: "POST",
            headers: await this.getHeaders(),
            body: JSON.stringify(body),
        });
        return response;
    }

    async put({ route, body }) {
        let response = await fetch(`/api${route}`, {
            method: "PUT",
            headers: await this.getHeaders(),
            body: JSON.stringify(body),
        });
        return response;
    }

    async delete({ route }) {
        let response = await fetch(`/api${route}`, {
            method: "delete",
            headers: await this.getHeaders(),
        });
        return response;
    }
}
