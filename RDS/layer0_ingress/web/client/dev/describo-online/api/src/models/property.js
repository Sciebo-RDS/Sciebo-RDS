"use strict";

module.exports = function (sequelize, DataTypes) {
    let Property = sequelize.define(
        "property",
        {
            id: {
                primaryKey: true,
                type: DataTypes.UUID,
                allowNull: false,
                defaultValue: DataTypes.UUIDV4,
            },
            name: {
                type: DataTypes.TEXT,
                allowNull: false,
            },
            definition: {
                type: DataTypes.JSON,
            },
            sequenceNumber: {
                type: DataTypes.INTEGER,
                allowNull: true,
            },
            tgtEntityId: {
                type: DataTypes.UUID,
            },
            value: {
                type: DataTypes.TEXT,
            },
            direction: {
                type: DataTypes.ENUM(["F", "R"]),
                allowNull: true,
            },
        },
        {
            timestamps: true,
            indexes: [{ fields: ["entityId"] }, { fields: ["tgtEntityId"] }],
        }
    );
    Property.associate = function (models) {
        Property.belongsTo(models.entity, { foreignKey: { allowNull: false } });
    };

    return Property;
};
