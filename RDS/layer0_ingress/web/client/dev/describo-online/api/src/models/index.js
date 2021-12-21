"use strict";

const fs = require("fs");
const path = require("path");
const basename = path.basename(__filename);
const Sequelize = require("sequelize");
const models = {};

let config = {
    db: {
        username: process.env.DB_USER,
        password: process.env.DB_PASSWORD,
        host: process.env.DB_HOST,
        port: process.env.DB_PORT,
        dialect: "postgres",
        database: process.env.DB_DATABASE,
        logging: false,
    },
    pool: {
        max: 20,
        min: 10,
        acquire: 30000,
        idle: 10000,
    },
};

let sequelize = new Sequelize(
    config.db.database,
    config.db.username,
    config.db.password,
    config.db
);

let modules = [
    require("./collection.js"),
    require("./collection_entity.js"),
    require("./collection_user.js"),
    require("./entity.js"),
    require("./entity_properties.js"),
    require("./property.js"),
    require("./user.js"),
    require("./template.js"),
    require("./session.js"),
    require("./user_entity.js"),
    require("./profile.js"),
];

// Initialize models
modules.forEach((module) => {
    const model = module(sequelize, Sequelize, config);
    models[model.name] = model;
});

// Apply associations
Object.keys(models).forEach((key) => {
    if ("associate" in models[key]) {
        models[key].associate(models);
    }
});

models.sequelize = sequelize;
models.Sequelize = Sequelize;

module.exports = models;
