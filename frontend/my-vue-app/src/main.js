import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import VueCookies from 'vue-cookies';
import router from './router';
import store from './store'; 
import axios from 'axios';


const app = createApp(App)
axios.defaults.baseURL = 'http://localhost:8000';
axios.defaults.withCredentials = true;
app.use(VueCookies)
app.use(router);
app.use(store); 
app.mount('#app')
