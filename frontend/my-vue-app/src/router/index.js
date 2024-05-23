import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import UploadFiles from '../views/UploadFiles.vue'
import HomeView from '../views/HomeView.vue';
import store from '../store/index.js';
import ProfileView from '../views/ProfileView.vue';
const routes = [
  {
    path: '/login',
    name: 'Login',
    component: LoginView,
  },
  {
    path: '/upload',
    name: 'Upload',
    component: UploadFiles,
    meta: { requiresAuth: true }
  },
  {
    path:'/profile',
    name: 'Profile',
    component: ProfileView,
    meta: { requiresAuth: true }
  },
  {
    path: '/',
    name: 'Home',
    component: HomeView,
  }
]

const BASE_URL = '/';

const router = createRouter({
  history: createWebHistory(BASE_URL),
  routes
})

router.beforeEach((to, from, next) => { // check if user is logged in
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (store.getters.isAuthenticated) {
      next(); 
      return;
    } 
      next('/login')
  } else {
    next();
  }
});


export default router
