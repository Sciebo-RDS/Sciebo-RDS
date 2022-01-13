import VueRouter from "vue-router";
import Home from "../views/Home.vue";
import Projects from "../views/Projects.vue";
import Settings from "../views/Settings.vue";
import Wizard from "../views/Wizard.vue";
import Services from "../views/Services.vue";
import Help from "../views/Help.vue";
import Removal from "../views/RemoveRDS.vue";

let routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
    icon: "mdi-home",
  },
  {
    path: "/projects",
    name: "Projects",
    component: Projects,
    icon: "mdi-lightbulb-on",
  },
  {
    path: "/services",
    name: "Services",
    component: Services,
    icon: "mdi-share-variant",
  },
  {
    path: "/settings",
    name: "Settings",
    component: Settings,
    icon: "mdi-cog",
    hide: true,
  },
  {
    path: "/help",
    name: "Help",
    component: Help,
    icon: "mdi-help-circle",
  },
  {
    path: "/removeRDS",
    name: "RemoveRDS",
    component: Removal,
    icon: "mdi-close",
    hide: true,
  },
  {
    path: "/wizard",
    name: "Wizard",
    component: Wizard,
    icon: "mdi-wizard-hat",
    hide: true,
  },
];

export default {
  install(Vue) {
    Vue.use(VueRouter);

    const titles = {
      Home: Vue.prototype.$gettext("Home"),
      Projects: Vue.prototype.$gettext("Projects"),
      Services: Vue.prototype.$gettext("Services"),
      Settings: Vue.prototype.$gettext("Settings"),
      Wizard: Vue.prototype.$gettext("Wizard"),
      Help: Vue.prototype.$gettext("Help"),
      RemoveRDS: Vue.prototype.$gettext("Remove RDS account"),
    };

    for (let index = 0; index < routes.length; index++) {
      const route = routes[index];
      route.title = titles[route.name];
    }

    const router = new VueRouter({
      routes,
    });

    Vue.prototype.$routers = router;
  },
  routes,
};
