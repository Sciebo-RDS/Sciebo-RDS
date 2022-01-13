<template>
    <div class="flex flex-col">
        <!-- <div>
            <el-button @click="getEntities">update</el-button>
        </div> -->
        <div class="flex flex-col space-y-2">
            <add-entity-component @add-entity="addNewEntity" />

            <div class="flex flex-row space-x-2">
                <el-input
                    placeholder="filter by name and @id"
                    v-model="filter"
                    @input="debouncedGetEntities"
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
        <el-table :data="entities" highlight-current-row>
            <el-table-column prop="etype" label="@type" width="180"> </el-table-column>
            <el-table-column prop="eid" label="@id" width="400"> </el-table-column>
            <el-table-column prop="name" label="Name"> </el-table-column>
            <el-table-column prop="isConnected" label="Connected" width="100">
                <template slot-scope="scope">
                    <div class="flex flex-row justify-center">
                        <div v-show="scope.row.isConnected" class="text-green-600">
                            <i class="fas fa-check"></i>
                        </div>
                        <div v-show="!scope.row.isConnected" class="text-red-600">
                            <i class="fas fa-times"></i>
                        </div>
                    </div>
                </template>
            </el-table-column>
            <el-table-column label="Actions" width="150">
                <template slot-scope="scope">
                    <div class="flex flex-row space-x-2">
                        <div>
                            <el-button @click="editEntity(scope.row.id)" size="small">
                                <i class="fas fa-edit"></i>
                            </el-button>
                        </div>
                        <div>
                            <el-button
                                @click="deleteEntity(scope.row.id)"
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
            debouncedGetEntities: debounce(this.getEntities, 1000),
            total: undefined,
            entities: [],
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
        this.getEntities();
    },
    methods: {
        async getEntities() {
            let { total, entities } = await this.dataService.getEntities({
                filter: this.filter,
                page: this.page * this.pageSize,
                limit: this.pageSize,
                orderBy: this.orderBy,
                orderDirection: this.orderDirection,
            });
            this.entities = [...entities];
            this.total = total;
        },
        nextPage(page) {
            this.page = page - 1;
            this.getEntities();
        },
        editEntity(id) {
            this.$store.commit("setSelectedEntity", { id });
            this.$emit("manage-data");
        },
        async deleteEntity(id) {
            await this.dataService.deleteEntity({ id });
            this.getEntities();
        },
        async addNewEntity({ type }) {
            let { entity } = await this.dataService.createEntity({
                name: "new entity",
                etype: type,
            });
            this.editEntity(entity.id);
        },
    },
};
</script>
