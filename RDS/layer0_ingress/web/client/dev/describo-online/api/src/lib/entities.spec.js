import "regenerator-runtime";
import {
    findEntity,
    getEntity,
    getEntityCount,
    getEntityProperties,
    getEntities,
    insertEntity,
    updateEntity,
    removeEntity,
    associate,
    attachProperty,
    updateProperty,
    removeProperty,
    insertFilesAndFolders,
    generateParentPaths,
} from "./entities";
import models from "../models";
import Chance from "chance";
const chance = new Chance();
import { uniq } from "lodash";

describe("Test entity and property management operations", () => {
    let collection, rootDataset;
    beforeAll(async () => {
        collection = await models.collection.create({ name: chance.name() });
        let entity = {
            "@id": "./",
            "@type": "Dataset",
            name: "root dataset",
        };
        rootDataset = await insertEntity({ entity, collectionId: collection.id });
    });
    afterAll(async () => {
        await models.collection.destroy({ where: { id: collection.id } });
        await models.sequelize.close();
    });
    test("it should be able to create an entity", async () => {
        let entity = {
            "@id": "1",
            "@type": "Person",
            name: "test",
        };
        entity = await insertEntity({ entity, collectionId: collection.id });
        let result = await models.entity.findAll({
            where: { eid: "1", etype: "Person", name: "test" },
        });
        expect(result.length).toEqual(1);
        expect(result[0].id).toEqual(entity.id);
        await removeEntities({ entities: [entity] });
    });
    test("it should fail to update an entity", async () => {
        let entity = {
            "@id": "1",
            "@type": "Person",
            name: "test",
        };
        entity = await insertEntity({ entity, collectionId: collection.id });
        try {
            let result = await updateEntity({
                collectionId: "4dcb643c-bfcf-43e9-86b4-77d2e20e7a2d",
                entityId: entity.id,
                name: "y",
                eid: "f",
            });
        } catch (error) {
            expect(error.message).toEqual(`You don't have permission to access that entity`);
        }
        await removeEntities({ entities: [entity] });
    });
    test("it should fail to attach a property to an entity", async () => {
        let entity = {
            "@id": "1",
            "@type": "Person",
            name: "test",
        };
        entity = await insertEntity({ entity, collectionId: collection.id });
        try {
            let result = await attachProperty({
                collectionId: "4dcb643c-bfcf-43e9-86b4-77d2e20e7a2d",
                entityId: entity.id,
                property: "y",
                value: "f",
            });
        } catch (error) {
            expect(error.message).toEqual(`You don't have permission to access that entity`);
        }
        await removeEntities({ entities: [entity] });
    });
    test("it should fail to update a property on an entity", async () => {
        let entity = {
            "@id": "1",
            "@type": "Person",
            name: "test",
        };
        entity = await insertEntity({ entity, collectionId: collection.id });
        try {
            let result = await updateProperty({
                collectionId: "4dcb643c-bfcf-43e9-86b4-77d2e20e7a2d",
                entityId: entity.id,
                property: "y",
                value: "f",
            });
        } catch (error) {
            expect(error.message).toEqual(`You don't have permission to access that entity`);
        }
        await removeEntities({ entities: [entity] });
    });
    test("it should fail to remove a property on an entity", async () => {
        let entity = {
            "@id": "1",
            "@type": "Person",
            name: "test",
        };
        entity = await insertEntity({ entity, collectionId: collection.id });
        let property = await attachProperty({
            collectionId: collection.id,
            entityId: entity.id,
            property: "author",
            value: "something",
        });
        try {
            let result = await removeProperty({
                collectionId: "4dcb643c-bfcf-43e9-86b4-77d2e20e7a2d",
                entityId: entity.id,
                propertyId: property.id,
            });
        } catch (error) {
            expect(error.message).toEqual(`You don't have permission to access that entity`);
        }
        await removeEntities({ entities: [entity] });
    });
    test("it should fail to remove an entity", async () => {
        let entity = {
            "@id": "1",
            "@type": "Person",
            name: "test",
        };
        entity = await insertEntity({ entity, collectionId: collection.id });
        try {
            let result = await removeEntity({
                collectionId: "4dcb643c-bfcf-43e9-86b4-77d2e20e7a2d",
                entityId: entity.id,
            });
        } catch (error) {
            expect(error.message).toEqual(`You don't have permission to access that entity`);
        }
        await removeEntities({ entities: [entity] });
    });
    test("it should be able to create an entity and set its hierarchy", async () => {
        let entity = {
            "@id": "1",
            "@type": "Camel",
            name: "test",
        };
        entity = await insertEntity({ entity, collectionId: collection.id });
        let result = await models.entity.findAll({
            where: { eid: "1", etype: "Camel", name: "test" },
        });
        expect(result.length).toEqual(1);
        expect(result[0].id).toEqual(entity.id);
        await removeEntities({ entities: [entity] });
    });
    test("it should be able to update an entities name or @id", async () => {
        let entity = {
            "@id": "1",
            "@type": "Person",
            name: "test",
        };
        entity = await insertEntity({ entity, collectionId: collection.id });

        entity = await updateEntity({
            collectionId: collection.id,
            entityId: entity.id,
            name: "new",
        });
        expect(entity.name).toBe("new");
        entity = await updateEntity({
            collectionId: collection.id,
            entityId: entity.id,
            eid: "new",
        });
        expect(entity.eid).toBe("new");
        entity = await updateEntity({
            collectionId: collection.id,
            entityId: entity.id,
            name: "blah",
            eid: "boo",
        });
        expect(entity.eid).toBe("boo");
        expect(entity.name).toBe("blah");

        await removeEntities({ entities: [entity] });
    });
    test("it should not be able to create an entity - missing @type", async () => {
        let entity = {
            "@id": "Person",
            name: "test",
        };
        try {
            entity = await insertEntity({
                entity,
                collectionId: collection.id,
            });
        } catch (error) {
            expect(error.message).toEqual(`Entity missing '@type' property`);
        }
    });
    test("it should be able to create a property attached to an entity", async () => {
        let entity = {
            "@id": "1",
            "@type": "Person",
            name: "test",
        };
        entity = await insertEntity({
            entity,
            collectionId: collection.id,
        });
        let property = await attachProperty({
            collectionId: collection.id,
            entityId: entity.id,
            property: "author",
            value: "something",
        });
        entity = await models.entity.findOne({
            where: { id: entity.id },
            include: [{ model: models.property }],
        });
        expect(entity.properties.length).toEqual(1);
        await removeEntities({ entities: [entity] });
    });
    test("it should be able to update a property attached to an entity", async () => {
        let entity = {
            "@id": "1",
            "@type": "Person",
            name: "test",
        };
        entity = await insertEntity({
            entity,
            collectionId: collection.id,
        });
        let property = await attachProperty({
            collectionId: collection.id,
            entityId: entity.id,
            property: "author",
            value: "something",
        });
        property = await updateProperty({
            collectionId: collection.id,
            entityId: entity.id,
            propertyId: property.id,
            value: "something else",
        });
        entity = await models.entity.findOne({
            where: { id: entity.id },
            include: [{ model: models.property }],
        });
        expect(entity.properties.length).toEqual(1);
        await removeEntities({ entities: [entity] });
    });
    test("it should be able to remove a property attached to an entity", async () => {
        let entity = {
            "@id": "1",
            "@type": "Person",
            name: "test",
        };
        entity = await insertEntity({
            entity,
            collectionId: collection.id,
        });
        let property = await attachProperty({
            collectionId: collection.id,
            entityId: entity.id,
            property: "author",
            value: "something",
        });
        await removeProperty({
            collectionId: collection.id,
            entityId: entity.id,
            propertyId: property.id,
        });
        entity = await models.entity.findOne({
            where: { id: entity.id },
            include: [{ model: models.property }],
        });
        expect(entity.properties.length).toEqual(0);
        await removeEntities({ entities: [entity] });
    });
    test("it should be able to remove link property attached to an entity", async () => {
        let entityA = {
            "@id": "A",
            "@type": "Person",
            name: "A",
        };
        entityA = await insertEntity({
            entity: entityA,
            collectionId: collection.id,
        });
        let entityB = {
            "@id": "B",
            "@type": "Person",
            name: "B",
        };
        entityB = await insertEntity({
            entity: entityB,
            collectionId: collection.id,
        });
        await associate({
            collectionId: collection.id,
            entityId: entityA.id,
            property: "author",
            tgtEntityId: entityB.id,
        });
        let entity = await models.entity.findOne({
            where: { id: entityA.id },
            include: [{ model: models.property }],
        });
        await removeProperty({
            collectionId: collection.id,
            entityId: entity.id,
            propertyId: entity.properties[0].id,
        });
        entity = await models.entity.findOne({
            where: { id: entityA.id },
            include: [{ model: models.property }],
        });
        expect(entity.properties.length).toBe(0);
        await removeEntities({ entities: [entityA, entityB] });
    });
    test("it should be able to attach the same property multiple time with different values", async () => {
        let entity = {
            "@id": "1",
            "@type": "Person",
            name: "test",
        };
        entity = await insertEntity({
            entity,
            collectionId: collection.id,
        });
        let property = await attachProperty({
            collectionId: collection.id,
            entityId: entity.id,
            property: "author",
            value: "something",
        });
        property = await attachProperty({
            collectionId: collection.id,
            entityId: entity.id,
            property: "author",
            value: "something else",
        });
        entity = await models.entity.findOne({
            where: { id: entity.id },
            include: [{ model: models.property }],
        });
        expect(entity.properties.length).toEqual(2);
        await removeEntities({ entities: [entity] });
    });
    test("it should be able to link two entities", async () => {
        let entityA = {
            "@id": "A",
            "@type": "Person",
            name: "A",
        };
        entityA = await insertEntity({
            entity: entityA,
            collectionId: collection.id,
        });
        let entityB = {
            "@id": "B",
            "@type": "Person",
            name: "B",
        };
        entityB = await insertEntity({
            entity: entityB,
            collectionId: collection.id,
        });
        await associate({
            collectionId: collection.id,
            entityId: entityA.id,
            property: "author",
            tgtEntityId: entityB.id,
        });
        let entities = await models.entity.findAll({
            include: [{ model: models.property }],
        });
        entityA = entities.filter((e) => e.name === "A")[0];
        entityB = entities.filter((e) => e.name === "B")[0];
        let propsA = entityA.properties[0].get();
        let propsB = entityB.properties[0].get();
        expect(propsA.entityId).toEqual(entityA.id);
        expect(propsA.tgtEntityId).toEqual(entityB.id);
        expect(propsA.direction).toEqual("F");

        expect(propsB.entityId).toEqual(entityB.id);
        expect(propsB.tgtEntityId).toEqual(entityA.id);
        expect(propsB.direction).toEqual("R");
        await removeEntities({ entities: [entityA, entityB] });
    });
    test("it should fail to link two entities", async () => {
        let entityA = {
            "@id": "A",
            "@type": "Person",
            name: "A",
        };
        entityA = await insertEntity({
            entity: entityA,
            collectionId: collection.id,
        });
        let entityB = {
            "@id": "B",
            "@type": "Person",
            name: "B",
        };
        entityB = await insertEntity({
            entity: entityB,
            collectionId: collection.id,
        });
        try {
            await associate({
                collectionId: "4dcb643c-bfcf-43e9-86b4-77d2e20e7a2d",
                entityId: entityA.id,
                property: "author",
                tgtEntityId: entityB.id,
            });
        } catch (error) {
            expect(error.message).toEqual(`You don't have permission to access that entity`);
        }
        await removeEntities({ entities: [entityA, entityB] });
    });
    test("it should be able to get all entity properties", async () => {
        let entityA = {
            "@id": "A",
            "@type": "Person",
            name: "A",
        };
        entityA = await insertEntity({
            entity: entityA,
            collectionId: collection.id,
        });
        let entityB = {
            "@id": "B",
            "@type": "Person",
            name: "B",
        };
        entityB = await insertEntity({
            entity: entityB,
            collectionId: collection.id,
        });
        let property = await attachProperty({
            collectionId: collection.id,
            entityId: entityA.id,
            property: "author",
            value: "something",
        });
        property = await attachProperty({
            collectionId: collection.id,
            entityId: entityA.id,
            property: "author",
            value: "something else",
        });
        await associate({
            collectionId: collection.id,
            entityId: entityA.id,
            property: "author",
            tgtEntityId: entityB.id,
        });
        let entity = await getEntityProperties({
            id: entityA.id,
            collectionId: collection.id,
        });
        let forward = entity.properties.filter((p) => p.direction === "F");
        let reverse = entity.properties.filter((p) => p.direction === "R");
        expect(entity.properties.length).toEqual(3);
        expect(forward.length).toEqual(1);
        expect(reverse.length).toEqual(0);
        await removeEntities({ entities: [entityA, entityB] });
    });
    test("it should be able to remove an entity and all associated properties", async () => {
        let entity = {
            "@id": "A",
            "@type": "Person",
            name: "A",
        };
        entity = await insertEntity({
            entity,
            collectionId: collection.id,
        });
        const entityId = entity.id;
        let property = await attachProperty({
            collectionId: collection.id,
            entityId: entity.id,
            property: "author",
            value: "something",
        });
        await removeEntity({ collectionId: collection.id, entityId });
        entity = await models.entity.findAll({ where: { id: entityId } });
        property = await models.property.findAll({
            where: { entityId },
        });
        expect(entity.length).toBe(0);
        expect(property.length).toBe(0);
    });
    test("it should be able to remove an entity and all associations - forward and reverse 1", async () => {
        let entityA = {
            "@id": "A",
            "@type": "Person",
            name: "A",
        };
        entityA = await insertEntity({
            entity: entityA,
            collectionId: collection.id,
        });
        let entityB = {
            "@id": "B",
            "@type": "Person",
            name: "B",
        };
        entityB = await insertEntity({
            entity: entityB,
            collectionId: collection.id,
        });
        await associate({
            collectionId: collection.id,
            entityId: entityA.id,
            property: "author",
            tgtEntityId: entityB.id,
        });
        await removeEntity({ collectionId: collection.id, entityId: entityA.id });
        let entities = await models.entity.findAll({
            where: { id: entityA.id },
            include: [{ model: models.property }],
        });
        expect(entities.length).toEqual(0);

        entities = await models.entity.findAll({
            where: { id: entityB.id },
            include: [{ model: models.property }],
        });
        expect(entities.length).toEqual(1);
        await removeEntities({ entities: [entityA, entityB] });
    });
    test("it should be able to remove an entity and all associations - forward and reverse 2", async () => {
        let entityA = {
            "@id": "A",
            "@type": "Person",
            name: "A",
        };
        entityA = await insertEntity({
            entity: entityA,
            collectionId: collection.id,
        });
        let entityB = {
            "@id": "B",
            "@type": "Person",
            name: "B",
        };
        entityB = await insertEntity({
            entity: entityB,
            collectionId: collection.id,
        });
        let entityC = {
            "@id": "C",
            "@type": "Person",
            name: "C",
        };
        entityC = await insertEntity({
            entity: entityC,
            collectionId: collection.id,
        });
        await associate({
            collectionId: collection.id,
            entityId: entityA.id,
            property: "author",
            tgtEntityId: entityB.id,
        });
        await associate({
            collectionId: collection.id,
            entityId: entityB.id,
            property: "author",
            tgtEntityId: entityC.id,
        });
        await removeEntity({ collectionId: collection.id, entityId: entityA.id });
        let entities = await models.entity.findAll({
            include: [{ model: models.property }],
        });
        entities = entities.filter((e) => e.eid !== "./");
        expect(entities.length).toEqual(2);
        entities.forEach((e) => {
            expect(e.properties.length).toEqual(1);
            expect(e.properties.length).toEqual(1);
        });
        await removeEntities({ entities });
    });
    test("it should be able to create a file entity connected to the root dataset", async () => {
        let files = [
            {
                path: "filea.mpg",
                parent: undefined,
                isDir: false,
                mimeType: "audio/mpeg",
                modTime: "2020-10-28T00:01:47Z",
            },
        ];
        let entities = await insertFilesAndFolders({ collectionId: collection.id, files });
        for (let entity of entities) {
            let entityId = entity.id;
            entity = await getEntity({ id: entityId, collectionId: collection.id });
            expect(entity.id).toEqual(entityId);
            let { properties } = await getEntityProperties({
                id: entityId,
                collectionId: collection.id,
            });
            expect(properties.length).toEqual(3);
        }
        await removeEntities({ entities });
    });
    test("it should be able to create a folder entity connected to the root datast", async () => {
        // create a folder
        let files = [
            {
                path: "data",
                parent: undefined,
                isDir: true,
                modTime: "2020-10-28T00:01:47Z",
            },
        ];
        let entities = await insertFilesAndFolders({ collectionId: collection.id, files });

        for (let entity of entities) {
            let entityId = entity.id;
            entity = await getEntity({ id: entityId, collectionId: collection.id });
            expect(entity.id).toEqual(entityId);
            let { properties } = await getEntityProperties({
                id: entityId,
                collectionId: collection.id,
            });
            expect(properties.length).toEqual(2);
        }
        await removeEntities({ entities });
    });
    test("it should not duplicate an entry", async () => {
        let files = [
            {
                path: "data",
                parent: undefined,
                isDir: true,
                modTime: "2020-10-28T00:01:47Z",
            },
        ];
        let entities = await insertFilesAndFolders({ collectionId: collection.id, files });
        entities = await models.entity.findAll({
            where: { eid: "data", etype: "Dataset" },
            include: [{ model: models.property }],
        });
        expect(entities.length).toEqual(1);

        entities = await insertFilesAndFolders({ collectionId: collection.id, files });
        entities = await models.entity.findAll({
            where: { eid: "data", etype: "Dataset" },
            include: [{ model: models.property }],
        });
        expect(entities.length).toEqual(1);
        await removeEntities({ entities });
    });
    test("it should be able to create a hierarchy of content", async () => {
        // create a bunch of files and folders
        let files = [
            {
                path: "test",
                parent: undefined,
                isDir: true,
            },
            {
                path: "data",
                parent: "test",
                isDir: true,
            },
            {
                path: "filea.mpg",
                parent: "test",
                isDir: false,
                mimeType: "audio/mpeg",
            },
        ];
        let entities = await insertFilesAndFolders({ collectionId: collection.id, files });

        let entity = await models.entity.findOne({
            where: { eid: "./", etype: "Dataset" },
            include: [{ model: models.property }],
        });
        expect(uniq(entity.properties.map((p) => p.name))).toEqual(["hasPart"]);

        entity = await models.entity.findOne({
            where: { eid: "test", etype: "Dataset" },
            include: [{ model: models.property }],
        });
        expect(entity.properties.length).toBe(3);
        let forward = entity.properties.filter((p) => p.direction === "F");
        expect(forward.length).toBe(2);
        let reverse = entity.properties.filter((p) => p.direction === "R");
        expect(reverse.length).toBe(1);

        await removeEntities({ entities });
    });
    test("it should generate all parent paths", async () => {
        // create a bunch of files and folders
        let files = [
            {
                path: "test",
                parent: "a/b/c/d",
                isDir: true,
            },
        ];
        files = generateParentPaths({ files });
        expect(files).toEqual([
            { path: "test", parent: "a/b/c/d", isDir: true },
            { path: "d", parent: "a/b/c", isDir: true },
            { path: "c", parent: "a/b", isDir: true },
            { path: "b", parent: "a", isDir: true },
            { path: "a", parent: undefined, isDir: true },
        ]);

        files = [
            {
                path: "test",
                parent: "a/b/c/d",
                isDir: true,
            },
            {
                path: "test2",
                parent: "x/y",
                isDir: true,
            },
        ];
        files = generateParentPaths({ files });
        expect(files).toEqual([
            { path: "test", parent: "a/b/c/d", isDir: true },
            { path: "test2", parent: "x/y", isDir: true },
            { path: "d", parent: "a/b/c", isDir: true },
            { path: "c", parent: "a/b", isDir: true },
            { path: "b", parent: "a", isDir: true },
            { path: "a", parent: undefined, isDir: true },
            { path: "y", parent: "x", isDir: true },
            { path: "x", parent: undefined, isDir: true },
        ]);

        files = [
            {
                path: "test.text",
                parent: "a/b/c/d",
                isDir: false,
            },
            {
                path: "test2",
                parent: "x/y",
                isDir: true,
            },
        ];
        files = generateParentPaths({ files });
        expect(files).toEqual([
            { path: "test2", parent: "x/y", isDir: true },
            { path: "d", parent: "a/b/c", isDir: true },
            { path: "c", parent: "a/b", isDir: true },
            { path: "b", parent: "a", isDir: true },
            { path: "a", parent: undefined, isDir: true },
            { path: "y", parent: "x", isDir: true },
            { path: "x", parent: undefined, isDir: true },
            { path: "test.text", parent: "a/b/c/d", isDir: false },
        ]);
    });
    test("it should be able to find an entity", async () => {
        let entity = {
            "@id": "1",
            "@type": "Person",
            name: "test",
        };
        entity = await insertEntity({ entity, collectionId: collection.id });

        let find = await findEntity({ collectionId: collection.id, eid: "1" });
        expect(find.length).toEqual(1);

        find = await findEntity({ collectionId: collection.id, etype: "Person" });
        expect(find.length).toEqual(1);

        find = await findEntity({ collectionId: collection.id, name: "test" });
        expect(find.length).toEqual(1);

        find = await findEntity({ collectionId: collection.id, hierarchy: "Per" });
        expect(find.length).toEqual(1);

        await removeEntities({ entities: [entity] });
    });
    test("it should be able to get a count of entities in the collection", async () => {
        let entity = {
            "@id": "1",
            "@type": "Person",
            name: "test",
        };
        entity = await insertEntity({ entity, collectionId: collection.id });

        let find = await getEntityCount({ collectionId: collection.id });
        expect(find).toEqual(2);

        await removeEntities({ entities: [entity] });
    });
    test("it should be able to get a list of entities in the collection", async () => {
        let entity = {
            "@id": "test",
            "@type": "Person",
            name: "test",
        };
        entity = await insertEntity({ entity, collectionId: collection.id });

        let find = await getEntities({ collectionId: collection.id });
        expect(find.total).toEqual(2);

        find = await getEntities({ collectionId: collection.id, filter: "es" });
        expect(find.total).toEqual(1);

        await removeEntities({ entities: [entity] });
    });
});

async function removeEntities({ entities }) {
    for (let entity of entities) {
        await models.entity.destroy({ where: { id: entity.id } });
    }
}
