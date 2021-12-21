import "regenerator-runtime";
import {
    getProfile,
    createProfile,
    updateProfile,
    lookupProfile,
    getTypeDefinition,
} from "./profile";
import { insertCollection } from "./collections";
import models from "../models";
const chance = require("chance").Chance();

describe("Test profile operations", () => {
    beforeEach(async () => {
        await models.profile.truncate({ cascade: true });
        await models.collection.truncate({ cascade: true });
    });
    afterAll(async () => {
        await models.sequelize.close();
    });
    test("it should be able to get a profile", async () => {
        const name = chance.name();
        let collection = {
            name,
            description: "",
            metadata: {},
        };
        collection = await insertCollection(collection);
        let profile = {
            name,
            profile: {},
        };
        profile = await createProfile({
            ...profile,
            collectionId: collection.id,
        });
        profile = await getProfile({ collectionId: collection.id });
        expect(profile.name).toEqual(name);
    });
    test("it should be able to create a profile", async () => {
        const name = chance.name();
        let collection = {
            name,
            description: "",
            metadata: {},
        };
        collection = await insertCollection(collection);
        let profile = {
            name,
            profile: {},
        };
        profile = await createProfile({
            ...profile,
            collectionId: collection.id,
        });
        expect(profile.collectionId).toEqual(collection.id);
        expect(profile.name).toEqual(name);
    });
    test("it should fail to create a profile - null collectionId", async () => {
        const name = chance.name();
        let collection = {
            name,
            description: "",
            metadata: {},
        };
        collection = await insertCollection(collection);
        let profile = {
            name,
            profile: {},
        };
        try {
            profile = await createProfile({
                ...profile,
            });
        } catch (error) {
            expect(error.message).toEqual("notNull Violation: profile.collectionId cannot be null");
        }
    });
    test("it should be able to update a profile", async () => {
        let name = chance.name();
        let collection = {
            name,
            description: "",
            metadata: {},
        };
        collection = await insertCollection(collection);
        let profile = {
            name,
            profile: {},
        };
        profile = await createProfile({
            ...profile,
            collectionId: collection.id,
        });
        name = chance.name();
        profile = await updateProfile({ profileId: profile.id, name });
        expect(profile.name).toEqual(name);
        name = chance.name();
        profile = await updateProfile({
            profileId: profile.id,
            name,
            profile: { key: "value" },
        });
        expect(profile.name).toEqual(name);
        expect(profile.profile).toEqual({ key: "value" });
    });
    test("it should be able to lookup the default profile for matching type definitions", async () => {
        let types = await lookupProfile({ query: "Airline" });
        expect(types.length).toBe(3);
    });
    test("it should be able to get a type definition", async () => {
        let type = await getTypeDefinition({ name: "Airline" });
        expect(type.name).toBe("Airline");
    });
});
