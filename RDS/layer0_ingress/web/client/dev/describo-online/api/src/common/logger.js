const { createLogger, format, transports } = require("winston");
const { combine, timestamp, printf } = format;

export function getLogger() {
    const myFormat = printf(({ level, message, timestamp }) => {
        return `${timestamp} ${level.toUpperCase()}: ${message}`;
    });
    const logger = createLogger({
        level: process.env.NODE_ENV === "development" ? "debug" : "info",
        format: combine(timestamp(), myFormat),
        transports: [new transports.Console()],
    });
    return logger;
}
