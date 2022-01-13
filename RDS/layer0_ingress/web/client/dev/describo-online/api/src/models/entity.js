"use strict";

module.exports = function (sequelize, DataTypes) {
    let Entity = sequelize.define(
        "entity",
        {
            id: {
                primaryKey: true,
                type: DataTypes.UUID,
                allowNull: false,
                defaultValue: DataTypes.UUIDV4,
            },
            eid: {
                type: DataTypes.STRING,
            },
            etype: {
                type: DataTypes.STRING,
                allowNull: false,
            },
            hierarchy: {
                type: DataTypes.STRING,
            },
            name: {
                type: DataTypes.STRING,
                defaultValue: "",
            },
            locked: {
                type: DataTypes.BOOLEAN,
                allowNull: false,
                defaultValue: false,
            },
        },
        {
            timestamps: true,
            indexes: [
                {
                    fields: ["collectionId", "etype"],
                },
                {
                    fields: ["collectionId", "hierarchy"],
                },
                {
                    unique: true,
                    fields: ["collectionId", "eid"],
                },
                {
                    fields: ["collectionId", "name"],
                },
            ],
        }
    );
    Entity.associate = function (models) {
        Entity.hasMany(models.property, {
            onDelete: "CASCADE",
            foreignKey: { allowNull: false },
        });
        Entity.belongsTo(models.collection);
    };

    return Entity;
};
