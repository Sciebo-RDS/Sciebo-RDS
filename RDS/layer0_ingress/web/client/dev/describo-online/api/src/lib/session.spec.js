import "regenerator-runtime";
import { loadConfiguration } from "../common";
import { isMatch, cloneDeep } from "lodash";
import { postSession } from "./session";
import { writeJSON } from "fs-extra";
import path from "path";
import { getUserSession } from "../lib/user";
import models from "../models";

describe("test session creation from stash", () => {
    const api = "http://localhost:8080";

    afterAll(async () => {
        await models.sequelize.close();
    });

    test("it should not be allowed to access this server", async () => {
        const origConfig = await loadConfiguration();

        let testConfig = cloneDeep(origConfig);
        testConfig.api.applications = [{ name: "test", secret: "xxx" }];
        await writeJSON("/srv/configuration/development-configuration.json", testConfig);

        try {
            await postSession({
                authorization: "yyyy",
                name: "test",
                email: "test@test.com",
            });
        } catch (error) {
            expect(error.body.code).toBe("Forbidden");
        }

        await writeJSON("/srv/configuration/development-configuration.json", origConfig);
    });
    test("it should be able to create a new session and get a session id", async () => {
        const origConfig = await loadConfiguration();

        let testConfig = cloneDeep(origConfig);
        testConfig.api.applications = [{ name: "test", secret: "xxx" }];
        await writeJSON("/srv/configuration/development-configuration.json", testConfig);

        const email = "test@test.com";
        let sessionId = await postSession({
            authorization: "xxx",
            name: "test",
            email,
        });
        let { session, user } = await getUserSession({ email });
        expect(session.id).toEqual(sessionId);
        await models.user.destroy({ where: { email } });

        await writeJSON("/srv/configuration/development-configuration.json", origConfig);
    });
});
