const { range, round } = require("lodash");
const ss = require("simple-statistics");
const {
    insertEntity,
    removeEntity,
    associate,
    attachProperty,
    findEntity,
} = require("../src/lib/entities");
const { removeCollection } = require("../src/lib/collections");
const models = require("../src/models");
const { spawn } = require("child_process");

const runs = 30;

let collection;

describe.skip("test insertion / deletion operations", () => {
    beforeAll(async () => {
        await models.sequelize.sync();
        collection = await models.collection.create({
            name: "test collection",
        });
    });
    afterAll(async () => {
        collection.destroy();
    });

    test("test inserting an entity into a collection", async () => {
        let times = [];
        for (let i of range(runs)) {
            let entityA = {
                "@id": "1",
                "@type": "Person",
                name: "A",
            };
            const t0 = performance.now();
            entityA = await insertEntity({
                entity: entityA,
                collectionId: collection.id,
            });
            const t1 = performance.now();
            times.push(t1 - t0);
            await removeEntity({ id: entityA.id });
        }
        log("create a new entity", times);
    });

    test("test creating and linking a property to an entity collection", async () => {
        let times = [];
        for (let i of range(runs)) {
            let entityA = {
                "@id": "1",
                "@type": "Person",
                name: "A",
            };
            entityA = await insertEntity({
                entity: entityA,
                collectionId: collection.id,
            });
            const t0 = performance.now();
            await attachProperty({
                entity: entityA,
                property: "author",
                value: "x",
            });
            const t1 = performance.now();
            times.push(t1 - t0);
            await removeEntity({ id: entityA.id });
        }
        log("create a new property", times);
    });

    test("test linking two entities in a collection", async () => {
        let times = [];
        for (let i of range(runs)) {
            let entityA = {
                "@id": "1",
                "@type": "Person",
                name: "A",
            };
            let entityB = {
                "@id": "2",
                "@type": "Person",
                name: "B",
            };
            entityA = await insertEntity({
                entity: entityA,
                collectionId: collection.id,
            });
            entityB = await insertEntity({
                entity: entityB,
                collectionId: collection.id,
            });
            const t0 = performance.now();
            await associate({
                entity: entityA,
                property: "author",
                tgtEntity: entityB,
            });
            const t1 = performance.now();
            times.push(t1 - t0);
            await removeEntity({ id: entityA.id });
            await removeEntity({ id: entityB.id });
        }
        log("link two entities in a collection", times);
    });

    test("remove an entity from a collection", async () => {
        let times = [];
        for (let i of range(runs)) {
            let entityA = {
                "@id": "1",
                "@type": "Person",
                name: "A",
            };
            entityA = await insertEntity({
                entity: entityA,
                collectionId: collection.id,
            });
            const t0 = performance.now();
            await removeEntity({ id: entityA.id });
            const t1 = performance.now();
            times.push(t1 - t0);
        }
        log("remove entity from collection", times);
    });

    test("lookup an entity by @id", async () => {
        let times = [];
        let entityA = {
            "@id": "1",
            "@type": "Person",
            name: "A",
        };
        await insertEntity({
            entity: entityA,
            collectionId: collection.id,
        });
        let result;
        for (let i of range(runs)) {
            const t0 = performance.now();
            result = await findEntity({ "@id": entityA["@id"] });
            const t1 = performance.now();
            times.push(t1 - t0);
        }
        await removeEntity({ id: result[0].id });
        log("find entity by @id", times);
    });

    test("lookup an entity by collection id and @id", async () => {
        let times = [];
        let entityA = {
            "@id": "1",
            "@type": "Person",
            name: "A",
        };
        await insertEntity({
            entity: entityA,
            collectionId: collection.id,
        });
        let result;
        for (let i of range(runs)) {
            const t0 = performance.now();
            result = await findEntity({
                "@id": entityA["@id"],
                collectionId: collection.id,
            });
            const t1 = performance.now();
            times.push(t1 - t0);
        }
        await removeEntity({ id: result[0].id });
        log("find entity by collectionId and @id", times);
    });

    test("lookup entities by collection id and @type", async () => {
        let times = [];
        let entityA = {
            "@id": "1",
            "@type": "Person",
            name: "A",
        };
        await insertEntity({
            entity: entityA,
            collectionId: collection.id,
        });
        let result;
        for (let i of range(runs)) {
            const t0 = performance.now();
            result = await findEntity({
                "@type": entityA["@type"],
                collectionId: collection.id,
            });
            const t1 = performance.now();
            times.push(t1 - t0);
        }
        result = await findEntity({
            "@id": entityA["@id"],
            collectionId: collection.id,
        });
        await removeEntity({ id: result[0].id });
        log("find entities by collectionId and @type", times);
    });
});

describe.skip("test whole collection removal", () => {
    test("test time taken to remove a collection with 10 entities", async () => {
        let times = [];
        for (let i in range(2)) {
            times.push(
                await runCleanupTest(
                    "N_ENTITIES_PER_COLLECTION=10 node ./dbTest/populate-db.js"
                )
            );
        }
        log("time to remove collection", times);
    }, 50000);
    test("test time taken to remove a collection with 100 entities", async () => {
        let times = [];
        for (let i in range(2)) {
            times.push(
                await runCleanupTest(
                    "N_ENTITIES_PER_COLLECTION=100 node ./dbTest/populate-db.js"
                )
            );
        }
        log("time to remove collection", times);
    }, 50000);
    test("test time taken to remove a collection with 200 entities", async () => {
        let times = [];
        for (let i in range(2)) {
            times.push(
                await runCleanupTest(
                    "N_ENTITIES_PER_COLLECTION=200 node ./dbTest/populate-db.js"
                )
            );
        }
        log("time to remove collection", times);
    }, 50000);
    test("test time taken to remove a collection with 400 entities", async () => {
        let times = [];
        for (let i in range(2)) {
            times.push(
                await runCleanupTest(
                    "N_ENTITIES_PER_COLLECTION=400 node ./dbTest/populate-db.js"
                )
            );
        }
        log("time to remove collection", times);
    }, 70000);
});

async function runCleanupTest(cmd) {
    await new Promise((resolve) => {
        const ls = spawn(cmd, {
            shell: true,
        });
        ls.stdout.on("data", (d) => {
            // console.log(d.toString("utf8"));
        });
        ls.on("close", (code) => {
            console.log("data load complete");
            resolve();
        });
    });

    let collection = await models.collection.findOne();
    const t0 = performance.now();
    await removeCollection({ id: collection.id });
    const t1 = performance.now();
    return t1 - t0;
}

function log(msg, times) {
    console.log(
        `${msg}\nMean:   ${round(ss.mean(times), 3)}\nStdDev: ${round(
            ss.standardDeviation(times),
            3
        )}`
    );
}
