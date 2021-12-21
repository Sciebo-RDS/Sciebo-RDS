import {
    getProfile,
    createProfile,
    updateProfile,
    lookupProfile,
    getTypeDefinition,
} from "../lib/profile";
import { BadRequestError, InternalServerError } from "restify-errors";
import { getLogger } from "../common/logger";
const log = getLogger();

export async function getProfileRouteHandler(req, res, next) {
    const collectionId = req.session.data?.current?.collectionId;
    console.log(collectionId);
    const profileId = req.params.profileId;
    if (!profileId) {
        log.error(`getProfileRouteHandler: profileId not provided`);
        return next(new BadRequestError());
    }
    try {
        let profile = await getProfile({ collectionId, profileId });
        res.send({ profile });
        return next();
    } catch (error) {
        log.error(`getProfileRouteHandler: ${error.message}`);
        return next(new InternalServerError());
    }
}

export async function lookupProfileRouteHandler(req, res, next) {
    const collectionId = req.session.data?.current?.collectionId;
    try {
        let { query } = req.query;
        let matches = await lookupProfile({ collectionId, query });
        res.send({ matches });
        return next(0);
    } catch (error) {
        log.error(`lookupProfileRouteHandler: ${error.message}`);
        return next(new BadRequestError());
    }
}

export async function createProfileRouteHandler(req, res, next) {
    let { name, profile, collectionId } = req.body;
    if (!name || !profile || !collectionId) {
        log.error(`updateProfileRouteHandler: name || profile || collection not provided`);
        return next(new BadRequestError());
    }
    try {
        profile = await createProfile({ collectionId, name, profile });
    } catch (error) {
        log.error(`createProfileRouteHandler: ${error.message}`);
        return next(new BadRequestError());
    }
    res.send({ profile });
    return next();
}

export async function updateProfileRouteHandler(req, res, next) {
    const profileId = req.params.profileId;
    if (!profileId) {
        log.error(`updateProfileRouteHandler: profileId not provided`);
        return next(new BadRequestError());
    }
    let { name, profile } = req.body;
    if (!name && !profile) {
        return next(new BadRequestError());
    }
    try {
        profile = await updateProfile({ profileId, name, profile });
    } catch (error) {
        log.error(`updateProfileRouteHandler: ${error.message}`);
        return next(new BadRequestError());
    }
    res.send({ profile });
    return next();
}

export async function getTypeDefinitionRouteHandler(req, res, next) {
    const collectionId = req.session.data?.current?.collectionId;
    try {
        let name = req.query.name;
        let definition = await getTypeDefinition({ collectionId, name });
        res.send({ definition });
        return next(0);
    } catch (error) {
        log.error(`getTypeDefinition: ${error.message}`);
        return next(new BadRequestError());
    }
}
