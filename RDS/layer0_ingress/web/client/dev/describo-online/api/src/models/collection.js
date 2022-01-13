"use strict";

module.exports = function (sequelize, DataTypes) {
    let Collection = sequelize.define("collection", {
        id: {
            primaryKey: true,
            type: DataTypes.UUID,
            allowNull: false,
            defaultValue: DataTypes.UUIDV4,
        },
        name: {
            type: DataTypes.STRING,
            allowNull: false,
            validate: {
                notEmpty: true,
            },
        },
        description: {
            type: DataTypes.TEXT,
        },
        metadata: {
            type: DataTypes.JSON,
        },
    });
    Collection.associate = function (models) {
        Collection.hasMany(models.entity, {
            onDelete: "CASCADE",
            foreignKey: { allowNull: false },
        });
        Collection.belongsToMany(models.user, {
            through: models.collection_user,
            foreignKey: "collectionId",
            otherKey: "userId",
            onDelete: "CASCADE",
        });
        Collection.hasOne(models.profile, {
            foreignKey: { allowNull: false },
            onDelete: "CASCADE",
        });
    };
    return Collection;
};
