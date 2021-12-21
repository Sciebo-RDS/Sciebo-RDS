function promise() {
    // eslint-disable-next-line no-undef
    let prom1 = new Promise(function (resolve, reject) {
        let timer = setInterval(function () {
            clearInterval(timer)
            reject(new Error('no value through response'))
        }, 10000)

        // eslint-disable-next-line no-undef
        const url = OC.generateUrl("/apps/rds/api/1.0/informations");
        fetch(url, {
            headers: new Headers({
                requesttoken: oc_requesttoken,
                "Content-Type": "application/json",
            })
        }).then((response) => {
            if (response.ok) {
                return response.text();
            }
            throw new Error(`${response.status} ${response.statusText}`);
        }).then((response) => {
            console.log("got response: ", response)
            const data = JSON.parse(response)
            resolve({
                url: data.cloudURL,
                server: data.cloudURL,
                language: data.language,
                response
            })
        }).catch((error) => {
            reject("cloudURL is empty, error: ", error)
        }).finally(() => {
            clearInterval(timer)
        })
    })

    return prom1;
}

function getConfig(context) {
    let prom = promise()
    prom.then((config) => {
        context.config = config;
    }).catch(() => {
        context.config = {
            url: "http://localhost:8080",
            server: "http://localhost:8080"
        };
    });
    return prom
}

export default getConfig