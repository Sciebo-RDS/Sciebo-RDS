"use strict";

module.exports = function (sequelize, DataTypes) {
    var CollectionEntity = sequelize.define(
        "collection_entity",
        {},
        {
            timestamps: false,
        }
    );

    return CollectionEntity;
};
