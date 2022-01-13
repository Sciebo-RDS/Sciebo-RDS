import "regenerator-runtime";
import fetch from "node-fetch";
import { removeCollection, insertCollection } from "../lib/collections";
import { Crate } from "../lib/crate";
import { createSessionForTest } from "../common";
import { updateUserSession } from "../lib/user";
import models from "../models";
import Chance from "chance";
const chance = new Chance();

const api = "http://localhost:8080";
describe("Test entity and property route operations", () => {
    let sessionId, user;
    beforeEach(async () => {
        ({ user, sessionId } = await createSessionForTest());
    });
    afterAll(async () => {
        await models.sequelize.close();
    });
    test("it should get the root dataset and all of its properties", async () => {
        let collection = await loadData({ name: chance.sentence() });
        await updateUserSession({
            sessionId,
            data: { current: { collectionId: collection.id } },
        });

        let response = await fetch(`${api}/entity/RootDataset`, {
            method: "GET",
            headers: {
                Authorization: `sid ${sessionId}`,
                "Content-Type": "application/json",
            },
        });
        let { entity } = await response.json();
        expect(entity.eid).toEqual("./");
        expect(entity.etype).toEqual("Dataset");
        expect(entity.eid);

        await removeCollection({ id: collection.id });
        await removeUser({ email: user.email });
    });
    test("it should get the entity with the given UUID", async () => {
        let collection = await loadData({ name: chance.sentence() });
        await updateUserSession({
            sessionId,
            data: { current: { collectionId: collection.id } },
        });

        let response = await fetch(`${api}/entity/RootDataset/properties`, {
            method: "GET",
            headers: {
                Authorization: `sid ${sessionId}`,
                "Content-Type": "application/json",
            },
        });
        let entity;
        let { properties } = await response.json();

        const target = properties.filter((p) => p.tgtEntityId).pop().tgtEntityId;
        response = await fetch(`${api}/entity/${target}`, {
            method: "GET",
            headers: {
                Authorization: `sid ${sessionId}`,
                "Content-Type": "application/json",
            },
        });
        ({ entity } = await response.json());
        expect(entity.eid).toEqual("person1");
        expect(entity.etype).toEqual("Person");

        await removeCollection({ id: collection.id });
        await removeUser({ email: user.email });
    });
    test("it should be able to find an entity by id", async () => {
        let collection = await loadData({ name: chance.sentence() });
        await updateUserSession({
            sessionId,
            data: { current: { collectionId: collection.id } },
        });

        // lookup an id
        let response = await fetch(`${api}/entity/lookup`, {
            method: "POST",
            headers: {
                Authorization: `sid ${sessionId}`,
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                etype: "Person",
                eid: "person",
            }),
        });
        let { entities } = await response.json();
        expect(entities.length).toBe(1);

        // lookup a type
        response = await fetch(`${api}/entity/lookup`, {
            method: "POST",
            headers: {
                Authorization: `sid ${sessionId}`,
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ etype: "Dataset" }),
        });
        ({ entities } = await response.json());
        expect(entities.length).toBe(1);

        // lookup all in collectionId
        response = await fetch(`${api}/entity/lookup`, {
            method: "POST",
            headers: {
                Authorization: `sid ${sessionId}`,
                "Content-Type": "application/json",
            },
        });
        ({ entities } = await response.json());
        expect(entities.length).toBe(2);

        await removeCollection({ id: collection.id });
        await removeUser({ email: user.email });
    });
    test("it should fail - no entity defined", async () => {
        let response = await fetch(`${api}/entity`, {
            method: "GET",
            headers: {
                Authorization: `sid ${sessionId}`,
                "Content-Type": "application/json",
            },
        });
        expect(response.status).toBe(403);
        await removeUser({ email: user.email });
    });
    test("it should fail - no collection defined in session", async () => {
        let response = await fetch(`${api}/entity/RootDataset`, {
            method: "GET",
            headers: {
                Authorization: `sid ${sessionId}`,
                "Content-Type": "application/json",
            },
        });
        expect(response.status).toBe(403);
        await removeUser({ email: user.email });
    });
    test("it should be able to create a new entity in the collection", async () => {
        let collection = await loadData({ name: chance.sentence() });
        await updateUserSession({
            sessionId,
            data: { current: { collectionId: collection.id } },
        });
        const entity = {
            name: chance.name(),
            etype: "Person",
        };
        let response = await fetch(`${api}/entity`, {
            method: "POST",
            headers: {
                Authorization: `sid ${sessionId}`,
                "Content-Type": "application/json",
                "X-Testing": true,
            },
            body: JSON.stringify({ entity }),
        });
        expect(response.status).toBe(200);
        await removeCollection({ id: collection.id });
        await removeUser({ email: user.email });
    });
    test("it should be able to update an entities data", async () => {
        let collection = await loadData({ name: chance.sentence() });
        await updateUserSession({
            sessionId,
            data: { current: { collectionId: collection.id } },
        });
        let entity = {
            name: chance.name(),
            etype: "Person",
        };
        let response = await fetch(`${api}/entity`, {
            method: "POST",
            headers: {
                Authorization: `sid ${sessionId}`,
                "Content-Type": "application/json",
                "X-Testing": true,
            },
            body: JSON.stringify({ entity }),
        });
        expect(response.status).toBe(200);
        ({ entity } = await response.json());

        let update = { name: chance.name(), eid: chance.word() };
        response = await fetch(`${api}/entity/${entity.id}`, {
            method: "PUT",
            headers: {
                Authorization: `sid ${sessionId}`,
                "Content-Type": "application/json",
                "X-Testing": true,
            },
            body: JSON.stringify(update),
        });
        expect(response.status).toBe(200);
        response = await response.json();
        expect(response.entity.name).toEqual(update.name);
        expect(response.entity.eid).toEqual(update.eid);
        await removeCollection({ id: collection.id });
        await removeUser({ email: user.email });
    });
    test("it should be able to delete an entity", async () => {
        let collection = await loadData({ name: chance.sentence() });
        await updateUserSession({
            sessionId,
            data: { current: { collectionId: collection.id } },
        });
        let entity = {
            name: chance.name(),
            etype: "Person",
        };
        let response = await fetch(`${api}/entity`, {
            method: "POST",
            headers: {
                Authorization: `sid ${sessionId}`,
                "Content-Type": "application/json",
                "X-Testing": true,
            },
            body: JSON.stringify({ entity }),
        });
        expect(response.status).toBe(200);
        ({ entity } = await response.json());

        response = await fetch(`${api}/entity/${entity.id}`, {
            method: "DELETE",
            headers: {
                Authorization: `sid ${sessionId}`,
                "Content-Type": "application/json",
                "X-Testing": true,
            },
        });
        expect(response.status).toBe(200);
        entity = await models.entity.findOne({ where: { id: entity.id } });
        expect(entity).toBeNull;
        await removeCollection({ id: collection.id });
        await removeUser({ email: user.email });
    });
    test("it should be able to add a simple property with a value", async () => {
        let collection = await loadData({ name: chance.sentence() });
        await updateUserSession({
            sessionId,
            data: { current: { collectionId: collection.id } },
        });

        let response = await fetch(`${api}/entity/RootDataset`, {
            method: "GET",
            headers: {
                Authorization: `sid ${sessionId}`,
                "Content-Type": "application/json",
            },
        });
        let { entity } = await response.json();

        let property = {
            property: "collaborator",
            value: chance.name(),
        };
        response = await fetch(`${api}/entity/${entity.id}/property`, {
            method: "POST",
            headers: {
                Authorization: `sid ${sessionId}`,
                "Content-Type": "application/json",
                "X-Testing": true,
            },
            body: JSON.stringify(property),
        });
        expect(response.status).toBe(200);
        ({ property } = await response.json());

        response = await fetch(`${api}/entity/RootDataset/properties`, {
            method: "GET",
            headers: {
                Authorization: `sid ${sessionId}`,
                "Content-Type": "application/json",
            },
        });
        let { properties } = await response.json();
        let p = properties.filter((p) => p.name === property.name);
        expect(p.length).toBe(1);
        expect(p[0].value).toBe(property.value);

        await removeCollection({ id: collection.id });
        await removeProperty({ id: property.id });
        await removeUser({ email: user.email });
    });
    test("it should be able to update a simple property with a value", async () => {
        let collection = await loadData({ name: chance.sentence() });
        await updateUserSession({
            sessionId,
            data: { current: { collectionId: collection.id } },
        });
        let response = await fetch(`${api}/entity/RootDataset`, {
            method: "GET",
            headers: {
                Authorization: `sid ${sessionId}`,
                "Content-Type": "application/json",
            },
        });
        let { entity } = await response.json();
        let property = {
            property: "collaborator",
            value: chance.name(),
        };
        response = await fetch(`${api}/entity/${entity.id}/property`, {
            method: "POST",
            headers: {
                Authorization: `sid ${sessionId}`,
                "Content-Type": "application/json",
                "X-Testing": true,
            },
            body: JSON.stringify(property),
        });
        expect(response.status).toBe(200);
        ({ property } = await response.json());
        let update = {
            value: chance.name(),
        };
        response = await fetch(`${api}/entity/${entity.id}/property/${property.id}`, {
            method: "PUT",
            headers: {
                Authorization: `sid ${sessionId}`,
                "Content-Type": "application/json",
                "X-Testing": true,
            },
            body: JSON.stringify(update),
        });
        expect(response.status).toBe(200);
        ({ property } = await response.json());
        response = await fetch(`${api}/entity/RootDataset/properties`, {
            method: "GET",
            headers: {
                Authorization: `sid ${sessionId}`,
                "Content-Type": "application/json",
            },
        });
        let { properties } = await response.json();
        let p = properties.filter((p) => p.name === property.name);
        expect(p.length).toBe(1);
        expect(p[0].value).toBe(property.value);
        await removeCollection({ id: collection.id });
        await removeProperty({ id: property.id });
        await removeUser({ email: user.email });
    });
    test("it should be able to remove a property", async () => {
        let collection = await loadData({ name: chance.sentence() });
        await updateUserSession({
            sessionId,
            data: { current: { collectionId: collection.id } },
        });
        let response = await fetch(`${api}/entity/RootDataset`, {
            method: "GET",
            headers: {
                Authorization: `sid ${sessionId}`,
                "Content-Type": "application/json",
            },
        });
        let { entity } = await response.json();
        let property = {
            property: "collaborator",
            value: chance.name(),
        };
        response = await fetch(`${api}/entity/${entity.id}/property`, {
            method: "POST",
            headers: {
                Authorization: `sid ${sessionId}`,
                "Content-Type": "application/json",
                "X-Testing": true,
            },
            body: JSON.stringify(property),
        });
        expect(response.status).toBe(200);
        ({ property } = await response.json());

        response = await fetch(`${api}/entity/${entity.id}/property/${property.id}`, {
            method: "DELETE",
            headers: {
                Authorization: `sid ${sessionId}`,
                "Content-Type": "application/json",
                "X-Testing": true,
            },
        });
        expect(response.status).toBe(200);

        response = await fetch(`${api}/entity/RootDataset/properties`, {
            method: "GET",
            headers: {
                Authorization: `sid ${sessionId}`,
                "Content-Type": "application/json",
            },
        });
        let { properties } = await response.json();
        let p = properties.filter((p) => p.name === property.name);
        expect(p.length).toBe(0);

        await removeCollection({ id: collection.id });
        await removeProperty({ id: property.id });
        await removeUser({ email: user.email });
    });
    test("it should associate two entities", async () => {
        let collection = await loadData({ name: chance.sentence() });
        await updateUserSession({
            sessionId,
            data: { current: { collectionId: collection.id } },
        });
        let entity = await fetch(`${api}/entity/RootDataset`, {
            method: "GET",
            headers: {
                Authorization: `sid ${sessionId}`,
                "Content-Type": "application/json",
            },
        });
        ({ entity } = await entity.json());

        let entityB = await fetch(`${api}/entity/lookup`, {
            method: "POST",
            headers: {
                Authorization: `sid ${sessionId}`,
                "Content-Type": "application/json",
                "X-Testing": true,
            },
            body: JSON.stringify({ eid: "person1" }),
        });
        let { entities } = await entityB.json();
        entityB = entities.pop();

        let association = {
            property: "collaborator",
            tgtEntityId: entityB.id,
        };
        let response = await fetch(`${api}/entity/${entity.id}/associate`, {
            method: "PUT",
            headers: {
                Authorization: `sid ${sessionId}`,
                "Content-Type": "application/json",
                "X-Testing": true,
            },
            body: JSON.stringify(association),
        });
        expect(response.status).toBe(200);

        entity = await fetch(`${api}/entity/${entity.id}/properties`, {
            method: "GET",
            headers: {
                Authorization: `sid ${sessionId}`,
                "Content-Type": "application/json",
            },
        });
        let { properties } = await entity.json();
        let p = properties.filter((p) => p.name === "collaborator");
        expect(p.length).toBe(1);

        await removeCollection({ id: collection.id });
        await removeUser({ email: user.email });
    });
    test("it should be able to create new file and folder entities", async () => {
        let collection = await loadData({ name: chance.sentence() });
        await updateUserSession({
            sessionId,
            data: { current: { collectionId: collection.id } },
        });
        let files = [
            {
                path: "filea.mpg",
                parent: "/test",
                isDir: false,
                mimeType: "audio/mpeg",
                modTime: "2020-10-28T00:01:47Z",
            },
        ];
        let response = await fetch(`${api}/files`, {
            method: "POST",
            headers: {
                Authorization: `sid ${sessionId}`,
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ files }),
        });
        expect(response.status).toBe(200);
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
async function removeProperty({ id }) {
    await models.property.destroy({ where: { id } });
}
