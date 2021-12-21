import { Crate } from "../lib/crate";
import { getLogger } from "./logger";
const log = getLogger();

export async function saveCrate({ session, user, collectionId, actions }) {
    try {
        const crateMgr = new Crate();
        let hrstart = process.hrtime();
        let crate;
        if (actions?.length) {
            crate = await crateMgr.updateCrate({
                localCrateFile: session?.data?.current?.local?.file,
                collectionId,
                actions,
            });
        } else {
            crate = await crateMgr.exportCollectionAsROCrate({
                collectionId,
                sync: true,
            });
        }
        let hrend = process.hrtime(hrstart);
        // log.debug(JSON.stringify(crate, null, 2));
        await crateMgr.saveCrate({
            session,
            user,
            resource: session?.data?.current?.remote?.resource,
            parent: session?.data?.current?.remote?.parent,
            localFile: session?.data?.current?.local?.file,
            crate,
        });

        log.debug(`Crate update time: ${hrend[0]}s, ${hrend[1]}ns`);
    } catch (error) {
        log.error(`saveCrate: error saving crate ${error.message}`);
        throw new Error("Error saving the crate back to the target");
    }
}
