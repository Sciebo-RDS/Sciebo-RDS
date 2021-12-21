import "regenerator-runtime";
import fetch from "node-fetch";
import { removeCollection, insertCollection } from "../lib/collections";
import { Crate } from "../lib/crate";
import { createSessionForTest } from "../common";
import { updateUserSession } from "../lib/user";
import models from "../models";
import Chance from "chance";
const chance = new Chance();

// server.get("/template", route(getTemplatesRouteHandler));
// server.get("/template/:templateId", route(getTemplateRouteHandler));
// server.post("/template", route(postTemplateRouteHandler));
// server.post("/template/:templateId", route(delTemplateRouteHandler));

const api = "http://localhost:8080";
describe("Test template route operations", () => {
    let collection, sessionId, user;
    afterAll(async () => {
        await models.sequelize.close();
    });
    test("it should save an entity template", async () => {
        ({ user, sessionId } = await createSessionForTest());
        collection = await loadData({ name: chance.sentence() });
        await updateUserSession({
            sessionId,
            data: { current: { collectionId: collection.id } },
        });
        let entity = await models.entity.findOne({
            where: { etype: "Person", collectionId: collection.id },
        });
        let response = await fetch(`${api}/template`, {
            method: "POST",
            headers: {
                Authorization: `sid ${sessionId}`,
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                entityId: entity.id,
            }),
        });
        let { template } = await response.json();
        expect(template.eid).toEqual("person1");

        await removeCollection({ id: collection.id });
        await removeUser({ email: user.email });
    });
    test("it should save a crate as a template", async () => {
        ({ user, sessionId } = await createSessionForTest());
        collection = await loadData({ name: chance.sentence() });
        await updateUserSession({
            sessionId,
            data: { current: { collectionId: collection.id } },
        });
        let response = await fetch(`${api}/template`, {
            method: "POST",
            headers: {
                Authorization: `sid ${sessionId}`,
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                name: "my template",
            }),
        });
        let { template } = await response.json();
        expect(template.name).toEqual("my template");

        await removeCollection({ id: collection.id });
        await removeUser({ email: user.email });
    });
    test("it should remove an entity template", async () => {
        ({ user, sessionId } = await createSessionForTest());
        collection = await loadData({ name: chance.sentence() });
        await updateUserSession({
            sessionId,
            data: { current: { collectionId: collection.id } },
        });
        let entity = await models.entity.findOne({
            where: { etype: "Person", collectionId: collection.id },
        });
        let response = await fetch(`${api}/template`, {
            method: "POST",
            headers: {
                Authorization: `sid ${sessionId}`,
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                entityId: entity.id,
            }),
        });
        let { template } = await response.json();
        response = await fetch(`${api}/template/${template.id}`, {
            method: "DELETE",
            headers: {
                Authorization: `sid ${sessionId}`,
                "Content-Type": "application/json",
            },
        });
        expect(response.status).toEqual(200);

        await removeCollection({ id: collection.id });
        await removeUser({ email: user.email });
    });
    test("it should retrieve a template", async () => {
        ({ user, sessionId } = await createSessionForTest());
        collection = await loadData({ name: chance.sentence() });
        await updateUserSession({
            sessionId,
            data: { current: { collectionId: collection.id } },
        });
        let entity = await models.entity.findOne({
            where: { etype: "Person", collectionId: collection.id },
        });
        let response = await fetch(`${api}/template`, {
            method: "POST",
            headers: {
                Authorization: `sid ${sessionId}`,
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                entityId: entity.id,
            }),
        });
        let { template } = await response.json();
        response = await fetch(`${api}/template/${template.id}`, {
            method: "GET",
            headers: {
                Authorization: `sid ${sessionId}`,
                "Content-Type": "application/json",
            },
        });
        expect(response.status).toEqual(200);

        await removeCollection({ id: collection.id });
        await removeUser({ email: user.email });
    });
    test("it should be able to lookup templates", async () => {
        ({ user, sessionId } = await createSessionForTest());
        collection = await loadData({ name: chance.sentence() });
        await updateUserSession({
            sessionId,
            data: { current: { collectionId: collection.id } },
        });
        let entity = await models.entity.findOne({
            where: { etype: "Person", collectionId: collection.id },
        });
        let response = await fetch(`${api}/template`, {
            method: "POST",
            headers: {
                Authorization: `sid ${sessionId}`,
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                entityId: entity.id,
            }),
        });
        response = await fetch(`${api}/template`, {
            method: "POST",
            headers: {
                Authorization: `sid ${sessionId}`,
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                name: "my fancy crate",
            }),
        });

        response = await fetch(`${api}/template?filter=person1`, {
            method: "GET",
            headers: {
                Authorization: `sid ${sessionId}`,
                "Content-Type": "application/json",
            },
        });
        let { templates } = await response.json();
        expect(templates.length).toEqual(1);
        expect(templates[0].eid).toEqual("person1");

        response = await fetch(`${api}/template`, {
            method: "GET",
            headers: {
                Authorization: `sid ${sessionId}`,
                "Content-Type": "application/json",
            },
        });
        ({ templates } = await response.json());
        expect(templates.length).toEqual(2);

        response = await fetch(`${api}/template?filter=fancy`, {
            method: "GET",
            headers: {
                Authorization: `sid ${sessionId}`,
                "Content-Type": "application/json",
            },
        });
        ({ templates } = await response.json());
        expect(templates.length).toEqual(1);

        await removeCollection({ id: collection.id });
        await removeUser({ email: user.email });
    });
});

async function loadData({ name }) {
    const crate = {
        "@context": ["https://w3id.org/ro/crate/1.1/context"],
        "@graph": [
            {
                "@type": "CreativeWork",
                "@id": "ro-crate-metadata.json",
                conformsTo: {
                    "@id": "https://w3id.org/ro/crate/1.1",
                },
                about: { "@id": "./" },
            },
            {
                "@id": "./",
                "@type": "Dataset",
                name: "dataset",
                author: "Person",
                contributor: [{ "@id": "person1" }],
            },
            {
                "@id": "person1",
                "@type": "Person",
                name: "a person",
            },
        ],
    };
    const collection = await insertCollection({ name });
    let crateManager = new Crate();
    await crateManager.importCrateIntoDatabase({
        collection,
        crate,
        sync: true,
    });
    return collection;
}

async function removeUser({ email }) {
    await models.user.destroy({ where: { email } });
}
