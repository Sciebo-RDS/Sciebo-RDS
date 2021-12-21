import path from "path";
import fetch from "node-fetch";
import { readJSON, writeJSON } from "fs-extra";
import { cloneDeep } from "lodash";
import { Crate } from "../lib/crate";
const api = "http://localhost:8080";
import { getLogger } from "../common/logger";
const log = getLogger();
import Chance from "chance";
const chance = new Chance();

export async function loadConfiguration() {
    let configuration =
        process.env.NODE_ENV === "development"
            ? "/srv/configuration/development-configuration.json"
            : "/srv/configuration.json";
    configuration = await readJSON(configuration);
    return configuration;
}

export async function createSessionForTest() {
    const origConfig = await loadConfiguration();

    let testConfig = cloneDeep(origConfig);
    testConfig.api.applications = [{ name: "test", url: "localhost:8000", secret: "xxx" }];
    await writeJSON("/srv/configuration/development-configuration.json", testConfig);
    let user = {
        email: chance.email(),
        name: chance.name(),
    };

    let response = await fetch(`${api}/session/application`, {
        method: "POST",
        headers: {
            Authorization: "Bearer xxx",
            "Content-Type": "application/json",
        },
        body: JSON.stringify(user),
    });
    response = await response.json();
    await writeJSON("/srv/configuration/development-configuration.json", origConfig);
    return { sessionId: response.sessionId, user };
}
