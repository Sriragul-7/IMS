<template>
  <div class="app-shell">
    <!-- Mobile Menu Button -->
    <button class="mobile-menu-btn" @click="sidebarOpen = true" aria-label="Open menu" aria-expanded="false">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <line x1="3" y1="6" x2="21" y2="6"></line>
        <line x1="3" y1="12" x2="21" y2="12"></line>
        <line x1="3" y1="18" x2="21" y2="18"></line>
      </svg>
    </button>

    <!-- Sidebar Overlay (Mobile) -->
    <div class="sidebar-overlay" v-if="sidebarOpen" @click="sidebarOpen = false" aria-hidden="true"></div>

    <!-- Sidebar -->
    <aside class="sidebar" :class="{ open: sidebarOpen, collapsed: sidebarCollapsed }" role="navigation" aria-label="Main navigation">
      <div class="sidebar-header">
        <div class="sidebar-brand" @click="toggleSidebarCollapse" title="Toggle sidebar">
          <div class="brand-mark" aria-hidden="true">
            <svg viewBox="0 0 40 40" width="28" height="28" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect width="40" height="40" rx="10" fill="currentColor"/>
              <path d="M12 14h16M12 20h12M12 26h8" stroke="white" stroke-width="3" stroke-linecap="round"/>
            </svg>
          </div>
          <div class="brand-text" v-show="!sidebarCollapsed">
            <div class="brand-name">Bannari Amman</div>
            <div class="brand-sub">Institute of Technology</div>
          </div>
          <button class="sidebar-collapse-btn" @click.stop="toggleSidebarCollapse" aria-label="Collapse sidebar" v-show="!sidebarCollapsed">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="15 18 9 12 15 6"></polyline>
            </svg>
          </button>
        </div>
      </div>

      <!-- Guardian Child Switcher -->
      <div class="sidebar-child-switcher" v-if="user.role === 'Guardian' && children.length > 1 && !sidebarCollapsed">
        <div class="switcher-header">
          <span class="switcher-label">Viewing as</span>
        </div>
        <div class="child-cards">
          <button v-for="c in children" :key="c.student" class="child-card" :class="{ active: selectedChild === c.student }" @click="selectChild(c.student)">
            <AvatarChip :name="c.student_name" size="sm" :color-index="getColorIndex(c.student)" class="child-avatar" />
            <div class="child-info">
              <span class="child-name">{{ c.student_name }}</span>
              <span class="child-program">{{ c.program }}</span>
            </div>
            <span v-if="selectedChild === c.student" class="child-active-indicator" aria-hidden="true">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
            </span>
          </button>
        </div>
      </div>

      <!-- Navigation -->
      <nav class="sidebar-nav" role="menu" aria-label="Portal navigation">
        <router-link v-for="item in navItems" :key="item.name" :to="item.to" class="nav-item" :class="{ active: $route.name === item.name }" role="menuitem" @click="sidebarOpen = false">
          <span class="nav-icon" v-html="item.icon" aria-hidden="true"></span>
          <span class="nav-label" v-show="!sidebarCollapsed">{{ item.label }}</span>
        </router-link>
      </nav>

      <!-- Sidebar Footer -->
      <div class="sidebar-footer">
        <div class="sidebar-user" v-show="!sidebarCollapsed">
          <AvatarChip :name="user.user_name || user.email" size="sm" :color-index="getColorIndex(user.email)" class="user-avatar" />
          <div class="user-info">
            <span class="user-name">{{ user.user_name || user.email }}</span>
            <span class="user-role">{{ user.role }}</span>
          </div>
        </div>
        <div class="sidebar-user-compact" v-show="sidebarCollapsed">
          <AvatarChip :name="user.user_name || user.email" size="sm" :color-index="getColorIndex(user.email)" />
        </div>
        <div class="sidebar-actions">
          <button class="btn-icon" @click="openDemoGuide" title="Demo Guide" aria-label="Open demo guide">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"></circle>
              <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"></path>
              <line x1="12" y1="17" x2="12.01" y2="17"></line>
            </svg>
          </button>
          <button class="btn-icon" @click="switchRole" title="Switch Role" aria-label="Switch role">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
              <circle cx="9" cy="7" r="4"></circle>
              <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
              <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
            </svg>
          </button>
          <button class="btn-icon btn-logout" @click="handleLogout" title="Sign out" aria-label="Sign out">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
              <polyline points="16 17 21 12 16 7"></polyline>
              <line x1="21" y1="12" x2="9" y2="12"></line>
            </svg>
          </button>
        </div>
      </div>
    </aside>

    <!-- Top Bar -->
    <header class="top-bar" role="banner">
      <div class="top-bar-left">
        <h1 class="page-title">{{ currentPageTitle }}</h1>
        <nav class="breadcrumb" v-if="breadcrumbs.length" aria-label="Breadcrumb">
          <ol class="breadcrumb-list">
            <li v-for="(crumb, i) in breadcrumbs" :key="crumb.label" class="breadcrumb-item">
              <router-link v-if="i < breadcrumbs.length - 1 && crumb.to" :to="crumb.to" class="breadcrumb-link">{{ crumb.label }}</router-link>
              <span v-else class="breadcrumb-current">{{ crumb.label }}</span>
              <svg v-if="i < breadcrumbs.length - 1" class="breadcrumb-sep" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                <polyline points="9 18 15 12 9 6"></polyline>
              </svg>
            </li>
          </ol>
        </nav>
      </div>
      <div class="top-bar-right">
        <div class="top-bar-search" v-if="showSearch">
          <svg class="search-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
          <input type="search" class="search-input" placeholder="Search..." @input="handleSearch" @focus="searchFocused = true" @blur="searchFocused = false" />
          <div class="search-results" v-if="searchFocused && searchResults.length">
            <div v-for="r in searchResults" :key="r.id" class="search-result-item" @click="selectSearchResult(r)">
              <span class="search-result-icon" v-html="r.icon"></span>
              <span class="search-result-text">{{ r.label }}</span>
            </div>
          </div>
        </div>
        <button class="btn-icon top-bar-notification" @click="toggleNotifications" aria-label="Notifications" :aria-expanded="notificationsOpen">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path>
            <path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
          </svg>
          <span v-if="notificationCount > 0" class="notification-badge">{{ notificationCount > 9 ? '9+' : notificationCount }}</span>
        </button>
        <div class="notifications-dropdown" v-if="notificationsOpen" role="menu">
          <div class="dropdown-header">
            <span>Notifications</span>
            <button class="btn-link" @click="markAllRead">Mark all read</button>
          </div>
          <div class="dropdown-list" v-if="notifications.length">
            <div v-for="n in notifications" :key="n.id" class="dropdown-item" :class="{ unread: !n.read }" role="menuitem" @click="handleNotificationClick(n)">
              <div class="notification-dot" v-if="!n.read"></div>
              <div class="notification-content">
                <span class="notification-title">{{ n.title }}</span>
                <span class="notification-time">{{ formatTime(n.time) }}</span>
              </div>
            </div>
          </div>
          <div class="dropdown-empty" v-else>No notifications</div>
          <div class="dropdown-footer">
            <a href="/app/notifications" class="btn-link" target="_blank">View all</a>
          </div>
        </div>
        <div class="user-menu-wrapper" @click="toggleUserMenu">
          <AvatarChip :name="user.user_name || user.email" size="sm" :color-index="getColorIndex(user.email)" class="topbar-avatar" />
          <span class="topbar-user-name" v-show="!isMobile">{{ user.user_name || user.email }}</span>
          <svg class="topbar-chevron" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="18 15 12 9 6 15"></polyline>
          </svg>
        </div>
        <div class="user-menu-dropdown" v-if="userMenuOpen" role="menu">
          <div class="user-menu-header">
            <AvatarChip :name="user.user_name || user.email" size="md" :color-index="getColorIndex(user.email)" />
            <div>
              <div class="user-menu-name">{{ user.user_name || user.email }}</div>
              <div class="user-menu-role">{{ user.role }}</div>
            </div>
          </div>
          <div class="user-menu-divider"></div>
          <button class="user-menu-item" role="menuitem" @click="goToProfile">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
            Profile
          </button>
          <button class="user-menu-item" role="menuitem" @click="switchRole">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>
            Switch Role
          </button>
          <button class="user-menu-item user-menu-item--danger" role="menuitem" @click="handleLogout">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path><polyline points="16 17 21 12 16 7"></polyline><line x1="21" y1="12" x2="9" y2="12"></line></svg>
            Sign Out
          </button>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="main-content" role="main">
      <div class="page-container">
        <slot :selected-child="selectedChild" :user="user" />
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch, nextTick } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { getSessionUser, clearSessionUser, logout, callAPI } from '../utils/api.js'
import AvatarChip from './AvatarChip.vue'

const router = useRouter()
const route = useRoute()

const user = ref(null)
const children = ref([])
const selectedChild = ref(null)
const sidebarOpen = ref(false)
const sidebarCollapsed = ref(false)
const userMenuOpen = ref(false)
const notificationsOpen = ref(false)
const searchFocused = ref(false)
const searchQuery = ref('')
const searchResults = ref([])

const STUDENT_NAV = [
  { name: 'dashboard', to: '/', label: 'Dashboard', icon: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7" rx="1"></rect><rect x="14" y="3" width="7" height="7" rx="1"></rect><rect x="3" y="14" width="7" height="7" rx="1"></rect><rect x="14" y="14" width="7" height="7" rx="1"></rect></svg>' },
  { name: 'profile', to: '/profile', label: 'My Profile', icon: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>' },
  { name: 'attendance', to: '/attendance', label: 'Attendance', icon: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>' },
  { name: 'results', to: '/results', label: 'Results', icon: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>' },
  { name: 'fees', to: '/fees', label: 'Fees', icon: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="1" x2="12" y2="23"></line><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path></svg>' },
  { name: 'notices', to: '/notices', label: 'Notices', icon: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>' },
  { name: 'library', to: '/library', label: 'Library', icon: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path></svg>' },
  { name: 'feedback', to: '/feedback', label: 'Feedback', icon: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>' }
]

const STAFF_NAV = {
  'Instructor': [
    { name: 'instructor-cockpit', to: '/instructor', label: 'Instructor Dashboard', icon: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path></svg>' }
  ],
  'Fee Manager': [
    { name: 'feemanager-cockpit', to: '/fees-manager', label: 'Fee Dashboard', icon: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="1" x2="12" y2="23"></line><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path></svg>' }
  ],
  'Facility Manager': [
    { name: 'facilitymanager-cockpit', to: '/facility-manager', label: 'Facility Dashboard', icon: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>' }
  ],
  'Communication Officer': [
    { name: 'communication-cockpit', to: '/communication', label: 'Communication Dashboard', icon: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>' }
  ],
  'Admissions Officer': [
    { name: 'admissions-cockpit', to: '/admissions', label: 'Admissions Dashboard', icon: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>' }
  ],
  'Academic Head': [
    { name: 'academichead-cockpit', to: '/academic-head', label: 'Academic Dashboard', icon: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path></svg>' }
  ],
  'System Manager': [
    { name: 'admin-cockpit', to: '/admin', label: 'Admin Dashboard', icon: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg>' }
  ],
}

const navItems = computed(() => {
  if (!user.value) return []
  if (user.value.role === 'Guardian' || user.value.role === 'Student') return STUDENT_NAV
  return STAFF_NAV[user.value.role] || STUDENT_NAV
})

const currentPageTitle = computed(() => {
  const item = navItems.value.find(i => i.name === route.name)
  return item ? item.label : 'Dashboard'
})

const breadcrumbs = computed(() => {
  const matched = route.matched.filter(m => m.meta.title)
  return matched.map(m => ({ label: m.meta.title, to: m.path }))
})

const isMobile = computed(() => window.innerWidth < 768)

const showSearch = computed(() => user.value && !['Student', 'Guardian'].includes(user.value.role))

const notificationCount = ref(3)
const notifications = ref([
  { id: 1, title: 'New fee payment received', time: Date.now() - 300000, read: false },
  { id: 2, title: 'Attendance marked for CS101', time: Date.now() - 1800000, read: false },
  { id: 3, title: 'Results published for Mid Term', time: Date.now() - 3600000, read: true }
])

function getColorIndex(str) {
  let hash = 0
  for (let i = 0; i < str.length; i++) {
    hash = str.charCodeAt(i) + ((hash << 5) - hash)
  }
  return Math.abs(hash) % 10
}

function toggleSidebarCollapse() {
  sidebarCollapsed.value = !sidebarCollapsed.value
}

function selectChild(studentId) {
  selectedChild.value = studentId
  localStorage.setItem('institution_portal_selected_child', studentId)
}

async function handleLogout() {
  await logout()
  router.push({ name: 'login' })
}

function goToProfile() {
  userMenuOpen.value = false
  router.push({ name: 'profile' })
}

function switchRole() {
  userMenuOpen.value = false
  handleLogout()
}

function openDemoGuide() {
  // Will be implemented in Phase F
  console.log('Open demo guide')
}

function toggleUserMenu() {
  userMenuOpen.value = !userMenuOpen.value
  notificationsOpen.value = false
}

function toggleNotifications() {
  notificationsOpen.value = !notificationsOpen.value
  userMenuOpen.value = false
}

function handleSearch() {
  // Search logic here
}

function selectSearchResult(result) {
  searchFocused.value = false
  searchQuery.value = ''
  if (result.route) router.push(result.route)
}

function handleNotificationClick(notification) {
  notification.read = true
  notificationCount.value = Math.max(0, notificationCount.value - 1)
  notificationsOpen.value = false
}

function formatTime(time) {
  const diff = Date.now() - time
  const minutes = Math.floor(diff / 60000)
  const hours = Math.floor(diff / 3600000)
  const days = Math.floor(diff / 86400000)
  if (minutes < 1) return 'Just now'
  if (minutes < 60) return `${minutes}m ago`
  if (hours < 24) return `${hours}h ago`
  return `${days}d ago`
}

function markAllRead() {
  notifications.value.forEach(n => n.read = true)
  notificationCount.value = 0
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

  const savedCollapsed = localStorage.getItem('institution_sidebar_collapsed')
  if (savedCollapsed !== null) {
    sidebarCollapsed.value = savedCollapsed === 'true'
  }
})

watch(sidebarCollapsed, (val) => {
  localStorage.setItem('institution_sidebar_collapsed', val.toString())
})

// Close dropdowns on outside click
document.addEventListener('click', (e) => {
  if (!e.target.closest('.user-menu-wrapper')) userMenuOpen.value = false
  if (!e.target.closest('.top-bar-notification')) notificationsOpen.value = false
  if (!e.target.closest('.top-bar-search')) searchFocused.value = false
})
</script>

<style scoped>
.app-shell { display: flex; min-height: 100vh; background: var(--color-bg); }

/* Mobile Menu Button */
.mobile-menu-btn {
  display: none;
  position: fixed;
  top: var(--space-4);
  left: var(--space-4);
  z-index: var(--z-fixed);
  width: 44px;
  height: 44px;
  border-radius: var(--radius-lg);
  border: none;
  background: var(--color-primary);
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: var(--shadow-lg);
  transition: all var(--transition-fast);
}
.mobile-menu-btn:hover { background: var(--color-primary-hover); transform: scale(1.02); }

.sidebar-overlay {
  display: none;
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.5);
  z-index: calc(var(--z-fixed) - 10);
  backdrop-filter: blur(2px);
  animation: fadeIn var(--transition-base);
}

/* Sidebar */
.sidebar {
  width: 280px;
  min-width: 280px;
  background: var(--color-primary);
  color: var(--gray-300);
  display: flex;
  flex-direction: column;
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  z-index: var(--z-fixed);
  overflow-y: auto;
  transition: transform var(--transition-slow), width var(--transition-base), min-width var(--transition-base);
}
.sidebar.collapsed {
  width: 72px;
  min-width: 72px;
}
.sidebar.open { transform: translateX(0); }

.sidebar-header { padding: var(--space-4) var(--space-4); border-bottom: 1px solid rgba(255,255,255,0.06); }
.sidebar-brand {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  cursor: pointer;
  padding: var(--space-2);
  border-radius: var(--radius-lg);
  transition: background var(--transition-fast);
}
.sidebar-brand:hover { background: rgba(255,255,255,0.05); }
.brand-mark {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-lg);
  background: var(--color-accent);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  color: white;
  box-shadow: var(--shadow-md);
}
.brand-text { overflow: hidden; flex: 1; min-width: 0; }
.brand-name { font-weight: var(--font-weight-semibold); font-size: var(--text-sm); color: white; line-height: 1.2; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.brand-sub { font-size: 10px; color: var(--gray-400); line-height: 1.3; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.sidebar-collapse-btn {
  width: 28px;
  height: 28px;
  border-radius: var(--radius-md);
  border: none;
  background: rgba(255,255,255,0.1);
  color: var(--gray-300);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--transition-fast);
  flex-shrink: 0;
}
.sidebar-collapse-btn:hover { background: rgba(255,255,255,0.15); color: white; }

.sidebar-child-switcher { padding: var(--space-4) var(--space-4); border-bottom: 1px solid rgba(255,255,255,0.06); }
.switcher-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: var(--space-3); }
.switcher-label { font-size: 10px; font-weight: var(--font-weight-semibold); text-transform: uppercase; letter-spacing: 0.08em; color: var(--gray-400); }
.child-cards { display: flex; flex-direction: column; gap: var(--space-2); }
.child-card {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-2-5) var(--space-3);
  border-radius: var(--radius-md);
  border: 1px solid rgba(255,255,255,0.08);
  background: rgba(255,255,255,0.03);
  cursor: pointer;
  transition: all var(--transition-fast);
  text-align: left;
  width: 100%;
  color: var(--gray-300);
  position: relative;
}
.child-card:hover { background: rgba(255,255,255,0.06); border-color: rgba(255,255,255,0.12); }
.child-card.active { background: rgba(14, 184, 166, 0.15); border-color: rgba(14, 184, 166, 0.4); color: white; }
.child-avatar { flex-shrink: 0; }
.child-info { overflow: hidden; flex: 1; }
.child-name { display: block; font-size: var(--text-sm); font-weight: var(--font-weight-medium); color: inherit; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.child-program { display: block; font-size: 10px; color: var(--gray-400); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.child-card.active .child-program { color: rgba(255,255,255,0.7); }
.child-active-indicator { color: var(--color-accent); flex-shrink: 0; }

.sidebar-nav { flex: 1; padding: var(--space-4) var(--space-3); overflow-y: auto; }
.nav-item {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3) var(--space-3);
  border-radius: var(--radius-md);
  color: var(--gray-400);
  text-decoration: none;
  font-size: var(--text-sm);
  font-weight: var(--font-weight-medium);
  transition: all var(--transition-fast);
  margin-bottom: 2px;
  role: menuitem;
  white-space: nowrap;
}
.nav-item:hover { background: rgba(255,255,255,0.06); color: var(--gray-200); }
.nav-item.active { background: rgba(14, 184, 166, 0.15); color: white; }
.nav-icon { width: 20px; text-align: center; font-size: 18px; flex-shrink: 0; }
.nav-label { overflow: hidden; text-overflow: ellipsis; }

.sidebar-footer { padding: var(--space-4) var(--space-4); border-top: 1px solid rgba(255,255,255,0.06); display: flex; align-items: center; justify-content: space-between; }
.sidebar-user { display: flex; align-items: center; gap: var(--space-3); overflow: hidden; min-width: 0; flex: 1; }
.user-avatar { flex-shrink: 0; }
.user-info { overflow: hidden; }
.user-name { display: block; font-size: var(--text-sm); font-weight: var(--font-weight-medium); color: var(--gray-200); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.user-role { display: block; font-size: 10px; color: var(--gray-400); }
.sidebar-user-compact { display: none; justify-content: center; }
.sidebar.collapsed .sidebar-user-compact { display: flex; }
.sidebar-actions { display: flex; align-items: center; gap: var(--space-1); }
.btn-icon {
  width: 36px;
  height: 36px;
  border-radius: var(--radius-md);
  border: none;
  background: rgba(255,255,255,0.06);
  color: var(--gray-400);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--transition-fast);
  flex-shrink: 0;
}
.btn-icon:hover { background: rgba(14, 184, 166, 0.15); color: var(--color-accent-light); }
.btn-logout:hover { background: rgba(220,38,38,0.15); color: #fca5a5; }

/* Top Bar */
.top-bar {
  padding: var(--space-4) var(--space-8);
  background: var(--color-surface);
  border-bottom: 1px solid var(--color-border-light);
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: sticky;
  top: 0;
  z-index: var(--z-sticky);
  gap: var(--space-4);
  flex-wrap: wrap;
}
.top-bar-left { display: flex; flex-direction: column; gap: var(--space-2); flex: 1; min-width: 0; }
.page-title { font-size: var(--text-xl); font-weight: var(--font-weight-bold); color: var(--color-text); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.breadcrumb { display: flex; align-items: center; }
.breadcrumb-list { display: flex; align-items: center; gap: 0; list-style: none; font-size: var(--text-sm); }
.breadcrumb-item { display: flex; align-items: center; gap: var(--space-1-5); }
.breadcrumb-link { color: var(--color-text-secondary); transition: color var(--transition-fast); }
.breadcrumb-link:hover { color: var(--color-accent); }
.breadcrumb-current { color: var(--color-text); font-weight: var(--font-weight-medium); }
.breadcrumb-sep { color: var(--gray-300); flex-shrink: 0; }

.top-bar-right { display: flex; align-items: center; gap: var(--space-3); flex-shrink: 0; }

.top-bar-search { position: relative; }
.search-icon { position: absolute; left: var(--space-3); top: 50%; transform: translateY(-50%); color: var(--color-text-muted); pointer-events: none; }
.search-input {
  width: 280px;
  padding: var(--space-2) var(--space-3) var(--space-2) 40px;
  font-size: var(--text-sm);
  font-family: inherit;
  color: var(--color-text);
  background: var(--gray-50);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-full);
  outline: none;
  transition: all var(--transition-fast);
}
.search-input:focus { width: 320px; background: var(--color-surface); border-color: var(--color-accent-light); box-shadow: 0 0 0 3px var(--color-accent-50); }
.search-input::placeholder { color: var(--color-text-muted); }
.search-results {
  position: absolute;
  top: calc(100% + var(--space-2));
  right: 0;
  width: 320px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-xl);
  overflow: hidden;
  z-index: var(--z-dropdown);
}
.search-result-item { display: flex; align-items: center; gap: var(--space-3); padding: var(--space-3) var(--space-4); cursor: pointer; transition: background var(--transition-fast); }
.search-result-item:hover { background: var(--gray-50); }
.search-result-icon { font-size: 1.125rem; }
.search-result-text { font-size: var(--text-sm); color: var(--color-text); }

.top-bar-notification { position: relative; }
.notification-badge {
  position: absolute;
  top: -2px;
  right: -2px;
  min-width: 18px;
  height: 18px;
  border-radius: var(--radius-full);
  background: var(--color-danger);
  color: white;
  font-size: 10px;
  font-weight: var(--font-weight-bold);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 5px;
}
.notifications-dropdown {
  position: absolute;
  top: calc(100% + var(--space-2));
  right: 0;
  width: 360px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-xl);
  overflow: hidden;
  z-index: var(--z-dropdown);
  animation: slideDown var(--transition-fast);
}
.dropdown-header { display: flex; justify-content: space-between; align-items: center; padding: var(--space-3) var(--space-4); border-bottom: 1px solid var(--color-border-light); }
.dropdown-header span { font-weight: var(--font-weight-semibold); color: var(--color-text); }
.btn-link { background: none; border: none; color: var(--color-accent); font-size: var(--text-sm); font-weight: var(--font-weight-medium); cursor: pointer; padding: 0; }
.btn-link:hover { text-decoration: underline; }
.dropdown-list { max-height: 300px; overflow-y: auto; }
.dropdown-item { display: flex; align-items: flex-start; gap: var(--space-3); padding: var(--space-3) var(--space-4); cursor: pointer; transition: background var(--transition-fast); border-bottom: 1px solid var(--color-border-light); }
.dropdown-item:last-child { border-bottom: none; }
.dropdown-item:hover { background: var(--gray-50); }
.dropdown-item.unread { background: var(--color-primary-50); }
.notification-dot { width: 8px; height: 8px; border-radius: 50%; background: var(--color-accent); flex-shrink: 0; margin-top: 2px; }
.notification-content { flex: 1; min-width: 0; }
.notification-title { display: block; font-size: var(--text-sm); font-weight: var(--font-weight-medium); color: var(--color-text); margin-bottom: 2px; }
.notification-time { font-size: var(--text-xs); color: var(--color-text-muted); }
.dropdown-empty { padding: var(--space-6); text-align: center; color: var(--color-text-muted); font-size: var(--text-sm); }
.dropdown-footer { padding: var(--space-3) var(--space-4); border-top: 1px solid var(--color-border-light); text-align: center; }

.user-menu-wrapper { display: flex; align-items: center; gap: var(--space-2); cursor: pointer; padding: var(--space-1) var(--space-2); border-radius: var(--radius-md); transition: background var(--transition-fast); }
.user-menu-wrapper:hover { background: var(--gray-100); }
.topbar-avatar { flex-shrink: 0; }
.topbar-user-name { font-size: var(--text-sm); font-weight: var(--font-weight-medium); color: var(--color-text); white-space: nowrap; }
.topbar-chevron { color: var(--color-text-muted); transition: transform var(--transition-fast); }
.user-menu-wrapper:hover .topbar-chevron { transform: rotate(180deg); }
.user-menu-dropdown {
  position: absolute;
  top: calc(100% + var(--space-2));
  right: 0;
  width: 240px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-xl);
  overflow: hidden;
  z-index: var(--z-dropdown);
  animation: slideDown var(--transition-fast);
}
.user-menu-header { display: flex; align-items: center; gap: var(--space-3); padding: var(--space-4); border-bottom: 1px solid var(--color-border-light); }
.user-menu-name { font-weight: var(--font-weight-semibold); color: var(--color-text); }
.user-menu-role { font-size: var(--text-xs); color: var(--color-text-muted); text-transform: capitalize; }
.user-menu-divider { height: 1px; background: var(--color-border-light); }
.user-menu-item {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  width: 100%;
  padding: var(--space-3) var(--space-4);
  background: none;
  border: none;
  color: var(--color-text);
  font-size: var(--text-sm);
  font-weight: var(--font-weight-medium);
  text-align: left;
  cursor: pointer;
  transition: background var(--transition-fast);
}
.user-menu-item:hover { background: var(--gray-50); }
.user-menu-item--danger { color: var(--color-danger); }
.user-menu-item--danger:hover { background: var(--color-danger-light); }

/* Main Content */
.main-content {
  flex: 1;
  margin-left: 280px;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  transition: margin-left var(--transition-base);
}
.sidebar.collapsed + .main-content { margin-left: 72px; }
.page-container { padding: var(--space-6) var(--space-8); flex: 1; width: 100%; }

/* Animations */
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes slideDown { from { opacity: 0; transform: translateY(-8px); } to { opacity: 1; transform: translateY(0); } }

/* Responsive */
@media (max-width: 1024px) {
  .top-bar { padding: var(--space-3) var(--space-6); }
  .page-container { padding: var(--space-5) var(--space-6); }
}
@media (max-width: 768px) {
  .mobile-menu-btn { display: flex; }
  .sidebar { transform: translateX(-100%); }
  .sidebar.open { transform: translateX(0); }
  .sidebar-overlay { display: block; }
  .main-content { margin-left: 0; }
  .sidebar.collapsed + .main-content { margin-left: 0; }
  .top-bar { padding: var(--space-3) var(--space-4) var(--space-3) 56px; }
  .page-container { padding: var(--space-4); }
  .page-title { font-size: var(--text-lg); }
  .breadcrumb { display: none; }
  .search-input { width: 200px; }
  .search-input:focus { width: 240px; }
  .topbar-user-name { display: none; }
}
@media (max-width: 480px) {
  .top-bar { padding: var(--space-2) var(--space-3) var(--space-2) 50px; }
  .notifications-dropdown, .user-menu-dropdown { right: -20px; width: calc(100vw - 40px); max-width: 360px; }
  .search-input { width: 160px; }
  .search-input:focus { width: 200px; }
}
</style>