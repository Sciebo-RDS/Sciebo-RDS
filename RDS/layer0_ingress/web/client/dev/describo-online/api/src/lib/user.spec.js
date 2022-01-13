import "regenerator-runtime";
import {
    getUser,
    createUser,
    getUserSession,
    createUserSession,
    updateUserSession,
    destroyUserSession,
} from "./user";
import models from "../models";
import { isMatch } from "lodash";
var chance = require("chance").Chance();

describe("Test user management operations", () => {
    afterAll(async () => {
        await models.sequelize.close();
    });
    test("it should be able to create a user", async () => {
        const email = "test@test.com";
        const name = "test user";

        let user = await createUser({ email, name });
        let u = (await models.user.findOne({ where: { email } })).get();
        expect(isMatch(user, u)).toBeTrue;

        await models.user.destroy({ where: { email } });
    });
    test("it should be able to find an existing user", async () => {
        const email = "test2@test.com";
        const name = "test user 2";

        let user = await createUser({ email, name });
        let u = await getUser({ email });
        expect(isMatch(user, u)).toBeTrue;

        u = await getUser({ id: user.id });
        expect(isMatch(user, u)).toBeTrue;

        await models.user.destroy({ where: { email } });
    });
    test("it should be able to create a session for a user", async () => {
        const email = "test3@test.com";
        const name = "test user 3";
        const session = {
            a: "b",
        };

        let user = await createUser({ email, name });
        let s = await createUserSession({ email, data: session });
        expect(s.data).toEqual(session);

        await models.user.destroy({ where: { email } });
        await models.session.destroy({ where: { id: s.id } });
    });
    test("it should be able to create an okta session for a user", async () => {
        const email = chance.email();
        const name = chance.word();
        const session = { a: "b" };
        const oktaToken = chance.word();
        let oktaExpiry = new Date();
        oktaExpiry = oktaExpiry.setSeconds(oktaExpiry.getSeconds() + 10);
        let user = await createUser({ email, name });
        let s = await createUserSession({ email, data: session, oktaToken, oktaExpiry });
        expect(s.data).toEqual(session);

        await models.user.destroy({ where: { email } });
        await models.session.destroy({ where: { id: s.id } });
    });
    test("it should be able to get a session using the session id", async () => {
        const email = chance.email();
        const name = chance.word();
        let session = { a: "b" };
        let user = await createUser({ email, name });
        let s = await createUserSession({ email, data: session });

        session = await getUserSession({ sessionId: s.id });
        expect(Object.keys(session).sort()).toEqual(["expiresAt", "session", "user"]);
        expect(session.user.id).toEqual(user.id);

        await models.user.destroy({ where: { email } });
        await models.session.destroy({ where: { id: s.id } });
    });
    test("it should be able to get a session by email", async () => {
        const email = chance.email();
        const name = chance.word();
        let session = { a: "b" };
        let user = await createUser({ email, name });
        let s = await createUserSession({ email, data: session });

        session = await getUserSession({ email });
        expect(Object.keys(session).sort()).toEqual(["expiresAt", "session", "user"]);
        expect(session.user.id).toEqual(user.id);

        await models.user.destroy({ where: { email } });
        await models.session.destroy({ where: { id: s.id } });
    });
    test("it should be able to get a session using the oktaToken", async () => {
        const email = chance.email();
        const name = chance.word();
        let session = { a: "b" };
        const oktaToken = chance.word();
        let oktaExpiry = new Date();
        oktaExpiry = oktaExpiry.setSeconds(oktaExpiry.getSeconds() + 10);
        let user = await createUser({ email, name });
        let s = await createUserSession({ email, data: session, oktaToken, oktaExpiry });

        session = await getUserSession({ oktaToken });
        expect(Object.keys(session).sort()).toEqual(["expiresAt", "session", "user"]);
        expect(session.user.id).toEqual(user.id);

        await models.user.destroy({ where: { email } });
        await models.session.destroy({ where: { id: s.id } });
    });
    test("it should find an expired session when looking up by session id", async () => {
        const email = chance.email();
        const name = chance.word();
        let session = { a: "b" };
        let user = await createUser({ email, name });
        let s = await createUserSession({ email, data: session });

        let date = new Date();
        date.setDate(date.getDate() - 10);

        s = await models.session.findOne({ where: { id: s.id } });
        await s.update({ createdAt: date });

        session = await getUserSession({ sessionId: session.id });
        expect(session).toEqual({ session: null, user: null });

        await models.user.destroy({ where: { email } });
        await models.session.destroy({ where: { id: s.id } });
    });
    test("it should not be able to find a session", async () => {
        const email = chance.email();
        const name = chance.word();
        let session = { a: "b" };
        let user = await createUser({ email, name });
        let s = await createUserSession({ email, data: session });

        session = await getUserSession({ oktaToken: "xxxy" });
        expect(session).toEqual({ session: null, user: null });

        await models.user.destroy({ where: { email } });
        await models.session.destroy({ where: { id: s.id } });
    });
    test("it should wipe a pre-existing session", async () => {
        const email = chance.email();
        const name = chance.word();
        let session = { a: "b" };
        let user = await createUser({ email, name });
        let s = await createUserSession({ email, data: session });
        session = { b: "c" };
        s = await createUserSession({ email, data: session });

        expect((await getUserSession({ email })).session.data).toEqual(session);

        await models.user.destroy({ where: { email } });
        await models.session.destroy({ where: { id: s.id } });
    });
    test("it should update an existing session with new data", async () => {
        const email = chance.email();
        const name = chance.word();
        let session = { a: "b" };
        let user = await createUser({ email, name });
        let s = await createUserSession({ email, data: session });
        session = { b: "c" };
        s = await updateUserSession({ sessionId: s.id, email, data: { b: "c" } });
        expect(s.data).toEqual({ a: "b", b: "c" });

        s = await updateUserSession({ sessionId: s.id, email, oktaToken: "a", oktaExpiry: "b" });
        expect(s.oktaToken).toEqual("a");
        expect(s.oktaExpiry).toEqual("b");

        await models.user.destroy({ where: { email } });
        await models.session.destroy({ where: { id: s.id } });
    });
    test("it should be able to destroy a session for a user", async () => {
        const email = "test4@test.com";
        const name = "test user 4";
        const session = {
            a: "b",
        };

        let user = await createUser({ email, name });
        let s = await createUserSession({ email, data: session });
        expect(s.data).toEqual(session);

        await destroyUserSession({ email });

        await models.user.destroy({ where: { email } });
    });
    test("it should find an existing user session", async () => {
        const email = "test5@test.com";
        const name = "test user 5";
        const session = {
            a: "b",
        };

        let user = await createUser({ email, name });
        let s = await createUserSession({ email, data: session });
        expect(s.data).toEqual(session);

        s = await getUserSession({ email });
        expect(s.session.data).toEqual(session);

        await models.user.destroy({ where: { email } });
    });
    test("it should not find a session for a user", async () => {
        const email = "test6@test.com";
        const name = "test user 6";
        const session = {
            a: "b",
        };

        let user = await createUser({ email, name });
        let s = await getUserSession({ email });
        expect(s.session).toEqual(null);
        expect(s.user).toEqual(null);

        await models.user.destroy({ where: { email } });
    });
});
