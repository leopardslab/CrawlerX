import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import firebase from 'firebase/compat/app';
import 'firebase/compat/auth';
import 'firebase/compat/firestore';

Vue.config.productionTip = false;

import VueMaterial from "vue-material";
import "vue-material/dist/vue-material.min.css";
import "vue-material/dist/theme/default.css";
import { BootstrapVue, IconsPlugin } from "bootstrap-vue";
import SidebarMenu from "./components/SideBar/SidebarMenu";
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue/dist/bootstrap-vue.css";
import axios from "axios";
import VueSwal from "vue-swal";
import VueClipboard from "vue-clipboard2";

Vue.use(VueMaterial);
Vue.component("sidebar-menu", SidebarMenu);
// Install BootstrapVue
Vue.use(BootstrapVue);
// Optionally install the BootstrapVue icon components plugin
Vue.use(IconsPlugin);
Vue.use(VueSwal);
Vue.use(VueClipboard);

Vue.prototype.$http = axios;

let app = "";

const firebaseConfig = {
  apiKey: process.env.VUE_APP_FIREBASE_API_KEY,
  authDomain: process.env.VUE_APP_FIREBASE_AUTH_DOMAIN,
  databaseURL: process.env.VUE_APP_FIREBASE_DB_DOMAIN,
  projectId: process.env.VUE_APP_FIREBASE_PROJECT_ID,
  storageBucket: process.env.VUE_APP_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: process.env.VUE_APP_FIREBASE_MESSAGING_SENDER_ID,
  appId: process.env.VUE_APP_FIREBASE_APP_ID,
  measurementId: process.env.VUE_APP_FIREBASE_MEASURMENT_ID,
};
firebase.initializeApp(firebaseConfig);

firebase.auth().onAuthStateChanged(() => {
  if (firebase.auth().currentUser) {
    // set user_id from the firebase
    Vue.prototype.$USER_ID = firebase.auth().currentUser.uid;

    // set token_id from the firebase
    firebase
      .auth()
      .currentUser.getIdToken(/* forceRefresh */ true)
      .then(function(idToken) {
        Vue.prototype.$TOKEN_ID = idToken;
      })
      .catch(function(error) {
        alert(
          "Cannot fetch userId of the current logged user " + error.message
        );
      });
  }

  if (!app) {
    app = new Vue({
      router,
      render: (h) => h(App),
    }).$mount("#app");
  }
});
