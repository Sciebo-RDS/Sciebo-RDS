import { BadRequestError, NotFoundError, ForbiddenError } from "restify-errors";
import {
    getEntity,
    getEntityCount,
    getEntities,
    getEntityProperties,
    findEntity,
    insertEntity,
    updateEntity,
    removeEntity,
    attachProperty,
    updateProperty,
    removeProperty,
    associate,
    insertFilesAndFolders,
} from "../lib/entities";
import { saveCrate } from "../common/save-crate";
import { getLogger } from "../common/logger";
const log = getLogger();

export async function getEntityRouteHandler(req, res, next) {
    const collectionId = req.session.data?.current?.collectionId;
    if (!collectionId) {
        return next(new ForbiddenError("No collection loaded"));
    }

    if (!req.params.entityId) {
        return next(
            new BadRequestError(
                `You must provide an entityId to lookup or the special value 'RootDataset'`
            )
        );
    }

    let entity;
    try {
        if (req.params.entityId === "RootDataset") {
            let entities = await findEntity({
                eid: "./",
                etype: "Dataset",
                collectionId,
                fuzzy: false,
            });
            entity = entities.pop();
            if (!entity) {
                return next(new NotFoundError(`Root dataset not found`));
            }
            entity = await getEntity({ id: entity.id, collectionId });
        } else {
            entity = await getEntity({ id: req.params.entityId, collectionId });
        }

        res.send({ entity });
        next();
    } catch (error) {
        log.error(`getEntityRouteHandler: ${error.message}`);
        return next(new ForbiddenError());
    }
}

export async function getEntityCountRouteHandler(req, res, next) {
    const collectionId = req.session.data?.current?.collectionId;
    if (!collectionId) {
        return next(new ForbiddenError("No collection loaded"));
    }

    try {
        let count = await getEntityCount({ collectionId });
        res.send({ count });
        next();
    } catch (error) {
        log.error(`getEntityRouteHandler: ${error.message}`);
        return next(new ForbiddenError());
    }
}

export async function getEntitiesRouteHandler(req, res, next) {
    const collectionId = req.session.data?.current?.collectionId;
    if (!collectionId) {
        return next(new ForbiddenError("No collection loaded"));
    }

    let filter = req.query.filter;
    let page = req.query.page;
    let limit = req.query.limit;
    let orderBy = req.query.orderBy.split(",");
    let orderDirection = req.query.direction;

    try {
        let results = await getEntities({
            collectionId,
            filter,
            page,
            limit,
            orderByProperties: orderBy,
            orderDirection,
        });
        res.send({ ...results });
        next();
    } catch (error) {
        log.error(`getEntitiesRouteHandler: ${error.message}`);
        return next(new ForbiddenError());
    }
}

export async function getEntityPropertiesRouteHandler(req, res, next) {
    const collectionId = req.session.data?.current?.collectionId;
    if (!collectionId) {
        return next(new ForbiddenError("No collection loaded"));
    }

    if (!req.params.entityId) {
        return next(
            new BadRequestError(
                `You must provide an entityId to lookup or the special value 'RootDataset'`
            )
        );
    }

    let entity, properties;
    try {
        if (req.params.entityId === "RootDataset") {
            entity = (
                await findEntity({
                    eid: "./",
                    etype: "Dataset",
                    collectionId,
                })
            ).pop();
            if (!entity) {
                return next(new NotFoundError(`Root dataset not found`));
            }
            ({ properties } = await getEntityProperties({
                id: entity.id,
                collectionId,
            }));
        } else {
            ({ properties } = await getEntityProperties({
                id: req.params.entityId,
                collectionId,
            }));
        }

        properties = properties.map((p) => p.get());
        res.send({ properties });
        next();
    } catch (error) {
        log.error(`getEntityPropertiesRouteHandler: ${error.message}`);
        return next(new ForbiddenError());
    }
}

export async function findEntityRouteHandler(req, res, next) {
    const collectionId = req.session.data?.current?.collectionId;
    if (!collectionId) {
        return next(new ForbiddenError("No collection loaded"));
    }

    let find = { collectionId };
    try {
        let { hierarchy, eid, etype, name, limit } = req.body;
        find = { collectionId, hierarchy, eid, etype, name, limit };
    } catch (error) {}
    try {
        let entities = await findEntity(find);
        res.send({ entities });
        next();
    } catch (error) {
        log.error(`findEntityRouteHandler: ${error.message}`);
        return next(new ForbiddenError());
    }
}

export async function postEntityRouteHandler(req, res, next) {
    const collectionId = req.session.data?.current?.collectionId;
    if (!collectionId) {
        return next(new ForbiddenError());
    }
    let entity = req.body.entity;
    try {
        entity = await insertEntity({ entity, collectionId });
        if (!req.headers["x-testing"]) {
            await saveCrate({
                session: req.session,
                user: req.user,
                collectionId,
                actions: [{ name: "insert", entity }],
            });
        }
        res.send({ entity });
        return next();
    } catch (error) {
        log.error(`postEntityRouteHandler: ${error.message}`);
        return next(new BadRequestError(error.message));
    }
}

export async function putEntityRouteHandler(req, res, next) {
    const collectionId = req.session.data?.current?.collectionId;
    if (!collectionId) {
        return next(new ForbiddenError());
    }
    if (!req.params.entityId) {
        return next(
            new BadRequestError(
                `You must provide an entityId to lookup or the special value 'RootDataset'`
            )
        );
    }
    let entityId = req.params.entityId;
    let { name, eid } = req.body;
    try {
        let entity = await updateEntity({ collectionId, entityId, name, eid });
        if (!req.headers["x-testing"]) {
            await saveCrate({
                session: req.session,
                user: req.user,
                collectionId,
                actions: [{ name: "update", entity }],
            });
        }
        res.send({ entity });
        return next();
    } catch (error) {
        log.error(`putEntityRouteHandler: ${error.message}`);
        return next(new BadRequestError(error.message));
    }
}

export async function delEntityRouteHandler(req, res, next) {
    const collectionId = req.session.data?.current?.collectionId;
    if (!collectionId) {
        return next(new ForbiddenError());
    }
    if (!req.params.entityId) {
        return next(
            new BadRequestError(
                `You must provide an entityId to lookup or the special value 'RootDataset'`
            )
        );
    }
    let entityId = req.params.entityId;
    try {
        let { updated, removed } = await removeEntity({ entityId, collectionId });
        let actions = updated.map((eid) => ({ name: "update", entity: { id: eid } }));
        actions = [...actions, { name: "remove", entity: removed.get() }];
        if (!req.headers["x-testing"]) {
            await saveCrate({
                session: req.session,
                user: req.user,
                collectionId,
                actions,
            });
        }
        res.send({});
        next();
    } catch (error) {
        console.log(error);
        log.error(`delEntityRouteHandler: ${error.message}`);
        return next(new BadRequestError(error.message));
    }
}

export async function postEntityPropertyRouteHandler(req, res, next) {
    const collectionId = req.session.data?.current?.collectionId;
    if (!collectionId) {
        return next(new ForbiddenError());
    }
    let entityId = req.params.entityId;
    let { property, value } = req.body;
    try {
        property = await attachProperty({
            collectionId,
            entityId,
            property,
            value,
        });
        if (!req.headers["x-testing"]) {
            await saveCrate({
                session: req.session,
                user: req.user,
                collectionId,
                actions: [{ name: "update", entity: { id: entityId } }],
            });
        }

        res.send({ property: property.get() });
        return next();
    } catch (error) {
        log.error(`postEntityPropertyRouteHandler: ${error.message}`);
        return next(new BadRequestError(error.message));
    }
}

export async function putEntityPropertyRouteHandler(req, res, next) {
    const collectionId = req.session.data?.current?.collectionId;
    if (!collectionId) {
        return next(new ForbiddenError());
    }
    const { entityId, propertyId } = req.params;
    let { value } = req.body;
    try {
        let property = await updateProperty({
            collectionId,
            entityId,
            propertyId,
            value,
        });
        if (!req.headers["x-testing"]) {
            await saveCrate({
                session: req.session,
                user: req.user,
                collectionId,
                actions: [{ name: "update", entity: { id: entityId } }],
            });
        }

        res.send({ property: property.get() });
        return next();
    } catch (error) {
        log.error(`putEntityPropertyRouteHandler: ${error.message}`);
        return next(new BadRequestError(error.message));
    }
}

export async function delEntityPropertyRouteHandler(req, res, next) {
    const collectionId = req.session.data?.current?.collectionId;
    if (!collectionId) {
        return next(new ForbiddenError());
    }
    const { entityId, propertyId } = req.params;
    try {
        await removeProperty({
            collectionId,
            entityId,
            propertyId,
        });
        if (!req.headers["x-testing"]) {
            await saveCrate({
                session: req.session,
                user: req.user,
                collectionId,
                actions: [{ name: "update", entity: { id: entityId } }],
            });
        }

        res.send({});
        return next();
    } catch (error) {
        log.error(`delEntityPropertyRouteHandler: ${error.message}`);
        return next(new BadRequestError(error.message));
    }
}

export async function putEntityAssociateRouteHandler(req, res, next) {
    const collectionId = req.session.data?.current?.collectionId;
    if (!collectionId) {
        return next(new ForbiddenError());
    }
    let entityId = req.params.entityId;
    try {
        let { property, tgtEntityId } = req.body;

        property = await associate({
            collectionId,
            entityId,
            property,
            tgtEntityId,
        });
        if (!req.headers["x-testing"]) {
            await saveCrate({
                session: req.session,
                user: req.user,
                collectionId,
                actions: [{ name: "update", entity: { id: entityId } }],
            });
        }

        res.send({});
        return next();
    } catch (error) {
        log.error(`putEntityPropertyRouteHandler: ${error.message}`);
        return next(new BadRequestError(error.message));
    }
}

export async function postFilesRouteHandler(req, res, next) {
    const collectionId = req.session.data?.current?.collectionId;
    if (!collectionId) {
        return next(new ForbiddenError());
    }
    let files = req.body.files;
    if (!files) {
        return next(new BadRequestError("You must provide an array of files to add"));
    }
    try {
        await insertFilesAndFolders({ collectionId, files });
        res.send({});
        return next();
    } catch (error) {
        log.error(`postFilesRouteHandler: ${error.message}`);
        return next(new BadRequestError(error.message));
    }
}
