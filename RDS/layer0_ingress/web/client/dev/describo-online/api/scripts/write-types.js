const { readJson, writeFile, ensureDir } = require("fs-extra");
const { flattenDeep, orderBy, has, compact, uniq, uniqBy, isString, cloneDeep } = require("lodash");
const path = require("path");
const { expand } = require("jsonld");

const {
    schema,
    roCrateAdditions,
    crateContext,
    simpleDataTypes,
    selectDataTypes,
    rename,
    addTypesToProperty,
    compoundTypes,
} = require("./configuration");

let classes = {};
let properties = {};
let other = {};

const defs = {
    property: "http://www.w3.org/1999/02/22-rdf-syntax-ns#Property",
    class: "http://www.w3.org/2000/01/rdf-schema#Class",
    label: "http://www.w3.org/2000/01/rdf-schema#label",
    inverse: "http://schema.org/inverseOf",
    range: "http://schema.org/rangeIncludes",
    domain: "http://schema.org/domainIncludes",
    subclass: "http://www.w3.org/2000/01/rdf-schema#subClassOf",
    help: "http://www.w3.org/2000/01/rdf-schema#comment",
};

(async () => {
    await ensureDir("./types");

    await extractSchemaOrgData();
    mapClassHierarchies();
    collapseNames();
    sortClassData();
    addCompoundTypeDefinitions();
    let context = await extractCrateContext();
    // diffSchemaOrgAndCrateContext({ context });
    await writeTypeDefinitions();
    // console.log(JSON.stringify(classes.CreativeWork, null, 2));
})();

function stripSchemaPath(text) {
    if (text) return text.split("/").pop();
}

async function extractSchemaOrgData() {
    const jsonld = await expand(await readJson(schema));
    const additions = await expand(await readJson(roCrateAdditions));

    let graph = [...jsonld, ...additions.filter((e) => e["@id"] !== "ro-crate-metadata.json")];
    extractClassesAndProperties({ graph });
    mapPropertiesToClasses();
}

function mapClassHierarchies() {
    Object.keys(classes).forEach((className) => {
        classes[className].hierarchy = uniq(
            compact(flattenDeep([className, getParent(className)])).reverse()
        ).reverse();
    });
    function getParent(className) {
        if (classes[className] && classes[className].subClassOf) {
            return classes[className].subClassOf.map((c) => {
                return c ? [c, getParent(c)] : c;
            });
        }
    }
}

function collapseNames() {
    Object.keys(classes).forEach((name) => {
        if (classes[name].subClassOf && classes[name].subClassOf.length) {
            classes[name].subClassOf = classes[name].subClassOf.map((n) => stripSchemaPath(n));
        }
        if (classes[name].hierarchy && classes[name].hierarchy.length) {
            classes[name].hierarchy = classes[name].hierarchy.map((n) => stripSchemaPath(n));
        }
    });
}

function sortClassData() {
    Object.keys(classes).forEach((c) => {
        classes[c].inputs = uniqBy(classes[c].inputs, "name");
        classes[c].inputs = orderBy(classes[c].inputs, "name");
        classes[c].linksTo = classes[c].linksTo.sort();
    });
}

function addCompoundTypeDefinitions() {
    compoundTypes.forEach((type) => {
        let types = type.split(", ");
        let hierarchy = uniq(
            flattenDeep(types.map((type) => classes[type].hierarchy)).reverse()
        ).reverse();
        classes[type] = {
            name: type,
            subClassOf: [],
            allowAdditionalProperties: false,
            inputs: [],
            linksTo: [],
            hierarchy,
        };
    });
}

function extractClassesAndProperties({ graph }) {
    // separate classes and properties
    graph.forEach((entry) => {
        // entry["@id"] = stripSchemaPath(entry["@id"]);
        let name = stripSchemaPath(entry["@id"]);
        // const name = entry["@id"];

        if (entry["@type"].includes(defs.property)) {
            if (rename.properties[name]) {
                name = rename.properties[name];
            }

            let range = getValue(entry[defs.range]).map((e) =>
                rename.classes[e] ? rename.classes[e] : e
            );
            if (addTypesToProperty[name]) {
                range = [...range, ...addTypesToProperty[name].types];
                range = uniq(range).sort();
            }

            properties[name] = {
                id: entry["@id"],
                name: name,
                type: "property",
                help: getValue(entry[defs.help], true),
                domain: getValue(entry[defs.domain]),
                range,
                inverseOf: getValue(entry[defs.inverse]),
            };
        } else if (entry["@type"].includes(defs.class)) {
            // is it a class?

            //  rename the class if required
            if (rename.classes[name]) {
                name = rename.classes[name];
            }
            let subClassOf = getValue(entry[defs.subclass]).map((e) =>
                rename.classes[e] ? rename.classes[e] : e
            );
            classes[name] = {
                id: entry["@id"],
                name,
                help: getValue(entry[defs.help], true),
                subClassOf,
                allowAdditionalProperties: false,
                inputs: [],
                linksTo: [],
            };
        } else {
            // is it something else?
            other[name] = entry;
        }
    });
}

function mapPropertiesToClasses() {
    // map properties back in to classes
    Object.keys(properties).forEach((property) => {
        property = properties[property];
        // console.log(property);
        const foundIn = property.domain ? property.domain.map((e) => stripSchemaPath(e)) : [];
        foundIn.forEach((target) => {
            // console.log("target", target);
            if (rename.classes[target]) {
                target = rename.classes[target];
                // console.log(target, property.name, property.range);
            }

            const complexTypes = property.range
                .map((t) => stripSchemaPath(t))
                .filter((t) => !simpleDataTypes.includes(t))
                .filter((t) => !selectDataTypes.includes(t));

            const simpleTypes = property.range
                .map((t) => stripSchemaPath(t))
                .filter((t) => simpleDataTypes.includes(t));
            // console.log(property.name, simpleTypes);

            const selectTypes = property.range
                .map((t) => stripSchemaPath(t))
                .filter((t) => !has(classes, t))
                .filter((t) => selectDataTypes.includes());

            // console.log(property.name, complexTypes, simpleTypes, selectTypes);

            // link this property to the relevant class
            const definition = {
                id: property.id,
                name: property.name,
                help: property.help,
            };

            let targetTypes = [];
            let input = {};

            if (complexTypes.length) {
                // complex types like Person and Organization ie Classes
                targetTypes.push(complexTypes);
            }
            if (selectTypes.length) {
                // map a boolean to true / false
                input = {
                    ...definition,
                    "@type": "Select",
                    options: [true, false],
                };
            }
            if (simpleTypes.length) {
                // simple types like Date, Text
                targetTypes.push(simpleTypes);
            }

            try {
                if (!selectTypes.length) {
                    targetTypes = flattenDeep(targetTypes);
                    classes[target].inputs.push({
                        ...definition,
                        multiple: true,
                        type: targetTypes.length ? targetTypes : ["Text"],
                    });
                } else {
                    classes[target].inputs.push(input);
                }
            } catch (error) {
                console.log("can't find target", target);
            }
            // use the acceptable types for this property
            //  to link the class reverse
            complexTypes.forEach((type) => {
                if (classes[type]) {
                    classes[type].linksTo.push(target);
                }
            });
        });
    });
}

async function extractCrateContext() {
    const jsonld = await readJson(crateContext);
    return jsonld["@context"];
}

async function writeTypeDefinitions() {
    // order class inputs and write to file
    let searchableIndex = [];
    let index = {};
    Object.keys(classes).forEach(async (c) => {
        const item = classes[c];
        item.linksTo = uniq(item.linksTo);
        item.inputs = orderBy(item.inputs, "property");

        index[item.name] = item;

        searchableIndex.push({
            name: c,
            help: item.help,
        });
    });
    await writeFile(path.join("types", "type-definitions.json"), JSON.stringify(index, null, 2));
    // console.log(JSON.stringify(index, null, 2));
    await writeFile(
        path.join("types", "type-definitions-lookup.json"),
        JSON.stringify(searchableIndex)
    );
}

function getValue(item, collapse) {
    if (!item) return [];
    let value = item.map((e) => {
        if (e["@id"]) return e["@id"];
        if (e["@value"]) return e["@value"];
    });
    value = compact(value);
    if (collapse) return value.join(", ");
    return value.map((e) => stripSchemaPath(e));
}

function diffSchemaOrgAndCrateContext({ context }) {
    let extra = {};
    const stats = {
        classes: Object.keys(classes).length,
        properties: Object.keys(properties).length,
        other: Object.keys(other).length,
        context: Object.keys(context).length,
    };
    const diff = stats.context - stats.classes - stats.properties - stats.other;
    console.log(`n classes ${stats.classes}`);
    console.log(`n properties: ${stats.properties}`);
    console.log(`n other things ${stats.other}`);
    console.log(`n context: ${stats.context}`);
    console.log(`Entries without definition: ${diff}`);
    console.log("");

    // console.log(properties.sportsTeam);

    for (let [key, value] of Object.entries(context)) {
        if (!classes[key] && !other[key] && !properties[key]) extra[key] = value;
    }
    console.log("Crate context entries without definitions in schema.org");
    console.log(extra);
}
