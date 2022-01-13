<template>
    <div class="flex flex-col">
        <iframe :src="link" title="" v-if="link" class="flex-grow"></iframe>
        <div class="flex flex-col justify-center items-center h-64" v-if="!link">
            <div v-loading="loading" class="w-10 h-10"></div>
            <div v-if="error" class="flex flex-row">
                <div class="text-base pt-1 text-center">
                    File preview is not available. <br />
                    If this is a personal onedrive it's not supported at all by Microsoft.
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        path: {
            type: String,
        },
        id: {
            type: String,
        },
    },
    data() {
        return {
            loading: false,
            link: undefined,
            error: undefined,
        };
    },
    mounted() {
        if (this.path) {
            this.getFilePreview();
        }
    },
    methods: {
        async getFilePreview() {
            this.loading = true;
            let endpoint;
            if (this.path) {
                endpoint = `/me/drive/root:${this.path}:/preview`;
                // endpoint = `/me/drive/root:${this.path}`;
                // let itemMetadata = await this.onedriveAuthenticationManager.client({ endpoint });
                // console.log(JSON.stringify(itemMetadata, null, 2));
                // endpoint = `/me/drive/items/${itemMetadata.id}/preview`;
                // endpoint = `${itemMetadata.parentReference.path}/${itemMetadata.name}/preview`;
            } else if (this.id) {
                let id = this.id.match("#") ? this.id.split("#")[1] : this.id;
                endpoint = `/me/drive/items/${id}/preview`;
            }
            try {
                let request = {
                    endpoint,
                    method: "POST",
                    body: {
                        viewer: "onedrive",
                        chromeless: true,
                        allowEdit: false,
                    },
                };
                let link = await this.onedriveAuthenticationManager.client(request);
                if (link.error) {
                    this.error = true;
                } else {
                    this.link = link.getUrl;
                }
            } catch (error) {
                this.error = `Preview not available at this time: ${error.message}`;
            }
            this.loading = false;
        },
    },
};
</script>
