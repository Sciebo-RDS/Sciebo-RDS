import models from "../models";
import { cloneDeep, omit } from "lodash";
import { demandKnownUser } from "../middleware";
import { loadConfiguration } from "../common";
import OktaJwtVerifier from "@okta/jwt-verifier";
import { postSession, getApplication } from "../lib/session";
import { createUser, createUserSession } from "../lib/user";
import { BadRequestError, UnauthorizedError, ForbiddenError } from "restify-errors";
import {
    readFolderRouteHandler,
    createFolderRouteHandler,
    deleteFolderRouteHandler,
} from "./file-browser";

import {
    getProfileRouteHandler,
    lookupProfileRouteHandler,
    createProfileRouteHandler,
    updateProfileRouteHandler,
    getTypeDefinitionRouteHandler,
} from "./profile";
import {
    getEntityRouteHandler,
    getEntityCountRouteHandler,
    getEntitiesRouteHandler,
    getEntityPropertiesRouteHandler,
    findEntityRouteHandler,
    postEntityRouteHandler,
    putEntityRouteHandler,
    delEntityRouteHandler,
    postEntityPropertyRouteHandler,
    putEntityPropertyRouteHandler,
    delEntityPropertyRouteHandler,
    putEntityAssociateRouteHandler,
    postFilesRouteHandler,
} from "./entity";
import { loadRouteHandler } from "./load";
import {
    getTemplatesRouteHandler,
    getTemplateRouteHandler,
    postTemplateRouteHandler,
    delTemplateRouteHandler,
    postAddTemplateRouteHandler,
    postReplaceCrateWithTemplateRouteHandler,
} from "./template";

import { getOwncloudOauthToken, assembleOwncloudConfiguration } from "../lib/backend-owncloud";

import { getLogger } from "../common/logger";
const log = getLogger();

export function setupRoutes({ server }) {
    server.get("/configuration", getConfiguration);
    server.get("/authenticated", route(isAuthenticated));
    server.post("/session/okta", createOktaSession);
    server.get("/session", route(getSession));
    server.post("/session/application", createApplicationSession);
    server.put("/session/application/:sessionId", updateApplicationSession);
    server.get("/session/configuration/:serviceName", route(getServiceConfiguration));
    server.post("/session/configuration/:serviceName", route(saveServiceConfiguration));
    server.post("/session/get-oauth-token/:serviceName", route(getOauthToken));
    server.post("/folder/create", route(createFolderRouteHandler));
    server.post("/folder/read", route(readFolderRouteHandler));
    server.post("/folder/delete", route(deleteFolderRouteHandler));
    server.get("/definition", route(getTypeDefinitionRouteHandler));
    server.get("/definition/:name", route(getTypeDefinitionRouteHandler));
    server.get("/definition/lookup", route(lookupProfileRouteHandler));
    server.get("/profile/:profileId", route(getProfileRouteHandler));
    server.post("/profile", route(createProfileRouteHandler));
    server.put("/profile/:profileId", route(updateProfileRouteHandler));
    server.post("/load", route(loadRouteHandler));
    server.post("/entity/lookup", route(findEntityRouteHandler));
    server.get("/entity/:entityId", route(getEntityRouteHandler));
    server.get("/entity/:entityId/properties", route(getEntityPropertiesRouteHandler));
    server.get("/entity/count", route(getEntityCountRouteHandler));
    server.get("/entity", route(getEntitiesRouteHandler));
    server.post("/entity", route(postEntityRouteHandler));
    server.put("/entity/:entityId", route(putEntityRouteHandler));
    server.del("/entity/:entityId", route(delEntityRouteHandler));
    server.post("/entity/:entityId/property", route(postEntityPropertyRouteHandler));
    server.put("/entity/:entityId/property/:propertyId", route(putEntityPropertyRouteHandler));
    server.del("/entity/:entityId/property/:propertyId", route(delEntityPropertyRouteHandler));
    server.put("/entity/:entityId/associate", route(putEntityAssociateRouteHandler));
    server.post("/files", route(postFilesRouteHandler));
    server.get("/template", route(getTemplatesRouteHandler));
    server.get("/template/:templateId", route(getTemplateRouteHandler));
    server.post("/template", route(postTemplateRouteHandler));
    server.del("/template/:templateId", route(delTemplateRouteHandler));
    server.post("/template/add", route(postAddTemplateRouteHandler));
    server.post("/template/replace", route(postReplaceCrateWithTemplateRouteHandler));

    if (process.env.NODE_ENV === "development") {
        // this is only for development of the capability to post back on save
        server.post("/save", (req, res, next) => {
            log.debug(`Crate POST'ed: ${req.body["@graph"][0]["@id"]}`);
            res.send({});
            return next();
        });
    }
}

function route(handler) {
    return [demandKnownUser, handler];
}

async function getConfiguration(req, res, next) {
    let configuration = await loadConfiguration();
    res.send({ configuration: configuration.ui });
    return next();
}

async function isAuthenticated(req, res, next) {
    res.send({});
    next();
}

async function createOktaSession(req, res, next) {
    let config = (await loadConfiguration()).ui;

    let token;
    try {
        token = req.headers.authorization.split("okta ").pop();
    } catch (error) {
        log.error(`createOktaSession: issue with authorization header: ${error.message}`);
        return next(new UnauthorizedError("Unable to get authorization from header"));
    }
    const oktaJwtVerifier = new OktaJwtVerifier({
        issuer: config.services.okta.issuer,
        clientId: config.services.okta.clientId,
        assertClaims: {
            cid: config.services.okta.clientId,
        },
    });
    let jwt;
    try {
        jwt = await oktaJwtVerifier.verifyAccessToken(token, "api://default");
    } catch (error) {
        log.error(`createOktaSession: okta token verification failure ${error.message}`);
        return next(new UnauthorizedError("Okta token verification failed"));
    }
    const email = req.body.email;
    const name = req.body.name;
    if (!email || !name) {
        log.error(`createOktaSession: email || name not provided`);
        return next(new BadRequestError());
    }

    await createUser({ name, email });
    let session = await createUserSession({
        email,
        data: {},
        oktaToken: token,
        oktaExpiry: jwt.claims.exp,
    });
    res.send({});
    return next();
}

async function createApplicationSession(req, res, next) {
    let authorization, application;
    try {
        authorization = req.headers.authorization.split("Bearer ").pop();
    } catch (error) {
        log.error(`createApplicationSession: issue with authorization header: ${error.message}`);
        return next(new BadRequestError("Unable to get authorization from header"));
    }

    try {
        application = await getApplication({ authorization });
    } catch (error) {
        log.error(
            `createApplicationSession: caller not an authorised application - authorization: ${authorization}`
        );
        return next(new ForbiddenError());
    }

    const email = req.body.email;
    const name = req.body.name;
    if (!authorization || !email || !name) {
        log.error(`createApplicationSession: authorization || email || name not provided`);
        return next(new BadRequestError());
    }

    try {
        let services = {};
        if (req.body.session?.owncloud) {
            services.owncloud = assembleOwncloudConfiguration({ body: req.body });
        }
        let sessionId = await postSession({
            authorization,
            email,
            name,
            data: { services },
        });
        res.send({ sessionId });
        next();
    } catch (error) {
        log.error(`createApplicationSession: ${error.message}`);
        return next(new ForbiddenError());
    }
}

async function updateApplicationSession(req, res, next) {
    let authorization, application;
    try {
        authorization = req.headers.authorization.split("Bearer ").pop();
    } catch (error) {
        log.error(`createApplicationSession: issue with authorization header: ${error.message}`);
        return next(new BadRequestError("Unable to get authorization from header"));
    }

    try {
        ({ application } = await getApplication({ authorization }));
    } catch (error) {
        log.error(
            `updateApplicationSession: caller not an authorised application - authorization: ${authorization}`
        );
        return next(new ForbiddenError());
    }

    try {
        let session = await models.session.findOne({ where: { id: req.params.sessionId } });
        if (session.creator !== application.name) {
            return next(new ForbiddenError());
        }
        let services = session.data.services;
        if (req.body.session?.owncloud) {
            services.owncloud = assembleOwncloudConfiguration({ body: req.body });
        }
        await session.update({ data: { ...session.data, ...services } });

        res.send({});
        next();
    } catch (error) {
        console.log(error);
        log.error(`updateApplicationSession: ${error.message}`);
        return next(new ForbiddenError());
    }
}

async function saveServiceConfiguration(req, res, next) {
    let session = await models.session.findOne({
        where: { id: req.session.id },
    });
    let data = cloneDeep(session.data);
    data = {
        ...data,
        services: {
            [req.body.service]: req.body,
        },
    };
    await session.update({ data });
    res.send({});
    next();
}

async function getServiceConfiguration(req, res, next) {
    let configuration = await loadConfiguration();
    configuration = configuration.api.services[req.params.serviceName].map((service) => {
        const privateConfiguration = ["clientSecret"];

        return omit(service, privateConfiguration);
    });

    res.send({ configuration });
    next();
}

async function getSession(req, res, next) {
    res.send({ embeddedSession: req.session.creator ? true : false, session: req.session.data });
    next();
}

async function getOauthToken(req, res, next) {
    let configuration = await loadConfiguration();

    let config;
    const serviceName = req.params.serviceName;
    try {
        let service = configuration.api.services[serviceName].filter(
            (s) => s.url === req.params.host
        )[0];
        switch (serviceName) {
            case "owncloud":
                config = await getOwncloudOauthToken({ service, code: req.params.code });
                service = "owncloud";
                await saveToSession({ sessionId: req.session.id, config, service: "owncloud" });
                break;
        }
        res.send({});
        next();
    } catch (error) {
        console.log(error);
        return next(new BadRequestError(error.message));
    }
}

async function saveToSession({ sessionId, config, service }) {
    let session = await models.session.findOne({
        where: { id: sessionId },
    });
    let data = cloneDeep(session.data);
    data = {
        ...data,
        services: {
            [service]: config,
        },
    };
    await session.update({ data });
}
