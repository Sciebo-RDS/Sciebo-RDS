const { getLogger } = require("./logger");

describe("test getting logger", () => {
    test("it should set level to debug in development", () => {
        process.env.NODE_ENV = "development";
        let logger = getLogger();
        expect(logger.level).toEqual("debug");
    });
    test("it should set level to info in production", () => {
        process.env.NODE_ENV = "production";
        let logger = getLogger();
        expect(logger.level).toEqual("info");
    });
});
