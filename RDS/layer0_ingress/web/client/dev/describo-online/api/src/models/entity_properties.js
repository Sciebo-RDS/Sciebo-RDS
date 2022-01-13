"use strict";

module.exports = function (sequelize, DataTypes) {
    var EntityProperties = sequelize.define(
        "entity_properties",
        {},
        {
            timestamps: false,
        }
    );

    return EntityProperties;
};
