import FileTreeLoader from "./file-tree-loader";

self.addEventListener("message", (m) => {
    const ftloader = new FileTreeLoader({
        // target: m.data.target,
    });
    (async () => {
        // await new Promise(resolve => setTimeout(resolve, Math.random() * 1000));
        console.log("***", m.data);
        console.log("here");
        // const content = await ftloader.load({
        //     filterFiles: m.data.filterFiles,
        //     path: m.data.path,
        //     root: m.data.root,
        // });
        let content = [];
        self.postMessage(content);
    })();
});
