import Vue from "vue";
import VueRouter from "vue-router";
import ShellComponent from "./components/Shell.component.vue";
import HomeComponent from "./components/home/Shell.component.vue";
import FeaturesComponent from "./components/features/Shell.component.vue";
import AboutComponent from "./components/About.component.vue";

Vue.use(VueRouter);

const routes = [
    {
        path: "/",
        component: ShellComponent,
        children: [
            {
                path: "/",
                name: "home",
                component: HomeComponent,
            },
            {
                path: "/features",
                name: "features",
                component: FeaturesComponent,
            },
            {
                path: "/about",
                name: "about",
                component: AboutComponent,
            },
        ],
    },
];

const router = new VueRouter({
    mode: "history",
    base: process.env.BASE_URL,
    routes,
});

export default router;
