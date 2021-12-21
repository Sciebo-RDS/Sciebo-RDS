const models = require("../models");
import { readJSON, readJSONSync } from "fs-extra";
import { cloneDeep, flattenDeep, orderBy, uniqBy } from "lodash";
import path from "path";
const typeDefinitions =
    process.env.NODE_ENV !== "development"
        ? readJSONSync("/srv/type-definitions.json")
        : readJSONSync(path.join(__dirname, "..", "common", "type-definitions.json"));
const typeDefinitionsLookup =
    process.env.NODE_ENV !== "development"
        ? readJSONSync("/srv/type-definitions-lookup.json")
        : readJSONSync(path.join(__dirname, "..", "common", "type-definitions-lookup.json"));

export async function getProfile({ collectionId }) {
    return (
        await models.profile.findOne({
            where: { collectionId },
        })
    ).get();
}

export async function lookupProfile({ collectionId, query }) {
    let profile;
    if (collectionId) {
        profile = await models.profile.findOne({
            where: { collectionId },
        });
    }
    if (!profile) {
        profile = typeDefinitionsLookup;
    }
    let re = new RegExp(query, "i");
    let matches = profile.filter((e) => {
        return re.exec(e.name) || re.exec(e.help);
    });
    matches = orderBy(matches, "name");
    return matches;
}

export async function getTypeDefinition({ collectionId, name }) {
    let profile, definitions;
    if (collectionId) {
        profile = await models.profile.findOne({
            where: { collectionId },
        });
        definitions = {};
    }
    if (!profile) {
        definitions = typeDefinitions;
    }

    let typeDefinition;
    let inputs = [];

    name = name.split(", ");
    if (name.length === 1) {
        name = name.pop();
        typeDefinition = definitions[name];
        if (!typeDefinition) return undefined;
        typeDefinition.hierarchy.forEach((e) => {
            inputs.push(cloneDeep(definitions[e].inputs));
        });
    } else {
        name.forEach((n) => {
            typeDefinition = definitions[n];
            if (!typeDefinition) return;
            typeDefinition.hierarchy.forEach((e) => {
                inputs.push(cloneDeep(definitions[e].inputs));
            });
        });
    }

    inputs = flattenDeep(inputs);
    inputs = uniqBy(inputs, "id");
    inputs = orderBy(inputs, "name");

    try {
        typeDefinition.inputs = inputs;
    } catch (error) {
        typeDefinition = {
            name,
            help: "",
            subClassOf: ["Thing"],
            allowAdditionalProperties: false,
            inputs,
        };
    }
    return typeDefinition;
}

export async function createProfile({ name, profile, collectionId }) {
    return (
        await models.profile.create({
            name,
            profile,
            collectionId,
        })
    ).get();
}

export async function updateProfile({ profileId, name, profile }) {
    let update = {};
    if (name) update.name = name;
    if (profile) update.profile = profile;
    await models.profile.update(update, {
        where: { id: profileId },
    });
    return (await models.profile.findOne({ where: { id: profileId } })).get();
}
