<template>
    <el-card>
        <div class="flex flex-col space-y-4">
            <div class="flex flex-col">
                <div class="flex flex-row space-x-2">
                    <el-input
                        placeholder="filter by name and @id"
                        v-model="filter"
                        @input="debouncedGetTemplates"
                        :clearable="true"
                        size="small"
                    >
                    </el-input>
                    <el-pagination
                        class="ml-2"
                        layout="total, prev, pager, next"
                        :total="total"
                        @current-change="nextPage"
                    >
                    </el-pagination>
                </div>
            </div>
            <el-table :data="templates" highlight-current-row v-loading="loading">
                <el-table-column prop="etype" label="@type" width="180"> </el-table-column>
                <el-table-column prop="eid" label="@id" width="400"> </el-table-column>
                <el-table-column prop="name" label="Name"> </el-table-column>
                <el-table-column prop="src" label="Entity Data" type="expand" width="100">
                    <template slot-scope="scope">
                        <pre>{{ JSON.stringify(scope.row.src, null, 2) }}</pre>
                    </template>
                </el-table-column>
                <el-table-column label="Actions" width="150">
                    <template slot-scope="scope">
                        <div class="flex flex-row space-x-2">
                            <div v-if="!scope.row.etype && !scope.row.eid">
                                <el-button
                                    @click="applyCrateTemplate(scope.row.id)"
                                    size="small"
                                    type="primary"
                                >
                                    <i class="fas fa-check-double"></i>
                                </el-button>
                            </div>
                            <div>
                                <el-button
                                    @click="deleteTemplate(scope.row.id)"
                                    size="small"
                                    type="danger"
                                    v-if="scope.row.eid !== './'"
                                >
                                    <i class="fas fa-trash"></i>
                                </el-button>
                            </div>
                        </div>
                    </template>
                </el-table-column>
            </el-table>
        </div>
    </el-card>
</template>

<script>
import AddEntityComponent from "@/components/manage-entities/AddEntity.component.vue";
import DataService from "@/components/manage-entities/data.service.js";
import { debounce } from "lodash";

export default {
    components: {
        AddEntityComponent,
    },
    data() {
        return {
            loading: false,
            debouncedGetTemplates: debounce(this.getTemplates, 1000),
            total: undefined,
            templates: [],
            filter: "",
            page: 0,
            pageSize: 10,
            orderBy: ["etype", "name"],
            orderDirection: ["asc"],
        };
    },
    mounted() {
        this.dataService = new DataService({
            $http: this.$http,
            $log: this.$log,
        });
        this.getTemplates();
    },
    methods: {
        async getTemplates() {
            let { templates, total } = await this.dataService.getTemplates({
                filter: this.filter,
                page: this.page * this.pageSize,
                limit: this.pageSize,
                orderBy: this.orderBy,
                orderDirection: this.orderDirection,
            });
            this.templates = [...templates];
            this.total = total;
        },
        nextPage(page) {
            this.page = page - 1;
            this.getTemplates();
        },
        async deleteTemplate(id) {
            await this.dataService.deleteTemplate({ id });
            this.getTemplates();
        },
        async applyCrateTemplate(templateId) {
            this.loading = true;
            await this.dataService.replaceCrateWithTemplate({ templateId });
            await new Promise((resolve) => setTimeout(resolve, 1000));
            this.$store.commit("setSelectedEntity", { id: "RootDataset" });
            this.loading = false;
        },
    },
};
</script>
