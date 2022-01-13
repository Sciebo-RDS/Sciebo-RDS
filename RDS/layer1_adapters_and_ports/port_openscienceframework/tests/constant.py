req = {
    "userId": "admin",
    "metadata": {
        "@context": [
            "https://w3id.org/ro/crate/1.0/context",
            {
                "@vocab": "https://schema.org/",
                "osfcategory": "https://www.research-data-services.org/jsonld/osfcategory",
                "zenodocategory": "https://www.research-data-services.org/jsonld/zenodocategory",
            },
        ],
        "@graph": [
            {
                "@id": "ro-crate-metadata.json",
                "@type": "CreativeWork",
                "about": {"@id": "./"},
                "identifier": "ro-crate-metadata.json",
                "conformsTo": {"@id": "https://w3id.org/ro/crate/1.0"},
                "license": {"@id": "https://creativecommons.org/licenses/by-sa/3.0"},
                "description": "Made with Describo: https://uts-eresearch.github.io/describo/",
            },
            {
                "@type": "Dataset",
                "datePublished": "2020-09-29T22:00:00.000Z",
                "name": ["testtitle"],
                "description": ["Beispieltest. Ganz viel\n\nasd mit umbruch"],
                "creator": [
                    {"@id": "#edf6055e-9985-4dfe-9759-8f1aa640d396"},
                    {"@id": "#ac356e5f-fb71-400e-904e-a473c4fc890d"},
                ],
                "zenodocategory": "publication/thesis",
                "osfcategory": "analysis",
                "@id": "./",
            },
            {
                "@type": "Person",
                "@reverse": {"creator": [{"@id": "./"}]},
                "name": "Peter Heiss",
                "familyName": "Heiss",
                "givenName": "Peter",
                "affiliation": [{"@id": "#4bafacfd-e123-44dc-90b9-63f974f85694"}],
                "@id": "#edf6055e-9985-4dfe-9759-8f1aa640d396",
            },
            {
                "@type": "Organization",
                "name": "WWU",
                "@reverse": {
                    "affiliation": [{"@id": "#edf6055e-9985-4dfe-9759-8f1aa640d396"}]
                },
                "@id": "#4bafacfd-e123-44dc-90b9-63f974f85694",
            },
            {
                "@type": "Person",
                "name": "Jens Stegmann",
                "familyName": "Stegmann",
                "givenName": "Jens",
                "email": "",
                "@reverse": {"creator": [{"@id": "./"}]},
                "@id": "#ac356e5f-fb71-400e-904e-a473c4fc890d",
            },
        ],
    },
}

result = {
    "data": {
        "type": "nodes",
        "attributes": {
            "description": "Beispieltest. Ganz viel  asd mit umbruch",
            "category": "analysis",
            "title": "testtitle",
        },
    }
}
