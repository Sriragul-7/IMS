<template>
  <div class="app-layout" v-if="user">
    <button class="mobile-menu-btn" @click="sidebarOpen = !sidebarOpen" aria-label="Toggle menu">
      <span v-html="sidebarOpen ? '&#10005;' : '&#9776;'"></span>
    </button>
    <div class="sidebar-overlay" v-if="sidebarOpen" @click="sidebarOpen = false"></div>

    <aside class="sidebar" :class="{ open: sidebarOpen }">
      <div class="sidebar-brand">
        <div class="brand-mark">BIT</div>
        <div class="brand-text">
          <div class="brand-name">Bannari Amman</div>
          <div class="brand-sub">Institute of Technology</div>
        </div>
      </div>

      <div class="sidebar-child-switcher" v-if="user.role === 'Guardian' && children.length > 1">
        <label class="switcher-label">Viewing</label>
        <div class="child-cards">
          <button v-for="c in children" :key="c.student" class="child-card"
            :class="{ active: selectedChild === c.student }" @click="selectChild(c.student)">
            <span class="child-avatar">{{ getInitials(c.student_name) }}</span>
            <div class="child-info">
              <span class="child-name">{{ c.student_name }}</span>
              <span class="child-program">{{ c.program }}</span>
            </div>
          </button>
        </div>
      </div>

      <nav class="sidebar-nav">
        <router-link v-for="item in navItems" :key="item.to" :to="item.to"
          class="nav-item" :class="{ active: $route.name === item.name }"
          @click="sidebarOpen = false">
          <span class="nav-icon" v-html="item.icon"></span>
          <span class="nav-label">{{ item.label }}</span>
        </router-link>
      </nav>

      <div class="sidebar-footer">
        <div class="sidebar-user">
          <span class="user-avatar">{{ getInitials(user.user_name || user.email) }}</span>
          <div class="user-info">
            <span class="user-name">{{ user.user_name || user.email }}</span>
            <span class="user-role">{{ user.role }}</span>
          </div>
        </div>
        <button class="btn-logout" @click="handleLogout" title="Sign out">
          <span>&#8592;</span>
        </button>
      </div>
    </aside>

    <main class="main-content">
      <header class="top-bar">
        <div class="top-bar-left">
          <h1 class="page-title">{{ currentPageTitle }}</h1>
        </div>
        <div class="top-bar-right">
          <span class="user-role-pill">{{ user.role }}</span>
        </div>
      </header>
      <div class="page-container">
        <router-view :selected-child="selectedChild" />
      </div>
    </main>
  </div>

  <div v-else>
    <router-view />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { getSessionUser, clearSessionUser, logout, callAPI } from './utils/api.js'

const router = useRouter()
const route = useRoute()
const user = ref(null)
const children = ref([])
const selectedChild = ref(null)
const sidebarOpen = ref(false)

const STUDENT_NAV = [
  { name: 'dashboard', to: '/', label: 'Dashboard', icon: '&#9632;' },
  { name: 'profile', to: '/profile', label: 'My Profile', icon: '&#9786;' },
  { name: 'attendance', to: '/attendance', label: 'Attendance', icon: '&#9776;' },
  { name: 'results', to: '/results', label: 'Results', icon: '&#9733;' },
  { name: 'fees', to: '/fees', label: 'Fees', icon: '&#9830;' },
  { name: 'notices', to: '/notices', label: 'Notices', icon: '&#9998;' },
  { name: 'library', to: '/library', label: 'Library', icon: '&#9734;' },
  { name: 'feedback', to: '/feedback', label: 'Feedback', icon: '&#10084;' },
]

const STAFF_NAV = {
  'Instructor': [
    { name: 'instructor-cockpit', to: '/instructor', label: 'Instructor Dashboard', icon: '&#127891;' },
  ],
  'Fee Manager': [
    { name: 'feemanager-cockpit', to: '/fees-manager', label: 'Fee Dashboard', icon: '&#128179;' },
  ],
  'Facility Manager': [
    { name: 'facilitymanager-cockpit', to: '/facility-manager', label: 'Facility Dashboard', icon: '&#127968;' },
  ],
  'Communication Officer': [
    { name: 'communication-cockpit', to: '/communication', label: 'Communication Dashboard', icon: '&#128172;' },
  ],
  'Admissions Officer': [
    { name: 'admissions-cockpit', to: '/admissions', label: 'Admissions Dashboard', icon: '&#128221;' },
  ],
  'Academic Head': [
    { name: 'academichead-cockpit', to: '/academic-head', label: 'Academic Dashboard', icon: '&#127891;' },
  ],
  'System Manager': [
    { name: 'admin-cockpit', to: '/admin', label: 'Admin Dashboard', icon: '&#9881;' },
  ],
}

const navItems = computed(() => {
  if (user.value?.role === 'Guardian' || user.value?.role === 'Student') return STUDENT_NAV
  return STAFF_NAV[user.value?.role] || STUDENT_NAV
})

const currentPageTitle = computed(() => {
  const item = navItems.value.find(i => i.name === route.name)
  return item ? item.label : 'Dashboard'
})

function getInitials(name) {
  if (!name) return '?'
  return name.split(' ').map(w => w[0]).join('').toUpperCase().slice(0, 2)
}

function selectChild(studentId) {
  selectedChild.value = studentId
  localStorage.setItem('institution_portal_selected_child', studentId)
}

async function handleLogout() {
  await logout()
  router.push({ name: 'login' })
}

onMounted(async () => {
  user.value = getSessionUser()
  if (!user.value) {
    router.push({ name: 'login' })
    return
  }

  if (user.value.role === 'Guardian') {
    try {
      const profile = await callAPI('portal_get_profile')
      children.value = profile.children || []
      if (children.value.length > 0) {
        const saved = localStorage.getItem('institution_portal_selected_child')
        selectedChild.value = saved && children.value.find(c => c.student === saved)
          ? saved : children.value[0].student
      }
    } catch (e) {
      console.error('Failed to load guardian profile:', e)
    }
  }
})
</script>

<style scoped>
.app-layout { display: flex; min-height: 100vh; }

.sidebar {
  width: 260px;
  background: var(--gray-900);
  color: var(--gray-300);
  display: flex;
  flex-direction: column;
  position: fixed;
  top: 0; left: 0; bottom: 0;
  z-index: 100;
  overflow-y: auto;
}

.sidebar-brand {
  padding: var(--space-5) var(--space-5);
  display: flex;
  align-items: center;
  gap: var(--space-3);
  border-bottom: 1px solid rgba(255,255,255,0.06);
}

.brand-mark {
  width: 40px; height: 40px;
  border-radius: var(--radius-md);
  background: var(--color-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: var(--text-sm);
  color: white;
  flex-shrink: 0;
}

.brand-text { overflow: hidden; }
.brand-name { font-weight: 600; font-size: var(--text-sm); color: white; line-height: 1.2; }
.brand-sub { font-size: 10px; color: var(--gray-400); line-height: 1.3; }

.sidebar-child-switcher { padding: var(--space-4) var(--space-4); border-bottom: 1px solid rgba(255,255,255,0.06); }
.switcher-label { font-size: 10px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.08em; color: var(--gray-400); display: block; margin-bottom: var(--space-2); }
.child-cards { display: flex; flex-direction: column; gap: var(--space-2); }
.child-card { display: flex; align-items: center; gap: var(--space-3); padding: var(--space-2-5) var(--space-3); border-radius: var(--radius-md); border: 1px solid rgba(255,255,255,0.08); background: rgba(255,255,255,0.03); cursor: pointer; transition: all var(--transition-fast); text-align: left; width: 100%; color: var(--gray-300); }
.child-card:hover { background: rgba(255,255,255,0.06); border-color: rgba(255,255,255,0.12); }
.child-card.active { background: rgba(59,130,246,0.12); border-color: rgba(59,130,246,0.3); color: white; }
.child-avatar { width: 32px; height: 32px; border-radius: var(--radius-sm); background: rgba(255,255,255,0.08); display: flex; align-items: center; justify-content: center; font-size: var(--text-xs); font-weight: 600; flex-shrink: 0; }
.child-card.active .child-avatar { background: var(--color-primary); color: white; }
.child-info { overflow: hidden; }
.child-name { display: block; font-size: var(--text-sm); font-weight: 500; color: inherit; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.child-program { display: block; font-size: 10px; color: var(--gray-400); }

.sidebar-nav { flex: 1; padding: var(--space-3) var(--space-3); overflow-y: auto; }
.nav-item { display: flex; align-items: center; gap: var(--space-3); padding: var(--space-2-5) var(--space-3); border-radius: var(--radius-md); color: var(--gray-400); text-decoration: none; font-size: var(--text-sm); font-weight: 500; transition: all var(--transition-fast); margin-bottom: 2px; }
.nav-item:hover { background: rgba(255,255,255,0.06); color: var(--gray-200); }
.nav-item.active { background: rgba(59,130,246,0.12); color: white; }
.nav-icon { width: 20px; text-align: center; font-size: 14px; flex-shrink: 0; }

.sidebar-footer { padding: var(--space-4) var(--space-4); border-top: 1px solid rgba(255,255,255,0.06); display: flex; align-items: center; justify-content: space-between; }
.sidebar-user { display: flex; align-items: center; gap: var(--space-3); overflow: hidden; min-width: 0; }
.user-avatar { width: 32px; height: 32px; border-radius: var(--radius-full); background: rgba(255,255,255,0.08); display: flex; align-items: center; justify-content: center; font-size: var(--text-xs); font-weight: 600; color: var(--gray-300); flex-shrink: 0; }
.user-info { overflow: hidden; }
.user-name { display: block; font-size: var(--text-sm); font-weight: 500; color: var(--gray-200); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.user-role { display: block; font-size: 10px; color: var(--gray-400); }
.btn-logout { width: 32px; height: 32px; border-radius: var(--radius-md); border: none; background: rgba(255,255,255,0.06); color: var(--gray-400); cursor: pointer; display: flex; align-items: center; justify-content: center; transition: all var(--transition-fast); flex-shrink: 0; }
.btn-logout:hover { background: rgba(220,38,38,0.15); color: #fca5a5; }

.main-content { flex: 1; margin-left: 260px; min-height: 100vh; display: flex; flex-direction: column; }
.top-bar { padding: var(--space-4) var(--space-8); background: var(--color-surface); border-bottom: 1px solid var(--color-border-light); display: flex; justify-content: space-between; align-items: center; position: sticky; top: 0; z-index: 50; }
.page-title { font-size: var(--text-lg); font-weight: 700; color: var(--color-text); }
.user-role-pill { font-size: 11px; padding: var(--space-1) var(--space-3); border-radius: var(--radius-full); background: var(--color-primary-100); color: var(--color-primary); font-weight: 600; }
.page-container { padding: var(--space-6) var(--space-8); flex: 1; }

.mobile-menu-btn { display: none; position: fixed; top: var(--space-3); left: var(--space-3); z-index: 200; width: 40px; height: 40px; border-radius: var(--radius-md); border: none; background: var(--color-primary); color: white; font-size: 18px; cursor: pointer; box-shadow: var(--shadow-md); align-items: center; justify-content: center; }
.sidebar-overlay { display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.5); z-index: 90; backdrop-filter: blur(2px); }

@media (max-width: 768px) {
  .mobile-menu-btn { display: flex; }
  .sidebar { transform: translateX(-100%); transition: transform var(--transition-slow); }
  .sidebar.open { transform: translateX(0); }
  .sidebar-overlay { display: block; }
  .main-content { margin-left: 0; }
  .top-bar { padding: var(--space-3) var(--space-4) var(--space-3) 56px; }
  .page-container { padding: var(--space-4); }
}
</style>
