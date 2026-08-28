import { createApp } from 'vue'
import { createRouter, createWebHashHistory } from 'vue-router'
import App from './App.vue'
import { routes } from './router.js'
import './styles/design-system.css'

const router = createRouter({
  history: createWebHashHistory(),
  routes,
})

const STAFF_ROUTES = {
  'Instructor': 'instructor-cockpit',
  'Fee Manager': 'feemanager-cockpit',
  'Facility Manager': 'facilitymanager-cockpit',
  'Communication Officer': 'communication-cockpit',
  'Admissions Officer': 'admissions-cockpit',
  'Academic Head': 'academichead-cockpit',
  'System Manager': 'admin-cockpit',
}

router.beforeEach((to, from, next) => {
  const user = JSON.parse(localStorage.getItem('institution_portal_user') || 'null')

  if (to.meta.requiresAuth && !user) {
    next({ name: 'login' })
  } else if (to.name === 'login' && user) {
    if (STAFF_ROUTES[user.role]) {
      next({ name: STAFF_ROUTES[user.role] })
    } else {
      next({ name: 'dashboard' })
    }
  } else {
    next()
  }
})

const app = createApp(App)
app.use(router)
app.mount('#app')
