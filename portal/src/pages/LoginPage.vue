<template>
  <div class="login-page">
    <div class="login-left">
      <div class="login-brand-panel">
        <div class="brand-mark-lg">BIT</div>
        <h1>Bannari Amman<br/>Institute of Technology</h1>
        <p>Student & Staff Portal</p>
        <div class="brand-features">
          <div class="feature-item"><span class="feature-icon">&#10003;</span> Attendance Tracking</div>
          <div class="feature-item"><span class="feature-icon">&#10003;</span> Results & Grades</div>
          <div class="feature-item"><span class="feature-icon">&#10003;</span> Fee Management</div>
          <div class="feature-item"><span class="feature-icon">&#10003;</span> Library Services</div>
          <div class="feature-item"><span class="feature-icon">&#10003;</span> Staff Cockpit</div>
        </div>
      </div>
    </div>
    <div class="login-right">
      <div class="login-card">
        <div class="login-header">
          <div class="brand-mark-sm">BIT</div>
          <h2>Welcome back</h2>
          <p>Sign in to your portal account</p>
        </div>

        <form @submit.prevent="handleLogin" class="login-form">
          <div v-if="error" class="login-alert">
            <span class="alert-icon">&#9888;</span>
            {{ error }}
          </div>

          <div class="form-group">
            <label class="form-label">Email address</label>
            <input v-model="email" type="email" class="form-input" placeholder="you@institution.local" required autofocus />
          </div>

          <div class="form-group">
            <label class="form-label">Password</label>
            <input v-model="password" type="password" class="form-input" placeholder="Enter your password" required />
          </div>

          <button type="submit" class="btn btn-primary btn-lg login-btn" :disabled="loading">
            <span v-if="loading" class="spinner" style="width:16px;height:16px;border-width:2px;"></span>
            {{ loading ? 'Signing in...' : 'Sign In' }}
          </button>
        </form>

        <div class="demo-section">
          <div class="demo-divider"><span>Quick Demo Access</span></div>
          <div class="demo-grid">
            <button v-for="d in demos" :key="d.email" class="demo-btn" @click="fillDemo(d)">
              <span class="demo-avatar" :style="{ background: d.color }">{{ d.initials }}</span>
              <div class="demo-text">
                <span class="demo-role">{{ d.role }}</span>
                <span class="demo-email">{{ d.email }}</span>
              </div>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { login, setSessionUser, callAPI } from '../utils/api.js'

const router = useRouter()
const email = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

const demos = [
  { email: 'richdemo@demo.institution.local', role: 'Student', initials: 'SJ', color: '#1e40af' },
  { email: 'student1@demo.institution.local', role: 'Student', initials: 'AK', color: '#3b82f6' },
  { email: 'guardian1@demo.institution.local', role: 'Guardian', initials: 'AN', color: '#7c3aed' },
  { email: 'guardian2@demo.institution.local', role: 'Guardian', initials: 'PH', color: '#6366f1' },
  { email: 'instructor1@demo.institution.local', role: 'Staff', initials: 'I1', color: '#059669' },
  { email: 'feemanager@demo.institution.local', role: 'Staff', initials: 'FM', color: '#d97706' },
  { email: 'academichead@demo.institution.local', role: 'Staff', initials: 'AH', color: '#2563eb' },
  { email: 'comms.officer@demo.institution.local', role: 'Staff', initials: 'CO', color: '#7c3aed' },
  { email: 'admin@demo.institution.local', role: 'Admin', initials: 'AD', color: '#0f172a' },
]

function fillDemo(d) {
  email.value = d.email
  password.value = 'Demo@2026'
}

const STAFF_ROLES = {
  'Instructor': { cockpit: 'instructor-cockpit', route: '/instructor' },
  'Fee Manager': { cockpit: 'feemanager-cockpit', route: '/fees-manager' },
  'Facility Manager': { cockpit: 'facilitymanager-cockpit', route: '/facility-manager' },
  'Communication Officer': { cockpit: 'communication-cockpit', route: '/communication' },
  'Admissions Officer': { cockpit: 'admissions-cockpit', route: '/admissions' },
  'Academic Head': { cockpit: 'academichead-cockpit', route: '/academic-head' },
  'System Manager': { cockpit: 'admin-cockpit', route: '/admin' },
}

async function handleLogin() {
  loading.value = true
  error.value = ''
  try {
    await login(email.value, password.value)
    let profile
    try {
      profile = await callAPI('portal_get_profile')
    } catch (portalErr) {
      profile = await callAPI('portal_get_staff_profile')
    }

    const isStaff = profile.type === 'staff'
    const isGuardian = profile.type === 'guardian'

    setSessionUser({
      email: email.value,
      role: isStaff ? profile.role : (isGuardian ? 'Guardian' : 'Student'),
      user_name: isStaff ? profile.full_name : (profile.student_name || profile.guardian_name),
      record_name: profile.name,
    })

    if (isStaff) {
      const staffRoute = STAFF_ROLES[profile.role]
      if (staffRoute) {
        router.push({ name: staffRoute.cockpit })
      } else {
        window.location.href = '/app'
        return
      }
    } else {
      router.push({ name: 'dashboard' })
    }
  } catch (e) {
    error.value = e.message || 'Login failed'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page { min-height: 100vh; display: flex; }
.login-left { flex: 1; background: linear-gradient(135deg, var(--gray-900) 0%, #1a2744 50%, var(--gray-900) 100%); display: flex; align-items: center; justify-content: center; padding: var(--space-10); position: relative; overflow: hidden; }
.login-left::before { content: ''; position: absolute; top: -50%; left: -50%; width: 200%; height: 200%; background: radial-gradient(circle at 30% 50%, rgba(30,64,175,0.15) 0%, transparent 50%); }
.login-brand-panel { position: relative; z-index: 1; color: white; max-width: 400px; }
.brand-mark-lg { width: 64px; height: 64px; border-radius: var(--radius-lg); background: var(--color-primary); display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: var(--text-xl); color: white; margin-bottom: var(--space-6); }
.login-brand-panel h1 { font-size: var(--text-3xl); font-weight: 700; line-height: 1.2; margin-bottom: var(--space-3); }
.login-brand-panel > p { font-size: var(--text-md); color: var(--gray-400); margin-bottom: var(--space-8); }
.brand-features { display: flex; flex-direction: column; gap: var(--space-3); }
.feature-item { display: flex; align-items: center; gap: var(--space-3); font-size: var(--text-sm); color: var(--gray-300); }
.feature-icon { width: 24px; height: 24px; border-radius: var(--radius-full); background: rgba(5,150,105,0.15); color: #34d399; display: flex; align-items: center; justify-content: center; font-size: 12px; flex-shrink: 0; }
.login-right { width: 480px; display: flex; align-items: center; justify-content: center; padding: var(--space-10); background: var(--color-surface); }
.login-card { width: 100%; max-width: 360px; }
.login-header { margin-bottom: var(--space-8); }
.brand-mark-sm { width: 44px; height: 44px; border-radius: var(--radius-md); background: var(--color-primary); display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: var(--text-sm); color: white; margin-bottom: var(--space-5); }
.login-header h2 { font-size: var(--text-2xl); font-weight: 700; color: var(--color-text); margin-bottom: var(--space-1); }
.login-header p { font-size: var(--text-sm); color: var(--color-text-secondary); }
.login-form { margin-bottom: var(--space-6); }
.login-btn { width: 100%; margin-top: var(--space-2); height: 44px; }
.login-alert { display: flex; align-items: center; gap: var(--space-2); padding: var(--space-3) var(--space-4); background: var(--color-danger-light); color: var(--color-danger-dark); border-radius: var(--radius-md); font-size: var(--text-sm); margin-bottom: var(--space-4); }
.alert-icon { flex-shrink: 0; }
.demo-section { margin-top: var(--space-2); }
.demo-divider { display: flex; align-items: center; gap: var(--space-3); margin-bottom: var(--space-4); }
.demo-divider::before, .demo-divider::after { content: ''; flex: 1; height: 1px; background: var(--color-border); }
.demo-divider span { font-size: 11px; font-weight: 500; color: var(--color-text-muted); text-transform: uppercase; letter-spacing: 0.05em; white-space: nowrap; }
.demo-grid { display: grid; grid-template-columns: 1fr 1fr; gap: var(--space-2); }
.demo-btn { display: flex; align-items: center; gap: var(--space-2-5); padding: var(--space-2-5) var(--space-3); border: 1px solid var(--color-border); border-radius: var(--radius-md); background: var(--color-surface); cursor: pointer; transition: all var(--transition-fast); text-align: left; }
.demo-btn:hover { border-color: var(--color-primary-light); background: var(--color-primary-50); }
.demo-avatar { width: 28px; height: 28px; border-radius: var(--radius-sm); display: flex; align-items: center; justify-content: center; font-size: 10px; font-weight: 700; color: white; flex-shrink: 0; }
.demo-text { overflow: hidden; }
.demo-role { display: block; font-size: 11px; font-weight: 600; color: var(--color-text); }
.demo-email { display: block; font-size: 10px; color: var(--color-text-muted); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
@media (max-width: 768px) {
  .login-page { flex-direction: column; }
  .login-left { padding: var(--space-8) var(--space-6); min-height: auto; }
  .login-brand-panel h1 { font-size: var(--text-2xl); }
  .brand-features { display: none; }
  .login-right { width: 100%; padding: var(--space-6); }
  .demo-grid { grid-template-columns: 1fr; }
}
</style>
