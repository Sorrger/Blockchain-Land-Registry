import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import PropertiesView from '../views/PropertiesView.vue'
import TransferView from '../views/TransferView.vue'
import UsersView from '../views/UsersView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', component: LoginView },
    // Notary Routes
    { path: '/notary-dashboard', redirect: '/properties' }, // For now redirect to properties
    { path: '/properties', component: PropertiesView },
    { path: '/users', component: UsersView },
    { path: '/transfer', component: TransferView },
    // Public User Routes
    { path: '/my-properties', component: PropertiesView }, // Reuse view for now
  ]
})

export default router