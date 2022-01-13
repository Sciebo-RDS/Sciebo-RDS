import { groupBy } from "lodash";

export default class DataService {
    constructor({ $http, $log }) {
        this.$http = $http;
        this.$log = $log;
    }
    async getEntity({ id }) {
        let response = await this.$http.get({
            route: `/entity/${id}`,
        });
        if (response.status !== 200) {
            return this.handleError({ response });
        } else {
            let { entity } = await response.json();
            entity.properties = [];
            return { entity };
        }
    }

    async getEntityCount() {
        let response = await this.$http.get({
            route: `/entity/count`,
        });
        if (response.status !== 200) {
            return this.handleError({ response });
        } else {
            return await response.json();
        }
    }

    async getEntities({ filter, page, limit, orderBy, orderDirection }) {
        let response = await this.$http.get({
            route: `/entity?page=${page}&limit=${limit}&orderBy=${encodeURIComponent(
                orderBy
            )}&direction=${encodeURIComponent(orderDirection)}&filter=${encodeURIComponent(
                filter
            )}`,
        });
        if (response.status !== 200) {
            return this.handleError({ response });
        } else {
            let { total, entities } = await response.json();
            return { total, entities };
        }
    }

    async getEntityProperties({ id }) {
        let response = await this.$http.get({
            route: `/entity/${id}/properties`,
        });
        if (response.status !== 200) {
            return this.handleError({ response });
        } else {
            let { properties } = await response.json();
            const forwardProperties = properties.filter((p) => p.direction !== "R");
            const reverseProperties = properties.filter((p) => p.direction === "R");
            properties = {
                forwardProperties: groupBy(forwardProperties, "name"),
                reverseProperties: groupBy(reverseProperties, "name"),
            };
            return { properties };
        }
    }

    async getEntityTypeDefinition({ type }) {
        let response = await this.$http.get({
            route: `/definition?name=${encodeURIComponent(type)}`,
        });
        if (response.status !== 200) {
            return this.handleError({ response });
        } else {
            response = await response.json();
            return {
                definition: response.definition ? response.definition : {},
            };
        }
    }

    async createEntity(entity) {
        this.$log.debug("create new entity", entity);
        let response = await this.$http.post({
            route: `/entity`,
            body: { entity },
        });
        if (response.status !== 200) {
            return this.handleError({ response });
        } else {
            return await response.json();
        }
    }

    async deleteEntity({ id }) {
        this.$log.debug("delete entity", id);
        let response = await this.$http.delete({
            route: `/entity/${id}`,
        });
        if (response.status !== 200) {
            return this.handleError({ response });
        } else {
            return await response.json();
        }
    }

    async updateEntityProperty({ id, property, value }) {
        this.$log.debug("update entity property", id, property, value);
        let response = await this.$http.put({
            route: `/entity/${id}`,
            body: {
                [property]: value,
            },
        });
        if (response.status !== 200) {
            return this.handleError({ response });
        } else {
            return await response.json();
        }
    }

    async createProperty({ srcEntityId, property, value }) {
        this.$log.debug("create property", srcEntityId, property, value);
        let response = await this.$http.post({
            route: `/entity/${srcEntityId}/property`,
            body: {
                property,
                value,
            },
        });
        if (response.status !== 200) {
            return this.handleError({ response });
        } else {
            return await response.json();
        }
    }

    async associate({ srcEntityId, property, tgtEntityId }) {
        this.$log.debug("associate ", srcEntityId, property, tgtEntityId);
        let response = await this.$http.put({
            route: `/entity/${srcEntityId}/associate`,
            body: {
                property,
                tgtEntityId,
            },
        });
        if (response.status !== 200) {
            return this.handleError({ response });
        } else {
            return await response.json();
        }
    }

    async updateProperty({ entityId, propertyId, property, value }) {
        this.$log.debug("update property", propertyId, property, value);
        let response = await this.$http.put({
            route: `/entity/${entityId}/property/${propertyId}`,
            body: {
                property,
                value,
            },
        });
        if (response.status !== 200) {
            return this.handleError({ response });
        } else {
            return await response.json();
        }
    }

    async deleteProperty({ entityId, propertyId }) {
        this.$log.debug("delete property", propertyId);
        let response = await this.$http.delete({
            route: `/entity/${entityId}/property/${propertyId}`,
        });
        if (response.status !== 200) {
            return this.handleError({ response });
        }
    }

    async findEntity({ etype, eid, name, hierarchy, limit }) {
        this.$log.debug("lookup entity");
        let response = await this.$http.post({
            route: `/entity/lookup`,
            body: { etype, eid, name, hierarchy, limit },
        });
        if (response.status !== 200) {
            return this.handleError({ response });
        } else {
            return await response.json();
        }
    }

    async lookupType({ query }) {
        this.$log.debug("lookup type definition", query);
        let response = await this.$http.get({
            route: `/definition/lookup?query=${query}`,
        });
        if (response.status !== 200) {
            return this.handleError({ response });
        } else {
            return await response.json();
        }
    }

    async saveEntityAsTemplate({ id }) {
        this.$log.debug("save entity as template", id);
        let response = await this.$http.post({
            route: `/template`,
            body: { entityId: id },
        });
        if (response.status !== 200) {
            return this.handleError({ response });
        } else {
            return await response.json();
        }
    }

    async saveCrateAsTemplate({ name }) {
        this.$log.debug("save crate as template");
        let response = await this.$http.post({
            route: `/template`,
            body: { name },
        });
        if (response.status !== 200) {
            return this.handleError({ response });
        } else {
            return await response.json();
        }
    }

    async getTemplates({ filter, type, page, limit, orderBy, orderDirection }) {
        this.$log.debug("lookup templates");
        let queryParams = { page, limit, orderBy, orderDirection, type };
        if (filter) queryParams.filter = encodeURIComponent(filter);

        const queryString = this.toQueryString(queryParams);
        const url = queryString ? `/template?${queryString}` : "/template";
        let response = await this.$http.get({
            route: url,
        });
        if (response.status !== 200) {
            return this.handleError({ response });
        } else {
            return await response.json();
        }
    }

    async deleteTemplate({ id }) {
        this.$log.debug("delete template", id);
        let response = await this.$http.delete({
            route: `/template/${id}`,
        });
        if (response.status !== 200) {
            return this.handleError({ response });
        } else {
            return await response.json();
        }
    }

    async replaceCrateWithTemplate({ templateId }) {
        this.$log.debug("replace crate with template", templateId);
        let response = await this.$http.post({
            route: `/template/replace`,
            body: { templateId },
        });
        if (response.status !== 200) {
            return this.handleError({ response });
        } else {
            return await response.json();
        }
    }

    async addTemplate({ templateId }) {
        this.$log.debug("add template", templateId);
        let response = await this.$http.post({
            route: `/template/add`,
            body: { templateId },
        });
        if (response.status !== 200) {
            return this.handleError({ response });
        } else {
            return await response.json();
        }
    }

    async handleError({ response }) {
        let error = await response.json();
        // this.$log.error(response.status, error.message);
        throw new Error(error.message);
    }

    toQueryString(paramsObject) {
        return Object.keys(paramsObject)
            .map((key) => `${encodeURIComponent(key)}=${encodeURIComponent(paramsObject[key])}`)
            .join("&");
    }
}
