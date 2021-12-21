import "regenerator-runtime";
import fetch from "node-fetch";
import { loadConfiguration } from "../common";
import { isMatch, cloneDeep } from "lodash";
import { writeJSON } from "fs-extra";
import path from "path";
import { getUserSession } from "../lib/user";
import { createSessionForTest } from "../common";

describe("Test routes - index.js", () => {
    const api = "http://localhost:8080";
    afterAll(async () => {
        await models.sequelize.close();
    });

    test("it should be able get the UI configuration", async () => {
        let response = await fetch(`${api}/configuration`);
        let config = await loadConfiguration();
        if (response.status === 200) {
            response = await response.json();
            expect(isMatch(response.configuration, config.ui)).toBeTrue;
        }
    });

    test("it should be able to create a new session", async () => {
        const origConfig = await loadConfiguration();

        let testConfig = cloneDeep(origConfig);
        testConfig.api.applications = [{ name: "test", secret: "xxx" }];
        await writeJSON("/srv/configuration/development-configuration.json", testConfig);
        let user = {
            email: "test@test.com",
            name: "test user",
        };

        let response = await fetch(`${api}/session/application`, {
            method: "POST",
            headers: {
                Authorization: "Bearer xxx",
                "Content-Type": "application/json",
            },
            body: JSON.stringify(user),
        });
        expect(response.status).toBe(200);
        response = await response.json();
        let s = await getUserSession({ email: user.email });
        expect(s.session.id).toEqual(response.sessionId);

        await writeJSON("/srv/configuration/development-configuration.json", origConfig);
    });

    test("it should be able to update an existing session", async () => {
        const origConfig = await loadConfiguration();

        let testConfig = cloneDeep(origConfig);
        testConfig.api.applications = [{ name: "test", secret: "xxx" }];
        await writeJSON("/srv/configuration/development-configuration.json", testConfig);
        let user = {
            email: "test@test.com",
            name: "test user",
            session: {
                owncloud: {
                    url: "1",
                },
            },
        };

        let response = await fetch(`${api}/session/application`, {
            method: "POST",
            headers: {
                Authorization: "Bearer xxx",
                "Content-Type": "application/json",
            },
            body: JSON.stringify(user),
        });
        expect(response.status).toBe(200);
        response = await response.json();

        const sessionId = response.sessionId;

        response = await fetch(`${api}/session/application/${sessionId}`, {
            method: "PUT",
            headers: {
                Authorization: "Bearer xxx",
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ session: { owncloud: { url: "2" } } }),
        });
        expect(response.status).toBe(200);
        response = await response.json();

        let s = await getUserSession({ sessionId });
        expect(s.session.data.services.owncloud.url).toEqual("2");

        await writeJSON("/srv/configuration/development-configuration.json", origConfig);
    });

    test("it should be able to create a session and login - bypassing okta auth", async () => {
        const origConfig = await loadConfiguration();

        let testConfig = cloneDeep(origConfig);
        testConfig.api.applications = [{ name: "test", secret: "xxx" }];
        await writeJSON("/srv/configuration/development-configuration.json", testConfig);
        const user = {
            email: "test2@test.com",
            name: "test user 2",
        };

        let response = await fetch(`${api}/session/application`, {
            method: "POST",
            headers: {
                Authorization: "Bearer xxx",
                "Content-Type": "application/json",
            },
            body: JSON.stringify(user),
        });
        expect(response.status).toBe(200);
        let { sessionId } = await response.json();

        response = await fetch(`${api}/authenticated`, {
            method: "GET",
            headers: {
                Authorization: `sid ${sessionId}`,
                "Content-Type": "application/json",
            },
        });
        expect(response.status).toBe(200);
        await writeJSON("/srv/configuration/development-configuration.json", origConfig);
    });

    test("it should be able to get service configuration", async () => {
        let { user, sessionId } = await createSessionForTest();
        let response = await fetch(`${api}/entity/RootDataset`, {
            method: "GET",
            headers: {
                Authorization: `sid ${sessionId}`,
                "Content-Type": "application/json",
            },
        });
        response = await fetch(`${api}/session/configuration/owncloud`, {
            method: "GET",
            headers: {
                Authorization: `sid ${sessionId}`,
                "Content-Type": "application/json",
            },
        });
        response = await response.json();
        expect(response.configuration).toBeDefined;
    });

    test("it should be able to save service configuration in the session", async () => {
        let { user, sessionId } = await createSessionForTest();
        let response = await fetch(`${api}/entity/RootDataset`, {
            method: "GET",
            headers: {
                Authorization: `sid ${sessionId}`,
                "Content-Type": "application/json",
            },
        });
        response = await fetch(`${api}/session/configuration/owncloud`, {
            method: "POST",
            headers: {
                Authorization: `sid ${sessionId}`,
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                service: "owncloud",
                url: "2",
            }),
        });
        response = await response.json();

        let s = await getUserSession({ sessionId });
        expect(s.session.data.services.owncloud.url).toEqual("2");
    });
});
