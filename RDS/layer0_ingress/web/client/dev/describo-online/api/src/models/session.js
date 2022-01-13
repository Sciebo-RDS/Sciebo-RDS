"use strict";

module.exports = function (sequelize, DataTypes) {
    let Session = sequelize.define(
        "session",
        {
            id: {
                primaryKey: true,
                type: DataTypes.UUID,
                allowNull: false,
                defaultValue: DataTypes.UUIDV4,
            },
            oktaToken: {
                type: DataTypes.TEXT,
            },
            oktaExpiry: {
                type: DataTypes.STRING,
            },
            data: {
                type: DataTypes.JSON,
            },
            creator: {
                type: DataTypes.STRING,
            },
        },
        {
            timestamps: true,
            indexes: [
                {
                    fields: ["oktaToken"],
                },
            ],
        }
    );
    Session.associate = function (models) {
        Session.belongsTo(models.user);
    };

    return Session;
};
