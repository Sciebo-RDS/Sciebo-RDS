const models = require("../models");
const { Op } = require("sequelize");
import { getEntity, getEntityProperties, insertEntity, attachProperty } from "./entities";
import { getTypeDefinition } from "./profile";
import { groupBy } from "lodash";
import { Crate } from "./crate";

export async function insertTemplate({ userId, entityId, collectionId, name }) {
    if (entityId) {
        // locate the entity, freeze it and store it as a template
        let entity = await getEntity({ id: entityId, collectionId });
        let { properties } = await getEntityProperties({ id: entityId, collectionId });
        properties = properties.filter((p) => p.value);
        properties = groupBy(properties, "name");

        entity = {
            eid: entity.eid,
            etype: entity.etype,
            name: entity.name,
        };
        Object.keys(properties).forEach((property) => {
            entity[property] = properties[property].map((p) => p.value);
        });

        let template = await models.template.findOne({
            where: { userId, eid: entity.eid, etype: entity.etype, name: entity.name },
        });
        if (!template) return await models.template.create({ userId, ...entity, src: entity });
        return template;
    } else {
        // find the collection, freeze it and store it as a template
        let crate = new Crate();
        crate = await crate.exportCollectionAsROCrate({ collectionId });
        return await models.template.create({ userId, name, src: crate });
    }
}

export async function addTemplate({ userId, collectionId, templateId }) {
    let template = (await models.template.findOne({ where: { id: templateId, userId } })).src;
    let entity = {
        name: template.name,
        eid: template.eid,
        etype: template.etype,
    };
    try {
        entity = await insertEntity({ entity, collectionId });
        const typeDefinition = await getTypeDefinition({ collectionId, name: template.etype });
        let properties = Object.keys(template).filter((p) => !["eid", "etype", "name"].includes(p));
        for (let property of properties) {
            let definition = typeDefinition.inputs.filter((i) => i.name === property)[0];
            for (let entry of template[property]) {
                await attachProperty({
                    collectionId,
                    entityId: entity.id,
                    property,
                    value: entry,
                    typeDefinition: definition,
                });
            }
        }
    } catch (error) {
        entity = (await models.entity.findOne({ where: { eid: entity.eid, collectionId } })).get();
    }
    return { entity };
}

export async function replaceCrateWithTemplate({ userId, collectionId, templateId }) {
    await models.entity.destroy({ where: { collectionId } });
    let collection = await models.collection.findOne({ where: { id: collectionId } });
    collection.metadata = {};
    collection = await collection.save();

    const template = (await getTemplate({ userId, templateId })).src;

    let crate = new Crate();
    crate = await crate.importCrateIntoDatabase({ collection, crate: template, sync: true });
}

export async function removeTemplate({ templateId, userId }) {
    await models.template.destroy({ where: { id: templateId, userId } });
}

export async function getTemplate({ userId, templateId }) {
    return await models.template.findOne({ where: { id: templateId, userId } });
}

export async function getTemplates({
    userId,
    filter,
    type,
    page = 0,
    limit = 10,
    orderBy = ["etype", "name"],
    orderDirection = "asc",
}) {
    let andClause = [{ userId }];
    if (type) andClause.push({ etype: type });
    let orClause = [];
    if (filter) {
        orClause = [
            { eid: { [Op.iLike]: `%${filter}%` } },
            { name: { [Op.iLike]: `%${filter}%` } },
        ];
    }
    if (orClause.length) {
        andClause.push({ [Op.or]: orClause });
    }

    let where = {
        [Op.and]: andClause,
    };
    where = {
        where,
        distinct: true,
        offset: page,
        limit,
        order: orderBy.map((p) => [p, orderDirection]),
    };

    let results = await models.template.findAndCountAll(where);
    let templates = results.rows.map((t) => t.get());
    return { templates, total: results.count };
}
