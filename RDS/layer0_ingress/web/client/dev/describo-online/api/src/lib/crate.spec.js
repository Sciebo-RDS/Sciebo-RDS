import "regenerator-runtime";
import { writeJSON, remove, ensureDir } from "fs-extra";
import { removeCollection, insertCollection } from "./collections";
import path from "path";
import { Crate } from "./crate";
import { isPlainObject, isMatch, flattenDeep } from "lodash";
import {
    insertEntity,
    attachProperty,
    associate,
    removeEntity,
    removeProperty,
    getEntity,
    getEntityProperties,
} from "./entities";
import models from "../models";
import { createSessionForTest } from "../common";
import Chance from "chance";
const chance = new Chance();

const testFiles = path.join("/tmp", "test-files");
describe("Test loading a crate from a file", () => {
    beforeEach(async () => {
        await ensureDir(testFiles);
    });
    afterAll(async () => {
        await remove(testFiles);
        await models.sequelize.close();
    });
    test("it does not have a describo identifier so one will be added - no identifier prop", async () => {
        let crate = {
            "@context": "https://w3id.org/ro/crate/1.1/context",
            "@graph": [
                {
                    "@type": "CreativeWork",
                    "@id": "ro-crate-metadata.json",
                    conformsTo: { "@id": "https://w3id.org/ro/crate/1.1" },
                    about: { "@id": "./" },
                },

                {
                    "@id": "./",
                    "@type": "Dataset",
                    name: "My crate",
                },
            ],
        };
        const testFileName = path.join(testFiles, "test1.json");
        await writeJSON(testFileName, crate);
        crate = new Crate();
        let { crate: newCrate, collection } = await crate.loadCrateFromFile({
            file: testFileName,
        });
        // console.log(newCrate["@graph"][0].identifier);
        expect(newCrate["@graph"][0].identifier).toEqual([
            {
                "@id": `#:localid:describo:${collection.id}`,
            },
        ]);

        await removeCollection({ id: collection.id });
    });
    test("it does not have a describo identifier so one will be added - existing identifier prop as string", async () => {
        let crate = {
            "@context": "https://w3id.org/ro/crate/1.1/context",
            "@graph": [
                {
                    "@type": "CreativeWork",
                    "@id": "ro-crate-metadata.json",
                    identifier: "ro-crate-metadata.json",
                    conformsTo: { "@id": "https://w3id.org/ro/crate/1.1" },
                    about: { "@id": "./" },
                },

                {
                    "@id": "./",
                    "@type": "Dataset",
                    name: "My crate",
                },
            ],
        };
        const testFileName = path.join(testFiles, "test2.json");
        await writeJSON(testFileName, crate);
        crate = new Crate();
        let { crate: newCrate, collection } = await crate.loadCrateFromFile({
            file: testFileName,
        });
        // console.log(newCrate["@graph"][0].identifier);
        expect(newCrate["@graph"][0].identifier).toEqual([
            "ro-crate-metadata.json",
            {
                "@id": `#:localid:describo:${collection.id}`,
            },
        ]);

        await removeCollection({ id: collection.id });
    });
    test("it does not have a describo identifier so one will be added - existing identifier prop as array", async () => {
        let crate = {
            "@context": "https://w3id.org/ro/crate/1.1/context",
            "@graph": [
                {
                    "@type": "CreativeWork",
                    "@id": "ro-crate-metadata.json",
                    identifier: ["ro-crate-metadata.json"],
                    conformsTo: { "@id": "https://w3id.org/ro/crate/1.1" },
                    about: { "@id": "./" },
                },

                {
                    "@id": "./",
                    "@type": "Dataset",
                    name: "My crate",
                },
            ],
        };
        const testFileName = path.join(testFiles, "test3.json");
        await writeJSON(testFileName, crate);
        crate = new Crate();
        let { crate: newCrate, collection } = await crate.loadCrateFromFile({
            file: testFileName,
        });
        // console.log(newCrate["@graph"][0].identifier);
        expect(newCrate["@graph"][0].identifier).toEqual([
            "ro-crate-metadata.json",
            {
                "@id": `#:localid:describo:${collection.id}`,
            },
        ]);

        await removeCollection({ id: collection.id });
    });
    test("it does not have a describo identifier so one will be added - existing identifier prop as object", async () => {
        let crate = {
            "@context": "https://w3id.org/ro/crate/1.1/context",
            "@graph": [
                {
                    "@type": "CreativeWork",
                    "@id": "ro-crate-metadata.json",
                    identifier: { "@id": "ro-crate-metadata.json" },
                    conformsTo: { "@id": "https://w3id.org/ro/crate/1.1" },
                    about: { "@id": "./" },
                },

                {
                    "@id": "./",
                    "@type": "Dataset",
                    name: "My crate",
                },
            ],
        };
        const testFileName = path.join(testFiles, "test4.json");
        await writeJSON(testFileName, crate);
        crate = new Crate();
        let { crate: newCrate, collection } = await crate.loadCrateFromFile({
            file: testFileName,
        });
        // console.log(newCrate["@graph"][0].identifier);
        expect(newCrate["@graph"][0].identifier).toEqual([
            { "@id": "ro-crate-metadata.json" },
            {
                "@id": `#:localid:describo:${collection.id}`,
            },
        ]);

        await removeCollection({ id: collection.id });
    });
    test("it does have a describo identifier so one will not be added - existing identifier prop as object", async () => {
        let crate = {
            "@context": "https://w3id.org/ro/crate/1.1/context",
            "@graph": [
                {
                    "@type": "CreativeWork",
                    "@id": "ro-crate-metadata.json",
                    identifier: {
                        "@id": "#:localid:describo:e2302114-f1cb-405b-8b8f-53f987849028",
                    },
                    conformsTo: { "@id": "https://w3id.org/ro/crate/1.1" },
                    about: { "@id": "./" },
                },

                {
                    "@id": "./",
                    "@type": "Dataset",
                    name: "My crate",
                },
            ],
        };
        const testFileName = path.join(testFiles, "test5.json");
        await writeJSON(testFileName, crate);
        crate = new Crate();
        let { crate: newCrate, collection } = await crate.loadCrateFromFile({
            file: testFileName,
        });
        // console.log(newCrate["@graph"][0].identifier);
        expect(newCrate["@graph"][0].identifier).toEqual({
            "@id": `#:localid:describo:e2302114-f1cb-405b-8b8f-53f987849028`,
        });

        await removeCollection({ id: collection.id });
    });
    test("it should get the root descriptor", async () => {
        let crate = {
            "@context": "https://w3id.org/ro/crate/1.1/context",
            "@graph": [
                {
                    "@type": "CreativeWork",
                    "@id": "ro-crate-metadata.json",
                    conformsTo: { "@id": "https://w3id.org/ro/crate/1.1" },
                    about: { "@id": "./" },
                },

                {
                    "@id": "./",
                    "@type": "Dataset",
                    name: "My crate",
                },
            ],
        };
        let rootDescriptor = new Crate().getRootDescriptor({ crate });
        expect(rootDescriptor).toEqual(crate["@graph"][0]);
    });
    test("it should get the root dataset", async () => {
        let crate = {
            "@context": "https://w3id.org/ro/crate/1.1/context",
            "@graph": [
                {
                    "@type": "CreativeWork",
                    "@id": "ro-crate-metadata.json",
                    conformsTo: { "@id": "https://w3id.org/ro/crate/1.1" },
                    about: { "@id": "./" },
                },

                {
                    "@id": "./",
                    "@type": "Dataset",
                    name: "My crate",
                },
            ],
        };
        let { rootDescriptor, rootDataset } = new Crate().getRootDataset({
            crate,
        });
        expect(rootDataset).toEqual(crate["@graph"][1]);
    });
    test("it should not find the root dataset", async () => {
        let crate = {
            "@context": "https://w3id.org/ro/crate/1.1/context",
            "@graph": [
                {
                    "@type": "CreativeWork",
                    "@id": "ro-crate-metadata.json",
                    conformsTo: { "@id": "https://w3id.org/ro/crate/1.1" },
                    about: { "@id": "./" },
                },

                {
                    "@id": "something else",
                    "@type": "Dataset",
                    name: "My crate",
                },
            ],
        };
        try {
            let { rootDescriptor, rootDataset } = new Crate().getRootDataset({
                crate,
            });
        } catch (error) {
            expect(error.message).toEqual(`Unable to locate the root dataset`);
        }
    });
    test("it should update the crate root descriptor", async () => {
        let crate = {
            "@context": "https://w3id.org/ro/crate/1.1/context",
            "@graph": [
                {
                    "@type": "CreativeWork",
                    "@id": "ro-crate-metadata.json",
                    conformsTo: { "@id": "https://w3id.org/ro/crate/1.1" },
                    about: { "@id": "./" },
                },

                {
                    "@id": "./",
                    "@type": "Dataset",
                    name: "My crate",
                },
            ],
        };

        const newDescriptor = {
            "@type": "CreativeWork",
            "@id": "ro-crate-metadata.json",
            conformsTo: { "@id": "https://w3id.org/ro/crate/1.1" },
            about: { "@id": "./" },
        };

        crate = new Crate().updateRootDescriptor({
            crate,
            rootDescriptor: newDescriptor,
        });
        expect(crate["@graph"][0]).toEqual(newDescriptor);
    });
    test("should load a simple crate without entities", async () => {
        const name = "my collection";
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
                },
            ],
        };
        let collection = await insertCollection({ name: "test1" });
        let crateManager = new Crate();
        await crateManager.importCrateIntoDatabase({
            collection,
            crate,
            sync: true,
        });

        let entities = await models.entity.findAll({
            where: { collectionId: collection.id },
        });
        expect(entities.length).toEqual(1);
        await removeCollection({ id: collection.id });
    });
    test("should fail to load a simple crate without root descriptor", async () => {
        const name = "my collection";
        const crate = {
            "@context": ["https://w3id.org/ro/crate/1.1/context"],
            "@graph": [
                {
                    "@id": "./",
                    "@type": "Dataset",
                    name: "dataset",
                },
            ],
        };
        let collection = await insertCollection({ name: "test1" });
        let crateManager = new Crate();
        try {
            await crateManager.importCrateIntoDatabase({
                collection,
                crate,
                sync: true,
            });
            // let collection = await importROCrate({ name, crate });
        } catch (error) {
            expect(error.message).toEqual(
                `The crate does not have exactly one root dataset descriptor`
            );
        }
        await removeCollection({ id: collection.id });
    });
    test("should fail to load a simple crate without multiple root descriptors", async () => {
        const name = "my collection";
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
                },
            ],
        };
        let collection = await insertCollection({ name: "test1" });
        let crateManager = new Crate();
        try {
            await crateManager.importCrateIntoDatabase({
                collection,
                crate,
                sync: true,
            });
        } catch (error) {
            expect(error.message).toEqual(
                `The crate does not have exactly one root dataset descriptor`
            );
        }
        await removeCollection({ id: collection.id });
    });
    test("should fail to re-load a collection ", async () => {
        const name = "my test collection";
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
                },
            ],
        };
        let collection = await insertCollection({ name: "test1" });
        let crateManager = new Crate();
        await crateManager.importCrateIntoDatabase({
            collection,
            crate,
            sync: true,
        });

        try {
            await crateManager.importCrateIntoDatabase({
                collection,
                crate,
                sync: true,
            });
        } catch (error) {
            expect(error.message).toEqual("That collection is already loaded.");
        }
        await removeCollection({ id: collection.id });
    });
    test("should load simple crate with one dataset and one entity", async () => {
        const name = "asdsadkgsdfgsdf";
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
        let entities = await models.entity.findAll({
            where: { collectionId: collection.id },
            attributes: ["id"],
            include: [{ model: models.property, attributes: ["id"], raw: true }],
        });
        expect(entities.length).toEqual(2);
        let properties = entities.map((e) => e.properties);
        expect(flattenDeep(properties).length).toEqual(3);

        await removeCollection({ id: collection.id });
    });
    test("should export a simple crate with one dataset and one entity", async () => {
        const name = "my collection";
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
                    author: ["Person", { "@id": "person1" }],
                },
                {
                    "@id": "person1",
                    "@type": "Person",
                    name: "a person",
                },
            ],
        };
        let collection = await insertCollection({ name: "test1" });
        let crateManager = new Crate();
        await crateManager.importCrateIntoDatabase({
            collection,
            crate,
            sync: true,
        });
        let exportedCrate = await crateManager.exportCollectionAsROCrate({
            collectionId: collection.id,
            sync: true,
        });
        // console.log(exportedCrate);

        crate["@graph"].forEach((entry) => {
            let exportedEntry = exportedCrate["@graph"].filter((e) => e["@id"] === entry["@id"]);
            expect(exportedEntry.length).toEqual(1);
            exportedEntry = exportedEntry.pop();
            expect(isMatch(exportedEntry, entry)).toBeTrue;
        });

        await removeCollection({ id: collection.id });
    });
    test("should assemble property values", async () => {
        let crateManager = new Crate();
        const collection = await models.collection.create({
            name: chance.name(),
        });
        const entityA = await models.entity.create({
            name: "entityA",
            eid: "1",
            etype: "person",
            collectionId: collection.id,
        });
        const entityB = await models.entity.create({
            name: "entityB",
            eid: "2",
            etype: "person",
            collectionId: collection.id,
        });
        await attachProperty({
            collectionId: collection.id,
            entityId: entityA.id,
            property: "author",
            value: "personA",
        });
        await attachProperty({
            collectionId: collection.id,
            entityId: entityA.id,
            property: "author",
            value: "personB",
        });

        // test 1 - should return an array with two strings
        // let properties = await models.property.findAll({
        //     where: { entityId: entityA.id },
        // })   ;
        let { properties } = await getEntityProperties({
            id: entityA.id,
            collectionId: collection.id,
        });
        let entities = await models.entity.findAll({
            raw: true,
            attributes: ["id", "eid"],
        });
        let idToEidMapping = entities.reduce((obj, e) => ({ ...obj, [e.id]: e.eid }), {});
        properties = crateManager.assembleProperties({
            properties,
            idToEidMapping,
        });
        expect(properties.forward.author.sort()).toEqual(["personA", "personB"]);

        // test 2 - should return an array with two strings an object
        await associate({
            collectionId: collection.id,
            entityId: entityA.id,
            property: "author",
            tgtEntityId: entityB.id,
        });
        ({ properties } = await getEntityProperties({
            id: entityA.id,
            collectionId: collection.id,
        }));
        entities = await models.entity.findAll({
            raw: true,
            attributes: ["id", "eid"],
        });
        idToEidMapping = entities.reduce((obj, e) => ({ ...obj, [e.id]: e.eid }), {});

        properties = crateManager.assembleProperties({
            properties,
            idToEidMapping,
        });
        // // console.log(JSON.stringify(properties, null, 2));
        expect(properties.forward.author.length).toEqual(3);
        expect(properties.forward.author.filter((e) => isPlainObject(e)).length).toEqual(1);

        ({ properties } = await getEntityProperties({
            id: entityB.id,
            collectionId: collection.id,
        }));
        properties = crateManager.assembleProperties({
            properties,
            idToEidMapping,
        });
        // // console.log(JSON.stringify(properties, null, 2));
        expect(properties.reverse.author.length).toEqual(1);

        await removeCollection({ id: collection.id });
    });
    test("it should correctly save the crate data after a change", async () => {
        let crate = {
            "@context": "https://w3id.org/ro/crate/1.1/context",
            "@graph": [
                {
                    "@type": "CreativeWork",
                    "@id": "ro-crate-metadata.json",
                    conformsTo: { "@id": "https://w3id.org/ro/crate/1.1" },
                    about: { "@id": "./" },
                },

                {
                    "@id": "./",
                    "@type": "Dataset",
                    name: "My crate",
                },
            ],
        };
        const testFileName = path.join(testFiles, "test1.json");
        await writeJSON(testFileName, crate);

        crate = new Crate();
        let { crate: newCrate, collection } = await crate.loadCrateFromFile({
            file: testFileName,
        });
        const collectionId = collection.id;

        await crate.importCrateIntoDatabase({ collection, crate: newCrate, sync: true });

        let rootDataset = (await models.entity.findAll()).pop();

        // update the name property of an entity
        rootDataset.name = "new name";
        let entity = await rootDataset.save();

        let updatedCrate = await save([{ name: "update", entity: entity.get() }]);
        expect(updatedCrate["@graph"][1].name).toEqual("new name");
        await writeJSON(testFileName, updatedCrate);

        // attach simple property - description - with a value
        let property = await attachProperty({
            collectionId,
            entityId: entity.id,
            property: "description",
            value: "text",
            typeDefinition: {},
        });
        updatedCrate = await save([{ name: "update", entity: entity.get() }]);
        expect(updatedCrate["@graph"][1].description).toEqual(["text"]);
        await writeJSON(testFileName, updatedCrate);

        // attach the same simple property - description - with another value
        property = await attachProperty({
            collectionId,
            entityId: entity.id,
            property: "description",
            value: "new",
            typeDefinition: {},
        });
        updatedCrate = await save([{ name: "update", entity: entity.get() }]);
        expect(updatedCrate["@graph"][1].description).toEqual(["text", "new"]);
        await writeJSON(testFileName, updatedCrate);

        // remove a simple property
        property = await removeProperty({
            collectionId,
            entityId: entity.id,
            propertyId: property.id,
        });
        updatedCrate = await save([{ name: "update", entity: entity.get() }]);
        expect(updatedCrate["@graph"][1].description).toEqual(["text"]);
        await writeJSON(testFileName, updatedCrate);

        // add an entity to the collection
        let newEntity = await insertEntity({
            collectionId,
            entity: { name: "test", etype: "Person" },
        });
        updatedCrate = await save([{ name: "insert", entity: newEntity }]);
        expect(updatedCrate["@graph"].length).toEqual(3);
        expect(updatedCrate["@graph"][2].name).toEqual("test");
        expect(updatedCrate["@graph"][2]["@type"]).toEqual("Person");
        await writeJSON(testFileName, updatedCrate);

        // associate an entity to the root dataset
        property = await associate({
            collectionId,
            entityId: rootDataset.id,
            property: "author",
            tgtEntityId: newEntity.id,
        });
        updatedCrate = await save([{ name: "update", entity: rootDataset }]);
        expect(updatedCrate["@graph"][1].author).toEqual([{ "@id": newEntity.id }]);
        expect(updatedCrate["@graph"][2]["@reverse"]).toEqual({ author: [{ "@id": "./" }] });
        await writeJSON(testFileName, updatedCrate);

        // remove a property
        let p = await models.property.findOne({
            where: { entityId: rootDataset.id, name: "author", direction: "F" },
        });

        let updated, removed;
        ({ updated } = await removeProperty({
            collectionId,
            entityId: rootDataset.id,
            propertyId: p.id,
        }));
        let actions = updated.map((eid) => ({ name: "update", entity: { id: eid } }));
        updatedCrate = await save(actions);
        expect(updatedCrate["@graph"][1].author).toBeUndefined;
        expect(updatedCrate["@graph"][2]["@reverse"]).toBeUndefined;
        await writeJSON(testFileName, updatedCrate);

        // remove an entity
        //   but first re-associate it to the root
        await associate({
            collectionId,
            entityId: rootDataset.id,
            property: "author",
            tgtEntityId: newEntity.id,
        });
        updatedCrate = await save([{ name: "update", entity: rootDataset }]);
        await writeJSON(testFileName, updatedCrate);

        //  now remove the whole entity
        ({ updated, removed } = await removeEntity({ collectionId, entityId: newEntity.id }));
        actions = updated.map((eid) => ({ name: "update", entity: { id: eid } }));
        actions = [...actions, { name: "remove", entity: removed }];
        updatedCrate = await save(actions);
        expect(updatedCrate["@graph"].length).toBe(2);
        expect(updatedCrate["@graph"][1].name).toBe("new name");
        await writeJSON(testFileName, updatedCrate);

        // console.log(JSON.stringify(updatedCrate["@graph"], null, 2));

        await removeCollection({ id: collection.id });

        async function save(actions) {
            return await crate.updateCrate({
                localCrateFile: testFileName,
                collectionId,
                actions,
            });
        }
    });
});
