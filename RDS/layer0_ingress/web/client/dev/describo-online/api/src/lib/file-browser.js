import { ensureDir, open, write, close, pathExists, remove } from "fs-extra";
import { spawn } from "child_process";
import { NotFoundError, InternalServerError, UnauthorizedError } from "restify-errors";
import path from "path";
import { camelCase } from "lodash";
import { getLogger } from "../common/logger";
import { loadConfiguration } from "../common";
const log = getLogger();
const localCachePath = "/srv/tmp";

export async function listFolder({ session, user, resource, folderPath }) {
    let cwd = await setup({ user, session, resource });

    log.debug(`List folder: ${resource} ${folderPath}`);
    try {
        let args = ["lsjson"];
        if (folderPath) {
            args.push(`${resource}:${folderPath}`);
        } else {
            args.push(`${resource}:`);
        }
        let content = await runCommand({ cwd, args });
        return processOutput(content, folderPath);
    } catch (error) {
        handleError(error);
    }

    function processOutput(content) {
        return content.map((entry) => {
            for (let key of Object.keys(entry)) {
                entry[camelCase(key)] = entry[key];
                delete entry[key];
            }
            if (entry.isDir) entry.children = [];
            entry.isLeaf = !entry.isDir;
            entry.parent = folderPath;
            return entry;
        });
    }
}

export async function createFolder({ session, user, resource, folderPath }) {
    let cwd = await setup({ user, session, resource });
    try {
        let args = ["mkdir", `${resource}:${folderPath}`];
        await runCommand({ cwd, args });
    } catch (error) {
        handleError(error);
    }
}

export async function deleteFolder({ session, user, resource, folderPath }) {
    let cwd = await setup({ user, session, resource });
    try {
        let args = ["purge", `${resource}:${folderPath}`];
        await runCommand({ cwd, args });
    } catch (error) {
        handleError(error);
    }
}

export async function syncRemoteFileToLocal({ session, user, resource, parent, name }) {
    let cwd = await setup({ user, session, resource });

    const rcloneSrc = `${resource}:${path.join(parent, name)}`;
    const rcloneTgt = path.join(cwd, "current");

    if (await pathExists(rcloneTgt)) {
        await remove(rcloneTgt);
    }
    await ensureDir(rcloneTgt);

    let args = ["copy", "--no-traverse", rcloneSrc, rcloneTgt];
    log.debug(`syncRemoteFileToLocal: rclone ${JSON.stringify(args)}`);
    try {
        await runCommand({ cwd, args });
        return path.join(rcloneTgt, name);
    } catch (error) {
        log.error(`syncRemoteFileToLocal: ${error.message}`);
        console.log(error);
    }
}

export async function syncLocalFileToRemote({ session, user, resource, parent, localFile }) {
    let cwd = await setup({ user, session, resource });

    const rcloneSrc = localFile;
    const rcloneTgt = `${resource}:${parent}`;

    let args = ["copy", "--no-traverse", rcloneSrc, rcloneTgt];
    log.debug(`syncLocalFileToRemote: rclone ${JSON.stringify(args)}`);
    try {
        await runCommand({ cwd, args });
    } catch (error) {
        log.error(`syncLocalFileToRemote: ${error.message}`);
        console.log(error);
    }
}

export async function setup({ session, user, resource }) {
    // use resource to see if we have a suitable rclone configuration
    if (!session.data.services) {
        throw new NotFoundError("No session data");
    }
    let rcloneConfiguration = session?.data?.services[resource];
    if (!rcloneConfiguration) {
        // fail not found error if not
        throw new NotFoundError("No session data");
    }

    // write rclone configuration to disk
    return await writeRcloneConfiguration({
        rcloneConfiguration,
        user,
    });
}

export function localWorkingDirectory({ user }) {
    return path.join(localCachePath, user.id);
}

async function writeRcloneConfiguration({ rcloneConfiguration, user }) {
    // console.log(JSON.stringify(rcloneConfiguration, null, 2));
    const folderPath = localWorkingDirectory({ user });
    const filePath = path.join(folderPath, "rclone.conf");
    await ensureDir(folderPath);
    const fd = await open(filePath, "w");
    switch (rcloneConfiguration.service) {
        case "onedrive":
            await write(fd, `[onedrive]\n`);
            await write(fd, `type = onedrive\n`);
            await write(fd, `token = ${JSON.stringify(rcloneConfiguration.token)}\n`);
            await write(fd, `drive_id = ${rcloneConfiguration.drive_id}\n`);
            await write(fd, `drive_type = ${rcloneConfiguration.token.access_token}\n`);
            break;
        case "owncloud":
            await write(fd, `[owncloud]\n`);
            await write(fd, `type = webdav\n`);
            await write(
                fd,
                `url = ${rcloneConfiguration.url}/files/${rcloneConfiguration.token.user_id}\n`
            );
            await write(fd, `vendor = owncloud\n`);
            await write(fd, `bearer_token = ${rcloneConfiguration.token.access_token}\n`);
    }
    await close(fd);
    return folderPath;
}

async function runCommand({ cwd, args }) {
    let content = await new Promise((resolve, reject) => {
        let content = "";
        let error = "";
        args = ["--config", "./rclone.conf", ...args];
        const s = spawn(rclone(), args, { cwd });

        s.stdout.on("data", function (msg) {
            content += msg.toString();
        });
        s.stderr.on("data", function (msg) {
            error += msg.toString();
        });
        s.on("close", (code) => {
            if (!code) {
                if (content) resolve(JSON.parse(content));
                resolve();
            }
            reject(new Error(error));
        });
    });
    return content;
}

function rclone() {
    if (process.env.NODE_ENV === "production") {
        return "/srv/bin/rclone";
    } else {
        return "/srv/api/bin/rclone";
    }
}

function handleError(error) {
    if (error.message.match("InvalidAuthenticationToken: Access token has expired")) {
        throw new UnauthorizedError(error.message);
    } else {
        console.error(error);
        throw new InternalServerError(error.message);
    }
}
