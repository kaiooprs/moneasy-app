import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import DashboardView from '../views/DashboardView.vue'
import WalletsView from '../views/WalletsView.vue'
import SubscriptionView from '../views/SubscriptionView.vue'
import TransactionsView from '../views/TransactionsView.vue'
import AnalyticsView from '../views/AnalyticsView.vue'
import ProfileView from '../views/ProfileView.vue'

const routes = [
  { path: '/', redirect: '/dashboard' },
  { path: '/login', name: 'login', component: LoginView },
  { path: '/dashboard', name: 'dashboard', component: DashboardView, meta: { requiresAuth: true } },
  { path: '/wallets', name: 'wallets', component: WalletsView },
  { path: '/subscriptions', name: 'subscriptions', component: SubscriptionView },
  { path: '/transactions', name: 'transactions', component: () => import('../views/TransactionsView.vue'), meta: { requiresAuth: true}},
  { path: '/analytics', name: 'analytics', component: () => import('../views/AnalyticsView.vue'), meta: { requiresAuth: true}},
  { path: '/profile', name: 'profile', component: ProfileView, meta: { requiresAuth: true}}
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// A MÁGICA ACONTECE AQUI:
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token');

  // 1. Se a rota precisa de login e o Kaio NÃO tem token: vai pro Login
  if (to.meta.requiresAuth && !token) {
    next('/login');
  } 
  // 2. Se o Kaio já está logado e tenta ir pro Login: vai pro Dashboard
  else if (to.path === '/login' && token) {
    next('/dashboard');
  } 
  // 3. Caso contrário: segue viagem normal
  else {
    next();
  }
});

export default router