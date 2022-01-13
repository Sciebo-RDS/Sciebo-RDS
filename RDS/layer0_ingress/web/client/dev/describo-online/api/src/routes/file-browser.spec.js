import "regenerator-runtime";
import fetch from "node-fetch";
import path from "path";
import { getUserSession } from "../lib/user";

/*
 *
 *    In order to run these tests you need to first login to the UI as yourself
 *    then login to Microsoft OneDrive to store an access token in the DB.
 *
 *    Once you've done that you can set the 'userEmail' variable to your email
 *    and the tests will run as you against your onedrive.
 *
 */
const api = "http://localhost:8080";
const userEmail = "m@lr.id.au";
describe.skip("Test file browser api routes", () => {
    let sessionId;
    beforeAll(async () => {
        // sessionId = await createSession();
    });
    test("it should fail to find an rclone configuration", async () => {
        const { user, session } = await getUserSession({
            email: userEmail,
        });

        let response = await fetch(`${api}/folder/read`, {
            method: "POST",
            headers: {
                Authorization: `sid ${session.id}`,
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ resource: "nodrive" }),
        });
        expect(response.status).toBe(404);
    });
    test("it should be able to get a listing of a onedrive folder using rclone", async () => {
        const { user, session } = await getUserSession({ email: userEmail });

        let response = await fetch(`${api}/folder/read`, {
            method: "POST",
            headers: {
                Authorization: `sid ${session.id}`,
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ resource: "onedrive" }),
        });
        expect(response.status).toBe(200);
        response = await response.json();
        expect(response.content).toBeTruthy;
    });
    test("it should be able to create a folder in onedrive", async () => {
        const { user, session } = await getUserSession({
            email: userEmail,
        });

        let response = await fetch(`${api}/folder/create`, {
            method: "POST",
            headers: {
                Authorization: `sid ${session.id}`,
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ resource: "onedrive", path: "test-folder" }),
        });
        expect(response.status).toBe(200);

        response = await fetch(`${api}/folder/read`, {
            method: "POST",
            headers: {
                Authorization: `sid ${session.id}`,
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ resource: "onedrive" }),
        });
        expect(response.status).toBe(200);
        response = await response.json();
        expect(
            response.content.filter((p) => p.Name === "test-folder").length
        ).toBe(1);
    });
    test("it should be able to create, and then remove a folder in onedrive", async () => {
        const { user, session } = await getUserSession({
            email: userEmail,
        });

        // create a folder
        let response = await fetch(`${api}/folder/create`, {
            method: "POST",
            headers: {
                Authorization: `sid ${session.id}`,
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                resource: "onedrive",
                path: "test-folder",
            }),
        });
        expect(response.status).toBe(200);

        // delete it
        response = await fetch(`${api}/folder/delete`, {
            method: "POST",
            headers: {
                Authorization: `sid ${session.id}`,
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                resource: "onedrive",
                path: "test-folder",
            }),
        });
        expect(response.status).toBe(200);

        // ensure it's gone
        response = await fetch(`${api}/folder/read`, {
            method: "POST",
            headers: {
                Authorization: `sid ${session.id}`,
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ resource: "onedrive" }),
        });
        expect(response.status).toBe(200);
        response = await response.json();
        expect(response.content.length).toBe(1);
        expect(
            response.content.filter((p) => p.Name === "test-folder").length
        ).toBe(0);
    });
});
