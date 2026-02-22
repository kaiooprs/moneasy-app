import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import DashboardView from '../views/DashboardView.vue'
import WalletsView from '../views/WalletsView.vue'
import SubscriptionView from '../views/SubscriptionView.vue'
import TransactionsView from '../views/TransactionsView.vue'
import AnalyticsView from '../views/AnalyticsView.vue'
import ProfileView from '../views/ProfileView.vue'
import CategoriesView from '../views/CategoriesView.vue';

const routes = [
  { path: '/', redirect: '/dashboard' },
  { path: '/login', name: 'login', component: LoginView },
  { path: '/dashboard', name: 'dashboard', component: DashboardView, meta: { requiresAuth: true } },
  { path: '/wallets', name: 'wallets', component: WalletsView },
  { path: '/subscriptions', name: 'subscriptions', component: SubscriptionView },
  { path: '/transactions', name: 'transactions', component: () => import('../views/TransactionsView.vue'), meta: { requiresAuth: true}},
  { path: '/analytics', name: 'analytics', component: () => import('../views/AnalyticsView.vue'), meta: { requiresAuth: true}},
  { path: '/profile', name: 'profile', component: ProfileView, meta: { requiresAuth: true}},
  { path: '/categories', name: 'categories', component: CategoriesView, meta: { requiresAuth: true }}
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token');

  if (to.meta.requiresAuth && !token) {
    next('/login');
  } 
  else if (to.path === '/login' && token) {
    next('/dashboard');
  } 
  else {
    next();
  }
});

export default router