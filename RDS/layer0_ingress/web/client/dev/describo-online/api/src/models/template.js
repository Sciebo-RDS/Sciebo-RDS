"use strict";

module.exports = function (sequelize, DataTypes) {
    let Template = sequelize.define(
        "template",
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
            },
            name: {
                type: DataTypes.STRING,
                allowNull: false,
            },
            src: {
                type: DataTypes.JSON,
            },
        },
        {
            timestamps: true,
        }
    );
    Template.associate = function (models) {
        Template.belongsTo(models.user, { foreignKey: { allowNull: false }, onDelete: "CASCADE" });
    };

    return Template;
};
