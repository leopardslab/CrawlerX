import Vue from "vue";
import Router from "vue-router";
import Dashboard from "../views/Dashboard.vue";
import DashboardPage from "../components/Contents/Dashboard.vue";
import Login from "../views/Login";
import SignUp from "../views/SignUp";
import firebase from 'firebase/compat/app';
import 'firebase/compat/auth';
import 'firebase/compat/firestore';
import Projects from "../components/Contents/Projects";
import Jobs from "../components/Contents/Jobs";
import IntervalJobs from "../components/Contents/IntervalJobs";
import CronJobs from "../components/Contents/CronJobs";
import JobData from "../components/Contents/JobData";
import ScheduleJobData from "../components/Contents/ScheduleJobData";
import ELKAnalysis from "../components/Contents/ELKAnalysis";

Vue.use(Router);

const router = new Router({
  mode: "history",
  routes: [
    {
      path: "*",
      redirect: "login",
    },
    {
      path: "/dashboard",
      component: Dashboard,
      meta: {
        requiresAuth: true,
      },
      children: [
        {
          // UserProfile will be rendered inside User's <router-view>
          // when /user/:id/profile is matched
          path: "",
          component: DashboardPage,
        },
        {
          // UserPosts will be rendered inside User's <router-view>
          // when /user/:id/posts is matched
          path: "projects",
          component: Projects,
        },
        {
          // UserPosts will be rendered inside User's <router-view>
          // when /user/:id/posts is matched
          path: "jobs",
          component: Jobs,
        },
        {
          path: "interval-jobs",
          component: IntervalJobs,
        },
        {
          path: "cron-jobs",
          component: CronJobs,
        },
        {
          // UserPosts will be rendered inside User's <router-view>
          // when /user/:id/posts is matched
          path: "job/:jobId",
          component: JobData,
        },
        {
          path: "schedule-job/:taskId",
          component: ScheduleJobData,
        },
        {
          // UserPosts will be rendered inside User's <router-view>
          // when /user/:id/posts is matched
          path: "analysis",
          component: ELKAnalysis,
        },
      ],
    },
    {
      path: "/about",
      name: "About",
      // route level code-splitting
      // this generates a separate chunk (about.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () =>
        import(/* webpackChunkName: "about" */ "../views/About.vue"),
    },
    {
      path: "/login",
      name: "Login",
      component: Login,
    },
    {
      path: "/signup",
      name: "SignUp",
      component: SignUp,
    },
  ],
});

router.beforeEach((to, from, next) => {
  const currentUser = firebase.auth().currentUser;
  const requiresAuth = to.matched.some((record) => record.meta.requiresAuth);

  if (requiresAuth && !currentUser) next("login");
  else if (!requiresAuth && currentUser) {
    // set user_id from the firebase
    if (
      Vue.prototype.$USER_ID === undefined ||
      Vue.prototype.$USER_ID === null ||
      Vue.prototype.$USER_ID === false
    ) {
      Vue.prototype.$USER_ID = firebase.auth().currentUser.uid;
    }

    // set token_id from the firebase
    if (
      Vue.prototype.$TOKEN_ID === undefined ||
      Vue.prototype.$TOKEN_ID === null ||
      Vue.prototype.$TOKEN_ID === false
    ) {
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

    next("dashboard");
  } else next();
});

export default router;
