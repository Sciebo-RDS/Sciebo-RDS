const models = require("../src/models");
const chance = require("chance").Chance();
const { range, chunk, round, flattenDeep } = require("lodash");

let debug = require("debug");
// debug.enable("datagen");
debug = require("debug")("datagen");

const limits = {
    collection: process.env.N_COLLECTIONS || 1,
    entitiesPerCollection: process.env.N_ENTITIES_PER_COLLECTION || 10,
    usersPerCollection: process.env.N_USERS_PER_COLLECTION || 10,
    propertiesPerEntity: process.env.N_PROPERTIES_PER_ENTITY || 5,
};
const createChunkSize = 100;

const types = ["Person", "Organization", "Place", "License"];

(async () => {
    await models.sequelize.sync();
    await truncateAllTables();

    let data = {
        collections: [],
        users: [],
        entities: [],
    };
    // for (let i in range(chance.integer({ min: 1, max: limits.user }))) {
    //     data.users.push(await createUser());
    // }
    for (let i in range(limits.collection)) {
        console.log(`Creating collection ${parseInt(i) + 1}`);
        // const collection = await createCollection({ users });
        const collection = await createCollection({});

        let entities = [];
        // create a random number of entities between 80% and the upper limit
        for (let j in range(
            // chance.integer({
            //     min: round(0.8 * limits.entitiesPerCollection),
            //     max: limits.entitiesPerCollection,
            // })
            limits.entitiesPerCollection
        )) {
            entities.push({
                name: chance.sentence(),
                etype: chance.pickone(types),
                eid: chance.url(),
                collectionId: collection.id,
            });
        }

        let nChunks = round(entities.length / createChunkSize);
        let j = 0;

        // create all the entities
        for (let c of chunk(entities, createChunkSize)) {
            try {
                debug(`Populating entities - chunk ${j + 1} of ${nChunks}`);
                await models.entity.bulkCreate(c);
            } catch (error) {
                // do nothing
            }
            j += 1;
        }

        // populate the entity properties
        const entityIds = await models.entity.findAll({
            where: { collectionId: collection.id },
            attributes: ["id"],
            raw: true,
        });

        j = 0;
        let entityCollectionLinks = entityIds.map((entity) => {
            return {
                collectionId: collection.id,
                entityId: entity.id,
            };
        });
        for (let c of chunk(entityCollectionLinks, createChunkSize)) {
            debug(
                `Attaching entities to collection - chunk ${
                    j + 1
                } of ${nChunks}`
            );
            try {
                await models.collection_entity.bulkCreate(c);
            } catch (error) {
                // do nothing
            }
            j += 1;
        }

        j = 0;
        for (let entityId of entityIds) {
            j += 1;
            if (!(j % createChunkSize)) {
                debug(
                    `Populating entity properties - ${j} of ${entityIds.length}`
                );
            }
            let properties = [];
            for (let j in range(
                // chance.integer({ min: 3, max: limits.propertiesPerEntity })
                limits.propertiesPerEntity
            )) {
                let data = await createProperty({
                    srcEntityId: entityId.id,
                    entityIds,
                });
                properties = [...properties, ...data.property];
            }
            try {
                properties = await models.property.bulkCreate(properties);
            } catch (error) {
                // do nothing
            }
            let entityProperties = properties.map((p) => {
                if (p.tgtEntityId) {
                    return [
                        {
                            entityId: p.tgtEntityId,
                            propertyId: p.id,
                        },
                        {
                            entityId: entityId.id,
                            propertyId: p.id,
                        },
                    ];
                } else {
                    return [
                        {
                            entityId: entityId.id,
                            propertyId: p.id,
                        },
                    ];
                }
            });
            entityProperties = flattenDeep(entityProperties);
            try {
                await models.entity_properties.bulkCreate(entityProperties);
            } catch (error) {
                //  do nothing
            }
        }

        await new Promise((resolve) => setTimeout(resolve, 1000));
    }

    await report();
    console.log("done");
})();

async function truncateAllTables() {
    await models.property.truncate({ cascade: true });
    await models.entity.truncate({ cascade: true });
    await models.collection.truncate({ cascade: true });
    await models.user.truncate({ cascade: true });
}

async function createUser() {
    return await models.user.create({
        email: chance.email(),
        name: chance.name(),
    });
}

async function createCollection({ users }) {
    // users = chance.pickset(users, limits.usersPerCollection);
    let collection = await models.collection.create({
        name: chance.sentence(),
        description: chance.paragraph(),
    });
    // for (let user of users) {
    //     await models.collection_user.create({
    //         collectionId: collection.id,
    //         userId: user.id,
    //     });
    // }
    return collection;
}

async function createProperty({ srcEntityId, entityIds }) {
    let tgtEntityId = chance.pickone(entityIds).id;
    let property = [];
    if (chance.bool() && tgtEntityId !== srcEntityId) {
        let name = chance.word();
        property.push({
            name,
            tgtEntityId: tgtEntityId,
            direction: "F",
            entityId: srcEntityId,
        });
        property.push({
            name,
            tgtEntityId: srcEntityId,
            direction: "R",
            entityId: tgtEntityId,
        });
    } else {
        property.push({
            name: chance.word(),
            value: chance.word(),
            entityId: srcEntityId,
        });
    }

    return { property };
}

async function report() {
    console.log("");
    let collections = await models.collection.findAndCountAll();
    console.log("Number of collections created", collections.count);

    let entities = await models.entity.count();
    console.log("Total number of entities created", entities);

    const properties = await models.property.count();
    console.log(`Total number of properties created: ${properties}`);
}
