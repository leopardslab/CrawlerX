import { createRouter, createWebHistory } from 'vue-router';
import Dashboard from '@/views/Dashboard.vue';
import Elasticsearch from '@/views/Elasticsearch.vue';
import Profile from '@/views/Profile.vue';
import SignIn from '@/views/SignIn.vue';
import SignUp from '@/views/SignUp.vue';
import Projects from '@/views/Projects.vue';
import Instant from '@/views/InstantJob.vue';
import Interval from '@/views/IntervalJob.vue';
import Cron from '@/views/CronJob.vue';
import store from "@/store";

const routes = [
  {
    path: '/:catchAll(.*)',
    redirect: '/sign-in',
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: '/projects',
    name: 'Projects',
    component: Projects,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: '/jobs/instant',
    name: 'Instant',
    component: Instant,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: '/jobs/interval',
    name: 'Interval',
    component: Interval,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: '/jobs/cron',
    name: 'Cron',
    component: Cron,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: '/analysis/elasticsearch',
    name: 'Elasticsearch',
    component: Elasticsearch,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: '/sign-in',
    name: 'Sign In',
    component: SignIn,
  },
  {
    path: '/sign-up',
    name: 'Sign Up',
    component: SignUp,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
  linkActiveClass: "active",
});

router.beforeEach((to, from, next) => {
  const currentUser = store.state.user;
  const requiresAuth = to.matched.some((record) => record.meta.requiresAuth);

  if (requiresAuth && currentUser === null) {
    next("SignIn");
  } else if (((to.fullPath === '/sign-in' || to.fullPath === '/sign-up') && currentUser != null)) {
    next("Dashboard");
  } else {
    next();
  }
});

export default router;
