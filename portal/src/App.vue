<template>
  <div class="app-layout">
    <AppShell v-if="user" :selected-child="selectedChild" @child-selected="selectedChild = $event">
      <template #default="{ selectedChild, user }">
        <router-view :selected-child="selectedChild" :user="user" />
      </template>
    </AppShell>

    <router-view v-else />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getSessionUser, clearSessionUser, logout, callAPI } from './utils/api.js'
import AppShell from './components/AppShell.vue'

const router = useRouter()
const user = ref(null)
const selectedChild = ref(null)

const PUBLIC_ROUTES = ['login']

onMounted(async () => {
  user.value = getSessionUser()
  
  // Check if current route requires auth
  const requiresAuth = !PUBLIC_ROUTES.includes(router.currentRoute.value.name)
  
  if (requiresAuth && !user.value) {
    router.push({ name: 'login' })
    return
  }
  
  if (user.value && router.currentRoute.value.name === 'login') {
    redirectToDashboard()
    return
  }

  if (user.value?.role === 'Guardian') {
    try {
      const profile = await callAPI('portal_get_profile')
      const children = profile.children || []
      if (children.length > 0) {
        const saved = localStorage.getItem('institution_portal_selected_child')
        selectedChild.value = saved && children.find(c => c.student === saved)
          ? saved : children[0].student
      }
    } catch (e) {
      console.error('Failed to load guardian profile:', e)
    }
  }
})

function redirectToDashboard() {
  if (!user.value) return
  
  const STAFF_ROUTES = {
    'Instructor': 'instructor-cockpit',
    'Fee Manager': 'feemanager-cockpit',
    'Facility Manager': 'facilitymanager-cockpit',
    'Communication Officer': 'communication-cockpit',
    'Admissions Officer': 'admissions-cockpit',
    'Academic Head': 'academichead-cockpit',
    'System Manager': 'admin-cockpit',
  }
  
  if (user.value.role === 'Student' || user.value.role === 'Guardian') {
    router.push({ name: 'dashboard' })
  } else if (STAFF_ROUTES[user.value.role]) {
    router.push({ name: STAFF_ROUTES[user.value.role] })
  } else {
    router.push({ name: 'dashboard' })
  }
}
</script>

<style scoped>
.app-layout { min-height: 100vh; }
</style>