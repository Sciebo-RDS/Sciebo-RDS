const models = require("../models");
const { Op } = require("sequelize");
const sequelize = models.sequelize;

module.exports = {
    findCollection,
    insertCollection,
    removeCollection,
};

async function insertCollection({ name, description, metadata }) {
    if (!name) {
        throw new Error("You must provide a collection name");
    }
    return (
        await models.collection.create({
            name,
            description,
            metadata,
        })
    ).get();
}

async function removeCollection({ id }) {
    await sequelize.transaction(async (t) => {
        await models.entity.destroy({
            where: { collectionId: id },
            include: [{ model: models.property }],
            transaction: t,
            cascade: true,
        });
        await models.collection.destroy({
            where: { id },
            transaction: t,
            cascade: true,
        });
    });
}

async function findCollection({ id, name }) {
    let where = {};
    if (id) where.id = id;
    if (name)
        where.name = {
            [Op.substring]: [name],
        };
    let collections = await models.collection.findAll({ where });
    if (collections.length) {
        return collections.map((c) => c.get());
    }
    return [];
}
