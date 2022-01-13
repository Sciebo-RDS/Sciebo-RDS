"use strict";

module.exports = function (sequelize, DataTypes) {
    var CollectionUser = sequelize.define(
        "collection_user",
        {},
        {
            timestamps: false,
        }
    );

    return CollectionUser;
};
