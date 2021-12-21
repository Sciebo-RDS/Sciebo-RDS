import "regenerator-runtime";
import models from "../models";
import { createUser, createUserSession } from "../lib/user";
import { refreshOauthTokens } from ".";
import fetchMock from "jest-fetch-mock";
const chance = require("chance").Chance();

fetchMock.enableMocks();

describe("Test refreshing access token stored in user sessions", () => {
    beforeEach(() => {
        fetch.resetMocks();
    });
    afterAll(() => async () => {
        await models.sequelize.close();
    });
    test("it should refresh active user sessions with a valid owncloud access_token and refresh_token", async () => {
        const user = {
            name: chance.word(),
            email: chance.email(),
            session: {
                services: {
                    owncloud: {
                        service: "owncloud",
                        url: "http://owncloud_server:8080/remote.php/dav",
                        folder: "/ro-crate test/",
                        token: {
                            access_token: "r4w7PPN",
                            refresh_token: "RwHe8bK",
                            user_id: "admin",
                            expires_in: 60,
                            expires_at: new Date(new Date().getTime() + 60 * 1000),
                            date: new Date(),
                        },
                    },
                },
            },
        };
        await createUser({ name: user.name, email: user.email });
        let session = await createUserSession({ email: user.email, data: user.session });

        const newSessionData = {
            access_token: "a",
            token_type: "Bearer",
            refresh_token: "b",
            expires_in: 1,
            expires_at: new Date(new Date().getTime() + 60 * 1000),
            user_id: "admin",
            date: new Date(),
        };
        fetch.mockResponseOnce(JSON.stringify(newSessionData));

        await refreshOauthTokens();

        session = await models.session.findOne({ where: { id: session.id } });
        expect(session.data.services.owncloud.token.access_token).toEqual("a");
        expect(session.data.services.owncloud.token.refresh_token).toEqual("b");

        await models.user.destroy({ where: { email: user.email } });
        await models.session.destroy({ where: { id: session.id } });
    });
    test("it should skip refreshing a user session when no refresh_token is present", async () => {
        const user = {
            name: chance.word(),
            email: chance.email(),
            session: {
                services: {
                    owncloud: {
                        service: "owncloud",
                        url: "http://owncloud_server:8080/remote.php/dav",
                        folder: "/ro-crate test/",
                        token: {
                            access_token: "r4w7PPN",
                            user_id: "admin",
                            expires_in: 60,
                            expires_at: new Date(new Date().getTime() + 60 * 1000),
                            date: new Date(),
                        },
                    },
                },
            },
        };
        await createUser({ name: user.name, email: user.email });
        let session = await createUserSession({ email: user.email, data: user.session });

        await refreshOauthTokens();

        session = await models.session.findOne({ where: { id: session.id } });
        expect(session.data.services.owncloud.token.access_token).toEqual("r4w7PPN");

        await models.user.destroy({ where: { email: user.email } });
        await models.session.destroy({ where: { id: session.id } });
    });
});
