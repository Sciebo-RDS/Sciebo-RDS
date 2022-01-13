module.exports = {
    verbose: true,
    rootDir: "src",
    testMatch: ["**/*.spec.js"],
    testPathIgnorePatterns: ["node_modules"],
    watchPathIgnorePatterns: ["\\**/.*(?<!spec).js"],
};
