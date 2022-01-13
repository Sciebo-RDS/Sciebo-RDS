"use strict";

module.exports = function (sequelize, DataTypes) {
    let User = sequelize.define(
        "user",
        {
            id: {
                primaryKey: true,
                type: DataTypes.UUID,
                allowNull: false,
                defaultValue: DataTypes.UUIDV4,
            },
            email: {
                type: DataTypes.STRING,
                allowNull: false,
                validate: {
                    isEmail: true,
                },
                unique: true,
            },
            name: {
                type: DataTypes.STRING,
                allowNull: false,
                defaultValue: "",
            },
        },
        {
            timestamps: true,
        }
    );
    User.associate = function (models) {
        User.hasOne(models.session, { onDelete: "CASCADE" });
        User.belongsToMany(models.collection, {
            through: models.collection_user,
            foreignKey: "userId",
            otherKey: "collectionId",
        });
        User.belongsToMany(models.entity, {
            through: models.user_entity,
            foreignKey: "userId",
            otherKey: "entityId",
        });
        User.hasMany(models.template, { foreignKey: { allowNull: false }, onDelete: "CASCADE" });
    };

    return User;
};
