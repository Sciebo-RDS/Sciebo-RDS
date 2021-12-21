const { readJson, writeFile, ensureDir } = require("fs-extra");
const { flattenDeep, orderBy, has, compact, uniq, uniqBy, isString, cloneDeep } = require("lodash");
const path = require("path");
const { expand } = require("jsonld");
const args = require("yargs/yargs")(process.argv.slice(2))
    .option("filter", {
        alias: "f",
        describe: "Class name to include - filtering all others out",
        type: "string",
        array: true,
    })
    .option("typeDefinition", {
        describe: "Path to the type definition file",
        type: "string",
        default: path.join(__dirname, "..", "src", "common", "type-definitions.json"),
    }).argv;

let classes = {};
// let properties = {};
// let other = {};

(async () => {
    const typeDefinitions = await readJson(args.typeDefinition);
    for (let key of Object.keys(typeDefinitions)) {
        if (args.filter.includes(key)) {
            classes[key] = typeDefinitions[key];
            typeDefinitions[key].subClassOf?.forEach((s) => {
                classes[s] = typeDefinitions[s];
            });
        }
    }
    // console.log(Object.keys(classes));
    console.log(classes);
    await ensureDir("./types");

    await writeTypeDefinitions();
})();

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
