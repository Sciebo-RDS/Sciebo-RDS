"use strict";

module.exports = function (sequelize, DataTypes) {
    let Profile = sequelize.define(
        "profile",
        {
            id: {
                primaryKey: true,
                type: DataTypes.UUID,
                allowNull: false,
                defaultValue: DataTypes.UUIDV4,
            },
            name: {
                type: DataTypes.STRING,
                allowNull: false,
            },
            profile: {
                type: DataTypes.JSON,
                allowNull: false,
            },
        },
        {
            timestamps: true,
        }
    );
    Profile.associate = function (models) {
        Profile.belongsTo(models.collection, {
            foreignKey: { allowNull: false },
        });
    };

    return Profile;
};
