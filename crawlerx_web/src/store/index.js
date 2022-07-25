import { createStore } from "vuex";
import bootstrap from "bootstrap/dist/js/bootstrap.min.js";

//Firebase imports
import { auth } from "@/firebase/config"
import {
  getIdToken,
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  signOut
} from 'firebase/auth'
import router from "@/router";

export default createStore({
  state: {
    hideConfigButton: false,
    isPinned: true,
    showConfig: false,
    isTransparent: "",
    isRTL: false,
    color: "",
    isNavFixed: false,
    isAbsolute: false,
    showNavs: true,
    showSidenav: true,
    showNavbar: true,
    showFooter: true,
    showMain: true,
    navbarFixed:
      "position-sticky blur shadow-blur left-auto top-1 z-index-sticky px-0 mx-4",
    absolute: "position-absolute px-4 mx-0 w-100 z-index-2",
    bootstrap,
    user: null,
    token: null
  },
  created() {
    this.onFirebaseAuthStateChanged();
  },
  mutations: {
    setUser(state, payload) {
      state.user = payload
    },
    setToken(state, payload) {
      state.token = payload
    },
    toggleConfigurator(state) {
      state.showConfig = !state.showConfig;
    },
    navbarMinimize(state) {
      const sidenav_show = document.querySelector(".g-sidenav-show");
      if (sidenav_show.classList.contains("g-sidenav-hidden")) {
        sidenav_show.classList.remove("g-sidenav-hidden");
        sidenav_show.classList.add("g-sidenav-pinned");
        state.isPinned = true;
      } else {
        sidenav_show.classList.add("g-sidenav-hidden");
        sidenav_show.classList.remove("g-sidenav-pinned");
        state.isPinned = false;
      }
    },
    sidebarType(state, payload) {
      state.isTransparent = payload;
    },
    cardBackground(state, payload) {
      state.color = payload;
    },
    navbarFixed(state) {
      if (state.isNavFixed === false) {
        state.isNavFixed = true;
      } else {
        state.isNavFixed = false;
      }
    },
    toggleEveryDisplay(state) {
      state.showNavbar = !state.showNavbar;
      state.showSidenav = !state.showSidenav;
      state.showFooter = !state.showFooter;
    },
    toggleHideConfig(state) {
      state.hideConfigButton = !state.hideConfigButton;
    },
    onFirebaseAuthStateChanged(state) {
      auth.onAuthStateChanged(function(user) {
        if (user) {
          state.user = user;
          state.token = getIdToken(user);
          router.push('/dashboard')
        }
      });
    },
  },
  actions: {
    async signup(context, { email, password }){
      const response = await createUserWithEmailAndPassword(auth, email, password)
      const token = await getIdToken(response.user);
      if (response) {
        context.commit('setUser', response.user)
        context.commit('setToken', token)
      } else {
        alert('Signup failed')
      }
    },
    async login(context, { email, password }){
      const response = await signInWithEmailAndPassword(auth, email, password)
      const token = await getIdToken(response.user);
      if (response) {
        context.commit('setUser', response.user)
        context.commit('setToken', token)
      } else {
        alert('Login failed')
      }
    },
    async logout(context){
      await signOut(auth)
      context.commit('setUser', null)
    },
    toggleSidebarColor({ commit }, payload) {
      commit("sidebarType", payload);
    },
    setCardBackground({ commit }, payload) {
      commit("cardBackground", payload);
    },
  },
  mounted() {

  },
  getters: {},
});
