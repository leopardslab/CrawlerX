import Vue from 'vue'
import App from './App.vue'
import router from './router'
import firebase from 'firebase'

Vue.config.productionTip = false;

import VueMaterial from 'vue-material'
import 'vue-material/dist/vue-material.min.css'
import 'vue-material/dist/theme/default.css'
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import SidebarMenu from './components/SideBar/SidebarMenu'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

Vue.use(VueMaterial);
Vue.component('sidebar-menu', SidebarMenu);
// Install BootstrapVue
Vue.use(BootstrapVue)
// Optionally install the BootstrapVue icon components plugin
Vue.use(IconsPlugin)

let app = '';

const firebaseConfig = {
  apiKey: "AIzaSyD88ucXoxhnfm3iNUA-FJ-zg-0GrJKT-Zo",
  authDomain: "crawlerx-b2ad1.firebaseapp.com",
  databaseURL: "https://crawlerx-b2ad1.firebaseio.com",
  projectId: "crawlerx-b2ad1",
  storageBucket: "crawlerx-b2ad1.appspot.com",
  messagingSenderId: "811171439353",
  appId: "1:811171439353:web:64e84b4fc347a5c37eb828",
  measurementId: "G-CM2MX0CRRC"
};

firebase.initializeApp(firebaseConfig);

firebase.auth().onAuthStateChanged(() => {
  if (!app) {
    app = new Vue({
      router,
      render: h => h(App)
    }).$mount('#app');
  }
});

