import { createRouter, createWebHistory } from "vue-router";

import UsersView from "@/views/UsersView.vue";
import PropertiesView from "@/views/PropertiesView.vue";
import TransferView from "@/views/TransferView.vue";

const routes = [
  { path: "/", redirect: "/users" },
  { path: "/users", component: UsersView },
  { path: "/properties", component: PropertiesView },
  { path: "/transfer", component: TransferView },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
