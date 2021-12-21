import "regenerator-runtime";
import { removeCollection, insertCollection } from "../lib/collections";
import { createUser } from "./user";
import { Crate } from "../lib/crate";
import { getEntityProperties } from "./entities";
import {
    insertTemplate,
    removeTemplate,
    getTemplate,
    getTemplates,
    addTemplate,
    replaceCrateWithTemplate,
} from "./template";
import models from "../models";
import Chance from "chance";
const chance = new Chance();

describe("Test template management operations", () => {
    let collection, user, rootDataset;
    beforeAll(async () => {
        collection = await loadData({ name: chance.sentence() });
        user = await createUser({ name: chance.name(), email: chance.email() });
    });
    afterAll(async () => {
        await removeCollection({ id: collection.id });
        await removeUser({ id: user.id });
        await models.sequelize.close();
    });
    test("it should save an entity template", async () => {
        let entity = await models.entity.findOne({
            where: { etype: "Person", collectionId: collection.id },
        });
        let template = await insertTemplate({
            userId: user.id,
            entityId: entity.id,
            collectionId: collection.id,
        });
        template = await getTemplate({ userId: user.id, templateId: template.id });
        expect(template.eid).toEqual("person1");
        expect(template.etype).toEqual("Person");
        await removeTemplate({ userId: user.id, templateId: template.id });
    });
    test("it should save a crate template", async () => {
        let template = await insertTemplate({
            userId: user.id,
            collectionId: collection.id,
            name: "my template",
        });
        template = await getTemplate({ userId: user.id, templateId: template.id });

        // console.log(template);
        expect(template.eid).toBeNull;
        expect(template.etype).toBeNull;
        expect(template.name).toBe("my template");
        expect(template.src["@graph"].length).toBe(3);
        await removeTemplate({ userId: user.id, templateId: template.id });
    });
    test("it should remove a template", async () => {
        let entity = await models.entity.findOne({
            where: { etype: "Person", collectionId: collection.id },
        });
        let template = await insertTemplate({
            userId: user.id,
            entityId: entity.id,
            collectionId: collection.id,
        });
        await removeTemplate({ userId: user.id, templateId: template.id });
        template = await getTemplate({ userId: user.id, templateId: template.id });
        expect(template).toBeNull;
    });
    test("it should find a given template", async () => {
        // save an entity template
        let entity = await models.entity.findOne({
            where: { etype: "Person", collectionId: collection.id },
        });
        await insertTemplate({
            userId: user.id,
            entityId: entity.id,
            collectionId: collection.id,
        });

        //  save a crate template
        await insertTemplate({
            userId: user.id,
            collectionId: collection.id,
            name: "this is a really silly name designed for lookup AGHJDJKHFUHK",
        });

        let { templates } = await getTemplates({ userId: user.id, filter: "person1" });
        expect(templates.length).toEqual(1);
        expect(templates[0].eid).toEqual("person1");

        ({ templates } = await getTemplates({ userId: user.id, filter: "Person" }));
        expect(templates.length).toEqual(1);
        expect(templates[0].eid).toEqual("person1");

        ({ templates } = await getTemplates({ userId: user.id, filter: "a person" }));
        expect(templates.length).toEqual(1);
        expect(templates[0].eid).toEqual("person1");

        ({ templates } = await getTemplates({ userId: user.id, filter: "per" }));
        expect(templates.length).toEqual(1);
        expect(templates[0].eid).toEqual("person1");

        ({ templates } = await getTemplates({ userId: user.id, filter: "designed" }));
        expect(templates.length).toEqual(1);

        ({ templates } = await getTemplates({ userId: user.id }));
        expect(templates.length).toEqual(2);
    });
    test("it should be able to add a template to a collection", async () => {
        let entity = await models.entity.findOne({
            where: { etype: "Person", collectionId: collection.id },
        });
        let template = await insertTemplate({
            userId: user.id,
            entityId: entity.id,
            collectionId: collection.id,
        });
        template = await getTemplate({ userId: user.id, templateId: template.id });
        // console.log(template.src);

        await models.entity.destroy({ where: { id: entity.id } });
        ({ entity } = await addTemplate({
            templateId: template.id,
            userId: user.id,
            collectionId: collection.id,
        }));

        let { properties } = await getEntityProperties({
            id: entity.id,
            collectionId: collection.id,
        });
        properties = properties.map((p) => ({ [p.name]: p.value }));
        expect(properties).toEqual([
            { firstName: "a" },
            { lastName: "person" },
            { description: "something" },
            { description: "and another thing" },
        ]);

        await removeTemplate({ userId: user.id, templateId: template.id });
    });
    test("it should be able to replace a collection with a crate template", async () => {
        let entity = await models.entity.findOne({
            where: { etype: "Person", collectionId: collection.id },
        });
        let template = await insertTemplate({
            userId: user.id,
            name: "my crate",
            collectionId: collection.id,
        });
        template = await getTemplate({ userId: user.id, templateId: template.id });
        await replaceCrateWithTemplate({
            userId: user.id,
            collectionId: collection.id,
            templateId: template.id,
        });

        const entities = await models.entity.findAll({ where: { collectionId: collection.id } });
        expect(entities.length).toBe(2);

        await removeTemplate({ userId: user.id, templateId: template.id });
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
                firstName: "a",
                lastName: "person",
                description: ["something", "and another thing"],
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
