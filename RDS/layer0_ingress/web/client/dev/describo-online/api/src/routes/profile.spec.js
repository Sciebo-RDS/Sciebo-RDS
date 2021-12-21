import "regenerator-runtime";
import fetch from "node-fetch";
import path from "path";
import { createSessionForTest } from "../common";
import { insertCollection } from "../lib/collections";
import { updateUserSession } from "../lib/user";

const chance = require("chance").Chance();
const api = "http://localhost:8080";

describe("Test profile handling routes", () => {
    let sessionId, user;
    beforeAll(async () => {
        ({ user, sessionId } = await createSessionForTest());
    });
    afterAll(async () => {
        await models.user.destroy({ where: { email: user.email } });
        await models.sequelize.close();
    });
    test("it should be able to create a profile", async () => {
        const name = chance.word();
        let collection = await insertCollection({ name });
        let response = await fetch(`${api}/profile`, {
            method: "POST",
            headers: {
                Authorization: `sid ${sessionId}`,
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                name,
                profile: {},
                collectionId: collection.id,
            }),
        });
        response = await response.json();
        expect(response.profile.name).toEqual(name);
        expect(response.profile.collectionId).toEqual(collection.id);
    });
    test("it should fail to create a profile - bad collectionId", async () => {
        const name = chance.word();
        let response = await fetch(`${api}/profile`, {
            method: "POST",
            headers: {
                Authorization: `sid ${sessionId}`,
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                name,
                profile: {},
                collectionId: chance.guid(),
            }),
        });
        expect(response.status).toBe(400);
    });
    test("it should fail to create a profile - no name", async () => {
        const name = chance.word();
        let collection = await insertCollection({ name });
        let response = await fetch(`${api}/profile`, {
            method: "POST",
            headers: {
                Authorization: `sid ${sessionId}`,
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                profile: {},
                collectionId: collection.id,
            }),
        });
        expect(response.status).toBe(400);
    });
    test("it should be able to retrieve a profile", async () => {
        const name = chance.word();
        let collection = await insertCollection({ name });
        await updateUserSession({
            sessionId,
            data: { current: { collectionId: collection.id } },
        });
        let response = await fetch(`${api}/profile`, {
            method: "POST",
            headers: {
                Authorization: `sid ${sessionId}`,
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                name,
                profile: {},
                collectionId: collection.id,
            }),
        });
        response = await response.json();
        const profileId = response.profile.id;

        response = await fetch(`${api}/profile/${profileId}`, {
            method: "GET",
            headers: {
                Authorization: `sid ${sessionId}`,
                "Content-Type": "application/json",
            },
        });
        response = await response.json();
        expect(response.profile.name).toEqual(name);
        expect(response.profile.id).toEqual(profileId);
    });
    test("it should be able to update a profile", async () => {
        let name = chance.word();
        let collection = await insertCollection({ name });
        let response = await fetch(`${api}/profile`, {
            method: "POST",
            headers: {
                Authorization: `sid ${sessionId}`,
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                name,
                profile: {},
                collectionId: collection.id,
            }),
        });
        response = await response.json();
        const profileId = response.profile.id;

        name = chance.word();
        response = await fetch(`${api}/profile/${profileId}`, {
            method: "PUT",
            headers: {
                Authorization: `sid ${sessionId}`,
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                name,
                profile: { key: "value" },
            }),
        });
        response = await response.json();
        expect(response.profile.name).toEqual(name);
        expect(response.profile.profile).toEqual({ key: "value" });
    });
    test("it should be able to lookup profile entities", async () => {
        let collection = await insertCollection({ name: chance.word() });

        await updateUserSession({
            sessionId,
            data: { current: { collectionId: collection.id } },
        });
        let response = await fetch(`${api}/definition/lookup?query=Airline`, {
            method: "GET",
            headers: {
                Authorization: `sid ${sessionId}`,
                "Content-Type": "application/json",
            },
        });
        let { matches } = await response.json();
        expect(matches.length).toBe(3);
    });
    test("it should be able to get a type definition", async () => {
        let collection = await insertCollection({ name: chance.name() });
        await updateUserSession({
            sessionId,
            data: { current: { collectionId: collection.id } },
        });
        let response = await fetch(`${api}/definition?name=Airline`, {
            method: "GET",
            headers: {
                Authorization: `sid ${sessionId}`,
                "Content-Type": "application/json",
            },
        });
        let { definition } = await response.json();
        expect(definition.name).toBe("Airline");
    });
});
