import { createRouter, createWebHashHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import DashboardCommercial from '@/components/DashboardCommercial.vue';
import DashboardComptable from '@/components/DashboardComptable.vue';
import DashboardDirection from '@/components/DashboardDirection.vue';
import RecuperationData from '@/components/RecuperationData.vue';
import Connexion from '@/components/Connexion.vue';
import ForgotPassword from '@/components/ForgotPassword.vue';


const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
    meta: { requiresAuth: true }
  },
  {
    path: '/DashboardCommercial',
    name: 'dashboard-commercial',
    component: DashboardCommercial,
    meta: { requiresAuth: true, accessIds: [1] } // Exemple: Seuls les utilisateurs avec access_id = 1 peuvent accéder
  },
  {
    path: '/DashboardComptable',
    name: 'dashboard-comptable',
    component: DashboardComptable,
    meta: { requiresAuth: true, accessIds: [2] } // Exemple: Seuls les utilisateurs avec access_id = 2 peuvent accéder
  },
  {
    path: '/DashboardDirection',
    name: 'dashboard-direction',
    component: DashboardDirection,
    meta: { requiresAuth: true, accessIds: [3] } // Exemple: Seuls les utilisateurs avec access_id = 3 peuvent accéder
  },
  {
    path: '/RecuperationData',
    name: 'recuperation-data',
    component: RecuperationData,
    meta: { requiresAuth: true } // Exemple: Cette route nécessite une authentification mais pas de restriction spécifique
  },
  {
    path: '/Connexion',
    name: 'se-connecter',
    component: Connexion
  },
  {
    path: '/ForgotPassword',
    name: 'forgot-password',
    component: ForgotPassword
  }
];

const router = createRouter({
  history: createWebHashHistory(),
  routes
});

/*
router.beforeEach((to, from, next) => {
  const isLoggedIn = localStorage.getItem('isLoggedIn');

  if (to.meta.requiresAuth && !isLoggedIn) {
    next('/Connexion');
  } else if (!to.meta.requiresAuth && isLoggedIn) {
    next('/');
  } else {
    next();
  }
});
*/




router.beforeEach((to, from, next) => {
  const isLoggedIn = localStorage.getItem('isLoggedIn');
  const accessIds = JSON.parse(localStorage.getItem('accessIds'));

  // Vérifier si la route nécessite une authentification
  if (to.meta.requiresAuth) {
      // Vérifier si l'utilisateur est connecté
      if (!isLoggedIn) {
          next('/Connexion');
          return;
      }

      // Vérifier si l'utilisateur a les droits d'accès requis
      if (to.meta.accessIds && !to.meta.accessIds.some(accessId => accessIds.includes(accessId))) {
          // Si l'utilisateur n'a pas les droits d'accès nécessaires, rediriger vers la page d'accueil
          next('/');
          return;
      }
  } else if (!to.meta.requiresAuth && isLoggedIn) {
      // Si l'utilisateur est connecté mais tente d'accéder à une page non autorisée, rediriger vers l'accueil
      next('/');
      return;
  }

  next(); // Autoriser la navigation normale
});

export default router;