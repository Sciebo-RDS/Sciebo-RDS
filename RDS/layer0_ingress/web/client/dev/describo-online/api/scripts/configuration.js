module.exports = {
    // the name of the schema.org jsonld file - expected to be in this folder
    schema: "schema.org.jsonld",

    // the name of the extra ro crate stuff to be added - expected to be in this folder
    roCrateAdditions: "ro-crate-additional-schema.jsonld",

    // the name of the ro crate context - expected to be in this folder
    crateContext: "crate-context.jsonld",

    // simple data types - ie not entities
    simpleDataTypes: ["Text", "Date", "DateTime", "Time", "Number", "Float", "Integer"],

    // classes to be mapped to a switch
    selectDataTypes: ["Boolean"],

    // rules for renaming properties and classes
    //   this happens after the datastructure has been assembled
    rename: {
        classes: {
            MediaObject: "File",
            Periodical: "Journal",
            "models#Object": "RepositoryObject",
            "models#Collection": "RepositoryCollection",
        },
        properties: {
            "models#hasMember": "hasMember",
            "models#hasFile": "hasFile",
        },
    },

    // extra types to be added to specified properties
    addTypesToProperty: {
        hasPart: {
            types: [
                "Dataset",
                "File",
                "File, ImageObject",
                "File, SoftwareSourceCode",
                "File, SoftwareSourceCode, ComputationalWorkflow",
                "RepositoryCollection",
                "RepositoryObject",
                "RepositoryObject, ImageObject",
                "ComputerLanguage, SoftwareApplication",
                "FormalParameter",
            ],
        },
    },

    // special compound type definitions
    compoundTypes: [
        "File, ImageObject",
        "File, SoftwareSourceCode",
        "RepositoryObject, ImageObject",
        "ComputerLanguage, SoftwareApplication",
        "File, SoftwareSourceCode, ComputationalWorkflow",
    ],
};
