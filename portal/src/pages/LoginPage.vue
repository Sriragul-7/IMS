<template>
  <div class="login-page">
    <!-- Left Panel - Branded -->
    <div class="login-left">
      <div class="login-brand-panel">
        <!-- BIT Logo - Text based, no SVG dependency -->
        <div class="brand-mark-lg" aria-label="BIT Logo">
          BIT
        </div>

        <h1 class="brand-title">
          <span class="brand-title-line">Bannari Amman</span>
          <span class="brand-title-line">Institute of Technology</span>
        </h1>
        <p class="brand-tagline">Empowering Excellence in Engineering &amp; Technology</p>

        <!-- Feature Highlights -->
        <div class="brand-features">
          <div class="feature-item" v-for="(feature, i) in features" :key="i" :style="{ animationDelay: (i * 0.1) + 's' }">
            <div class="feature-icon">{{ feature.icon }}</div>
            <div class="feature-content">
              <span class="feature-title">{{ feature.title }}</span>
              <span class="feature-desc">{{ feature.desc }}</span>
            </div>
          </div>
        </div>

        <!-- Footer -->
        <div class="brand-footer">
          <span class="brand-motto">Excellence in Education Since 1996</span>
          <span class="brand-location">Sathyamangalam, Tamil Nadu</span>
        </div>
      </div>

      <!-- Background Shapes -->
      <div class="login-bg-shapes" aria-hidden="true">
        <div class="bg-shape bg-shape--1"></div>
        <div class="bg-shape bg-shape--2"></div>
        <div class="bg-shape bg-shape--3"></div>
        <div class="bg-shape bg-shape--4"></div>
        <div class="bg-shape bg-shape--5"></div>
      </div>
    </div>

    <!-- Right Panel - Login Form -->
    <div class="login-right">
      <div class="login-card">
        <!-- Logo & Header -->
        <div class="login-header">
          <div class="brand-mark-sm" aria-label="BIT Logo">
            BIT
          </div>
          <h2>Welcome back</h2>
          <p>Sign in to your portal account</p>
        </div>

        <!-- Login Form -->
        <form @submit.prevent="handleLogin" class="login-form">
          <div v-if="error" class="login-alert" role="alert">
            {{ error }}
          </div>

          <div class="form-group">
            <label class="form-label" for="email">Email address</label>
            <input id="email" v-model="email" type="email" class="form-input" placeholder="you@institution.local" required autofocus autocomplete="email" />
          </div>

          <div class="form-group">
            <label class="form-label" for="password">Password</label>
            <div class="password-wrapper">
              <input id="password" v-model="password" :type="showPassword ? 'text' : 'password'" class="form-input" placeholder="Enter your password" required autocomplete="current-password" />
              <button type="button" class="password-toggle" @click="showPassword = !showPassword" :aria-label="showPassword ? 'Hide password' : 'Show password'">
                {{ showPassword ? 'Show' : 'Hide' }}
              </button>
            </div>
          </div>

          <button type="submit" class="btn btn-primary btn-lg btn-block login-btn" :disabled="loading">
            <span v-if="loading" class="btn-spinner">
              <svg class="spinner" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round">
                <circle cx="12" cy="12" r="10" stroke-opacity="0.25"></circle>
                <path d="M12 2a10 10 0 0 1 10 10" stroke-opacity="1"></path>
              </svg>
            </span>
            <span>{{ loading ? 'Signing in...' : 'Sign In' }}</span>
          </button>
        </form>

        <!-- Demo Access Cards -->
        <div class="demo-section">
          <div class="demo-divider"><span>Quick Demo Access</span></div>
          <p class="demo-hint">Click a role card to auto-fill credentials</p>
          <div class="demo-grid" role="list" aria-label="Demo accounts">
            <button v-for="(d, i) in demoRoles" :key="i" class="demo-card" @click="fillDemo(d)" role="listitem" :aria-label="`Login as ${d.role} (${d.email})`">
              <div class="demo-card-icon" :style="{ background: d.gradient }">
                {{ d.icon }}
              </div>
              <div class="demo-card-content">
                <span class="demo-card-role">{{ d.role }}</span>
                <span class="demo-card-email">{{ d.email }}</span>
              </div>
              <div class="demo-card-arrow" aria-hidden="true">
                &#8594;
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
const showPassword = ref(false)

const features = [
  { title: 'Student Portal', desc: 'Attendance, Results, Fees, Library &amp; More', icon: 'S', color: '#2563eb' },
  { title: 'Staff Cockpits', desc: 'Role-specific dashboards for all staff roles', icon: 'S', color: '#059669' },
  { title: 'Real-time Data', desc: 'Live attendance, marks, and fee tracking', icon: 'S', color: '#d97706' },
  { title: 'Guardian Access', desc: 'Multi-child monitoring with child switcher', icon: 'S', color: '#7c3aed' },
  { title: 'Communication', desc: 'Notices, announcements &amp; feedback system', icon: 'S', color: '#ec4899' },
  { title: 'Facilities', desc: 'Library, Hostel &amp; Transport management', icon: 'S', color: '#0d9488' }
]

const demoRoles = [
  { email: 'richdemo@demo.institution.local', role: 'Student (Rich Demo)', description: 'Full data: attendance, results, fees, library', icon: 'S', gradient: 'linear-gradient(135deg, #2563eb, #1d4ed8)' },
  { email: 'student1@demo.institution.local', role: 'Student', description: 'B.E. Computer Science • Minimal demo data', icon: 'S', gradient: 'linear-gradient(135deg, #2563eb, #3b82f6)' },
  { email: 'guardian1@demo.institution.local', role: 'Guardian (2 Children)', description: 'Multi-child switcher demo', icon: 'S', gradient: 'linear-gradient(135deg, #7c3aed, #a855f7)' },
  { email: 'guardian2@demo.institution.local', role: 'Guardian (3 Children)', description: 'Larger family switching demo', icon: 'S', gradient: 'linear-gradient(135deg, #6366f1, #818cf8)' },
  { email: 'instructor1@demo.institution.local', role: 'Instructor', description: "Today's classes, pending marks", icon: 'S', gradient: 'linear-gradient(135deg, #059669, #10b981)' },
  { email: 'feemanager@demo.institution.local', role: 'Fee Manager', description: 'Outstanding fees, payments, discounts', icon: 'S', gradient: 'linear-gradient(135deg, #d97706, #f59e0b)' },
  { email: 'facilitymanager@demo.institution.local', role: 'Facility Manager', description: 'Library issues, hostel, transport', icon: 'S', gradient: 'linear-gradient(135deg, #0d9488, #14b8a6)' },
  { email: 'comms.officer@demo.institution.local', role: 'Communication Officer', description: 'Notices, feedback queue', icon: 'S', gradient: 'linear-gradient(135deg, #ec4899, #f472b6)' },
  { email: 'admissions@demo.institution.local', role: 'Admissions Officer', description: 'Inquiry pipeline, applicant review', icon: 'S', gradient: 'linear-gradient(135deg, #d97706, #b45309)' },
  { email: 'academichead@demo.institution.local', role: 'Academic Head', description: 'Programs, attendance, exam performance', icon: 'S', gradient: 'linear-gradient(135deg, #d97706, #b45309)' },
  { email: 'admin@demo.institution.local', role: 'System Manager', description: 'Mission control • Institution overview', icon: 'S', gradient: 'linear-gradient(135deg, #7c3aed, #6d28d9)' }
]

function fillDemo(d) {
  email.value = d.email
  password.value = 'Demo@2026'
  error.value = ''
}

const STAFF_ROUTES = {
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
      const staffRoute = STAFF_ROUTES[profile.role]
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
.login-page {
  min-height: 100vh;
  display: flex;
  background: var(--color-surface);
}

.login-left {
  flex: 1;
  background: var(--gradient-hero);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-8);
  position: relative;
  overflow: hidden;
  min-height: 700px;
}

.login-brand-panel {
  position: relative;
  z-index: 1;
  color: white;
  max-width: 560px;
  width: 100%;
  animation: slideUp 0.8s ease;
}

.brand-mark-lg {
  width: 64px;
  height: 64px;
  border-radius: var(--radius-xl);
  background: rgba(255,255,255,0.15);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 28px;
  font-weight: var(--font-weight-bold);
  margin-bottom: var(--space-6);
  box-shadow: 0 10px 25px -5px rgba(14, 184, 166, 0.2);
  border: 1px solid rgba(255,255,255,0.2);
  animation: scaleIn 0.6s var(--transition-bounce) 0.1s both;
}

.brand-title {
  display: flex;
  flex-direction: column;
  font-size: var(--text-3xl);
  font-weight: var(--font-weight-bold);
  line-height: var(--leading-tight);
  letter-spacing: -0.025em;
  margin-bottom: var(--space-3);
  animation: slideUp 0.8s ease 0.2s both;
}
.brand-title-line { display: block; }

.brand-tagline {
  font-size: var(--text-lg);
  color: rgba(255,255,255,0.85);
  margin-bottom: var(--space-8);
  font-weight: var(--font-weight-medium);
  animation: slideUp 0.8s ease 0.3s both;
}

.brand-features {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
  margin-bottom: var(--space-8);
}

.feature-item {
  display: flex;
  align-items: flex-start;
  gap: var(--space-3);
  padding: var(--space-3) var(--space-4);
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: var(--radius-lg);
  backdrop-filter: blur(8px);
  transition: all var(--transition-base);
  animation: slideUp 0.6s ease both;
}

.feature-item:hover {
  background: rgba(255,255,255,0.1);
  border-color: rgba(14, 184, 166, 0.3);
  transform: translateX(4px);
}

.feature-icon {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  line-height: 1;
  flex-shrink: 0;
}

.feature-content { flex: 1; min-width: 0; }
.feature-title {
  display: block;
  font-size: var(--text-sm);
  font-weight: var(--font-weight-semibold);
  color: white;
  margin-bottom: 2px;
}
.feature-desc {
  display: block;
  font-size: 11px;
  color: var(--gray-300);
}

.brand-footer {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
  padding-top: var(--space-4);
  border-top: 1px solid rgba(255,255,255,0.1);
}
.brand-motto { font-size: var(--text-sm); color: var(--gray-300); font-weight: var(--font-weight-medium); }
.brand-location { font-size: var(--text-xs); color: var(--gray-400); }

.login-bg-shapes { position: absolute; inset: 0; pointer-events: none; overflow: hidden; }
.bg-shape { position: absolute; border-radius: 50%; background: rgba(255,255,255,0.03); animation: float 20s ease-in-out infinite; }
.bg-shape--1 { width: 300px; height: 300px; top: -80px; right: -80px; animation-delay: 0s; }
.bg-shape--2 { width: 200px; height: 200px; bottom: -50px; left: -50px; animation-delay: -5s; }
.bg-shape--3 { width: 150px; height: 150px; top: 20%; right: 10%; animation-delay: -10s; }
.bg-shape--4 { width: 100px; height: 100px; bottom: 30%; left: 15%; animation-delay: -15s; }
.bg-shape--5 { width: 80px; height: 80px; top: 50%; right: 30%; animation-delay: -7s; }

.login-right {
  width: 480px;
  max-width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-10);
  background: var(--color-surface);
  border-left: 1px solid var(--color-border-light);
  min-height: 700px;
}

.login-card {
  width: 100%;
  max-width: 400px;
  animation: fadeIn 0.8s ease 0.2s both;
}

.login-header {
  text-align: center;
  margin-bottom: var(--space-8);
}

.brand-mark-sm {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-lg);
  background: var(--color-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  margin: 0 auto var(--space-5);
  box-shadow: 0 4px 6px -1px rgba(15, 23, 42, 0.2);
  border: 1px solid rgba(255,255,255,0.2);
  font-size: 20px;
  font-weight: var(--font-weight-bold);
}

.login-header h2 {
  font-size: var(--text-2xl);
  font-weight: var(--font-weight-bold);
  color: var(--color-text);
  margin-bottom: var(--space-1);
}
.login-header p {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
}

.login-form { margin-bottom: var(--space-6); }
.login-btn { height: 48px; margin-top: var(--space-2); }
.btn-spinner { display: inline-flex; }
.spinner { animation: spin 0.8s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

.password-wrapper { position: relative; }
.password-toggle {
  position: absolute;
  right: var(--space-3);
  top: 50%;
  transform: translateY(-50%);
  width: 36px;
  height: 36px;
  border-radius: var(--radius-md);
  border: none;
  background: transparent;
  color: var(--color-text-muted);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--transition-fast);
  font-size: 18px;
}
.password-toggle:hover { background: var(--gray-100); color: var(--color-text); }

.login-alert {
  display: flex;
  align-items: flex-start;
  gap: var(--space-2);
  padding: var(--space-3) var(--space-4);
  background: var(--color-danger-light);
  color: var(--color-danger-dark);
  border-radius: var(--radius-md);
  font-size: var(--text-sm);
  margin-bottom: var(--space-4);
  border: 1px solid var(--color-danger-light);
  animation: shake 0.4s ease;
}
@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-4px); }
  75% { transform: translateX(4px); }
}

.demo-section { margin-top: var(--space-2); }
.demo-divider {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  margin-bottom: var(--space-3);
}
.demo-divider::before, .demo-divider::after { content: ''; flex: 1; height: 1px; background: var(--color-border); }
.demo-divider span {
  font-size: 11px;
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  white-space: nowrap;
}
.demo-hint { font-size: var(--text-xs); color: var(--color-text-muted); text-align: center; margin-bottom: var(--space-4); }

.demo-grid { display: grid; grid-template-columns: 1fr 1fr; gap: var(--space-2); }
.demo-card {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3) var(--space-4);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  background: var(--color-surface);
  cursor: pointer;
  transition: all var(--transition-fast);
  text-align: left;
  position: relative;
  overflow: hidden;
}
.demo-card::before { content: ''; position: absolute; left: 0; top: 0; bottom: 0; width: 3px; background: var(--color-primary); opacity: 0; transition: opacity var(--transition-fast); }
.demo-card:hover { border-color: var(--color-accent-light); background: var(--color-accent-50); transform: translateY(-1px); box-shadow: var(--shadow-md); }
.demo-card:hover::before { opacity: 1; }
.demo-card-icon {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.125rem;
  line-height: 1;
  flex-shrink: 0;
  color: white;
}
.demo-card-content { flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 2px; }
.demo-card-role {
  font-size: var(--text-sm);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.demo-card-email {
  font-size: 10px;
  color: var(--color-text-muted);
  font-family: var(--font-family-mono);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.demo-card-arrow { color: var(--color-text-muted); transition: transform var(--transition-fast); }
.demo-card:hover .demo-card-arrow { transform: translateX(4px); color: var(--color-accent); }

@media (max-width: 1024px) {
  .login-left { padding: var(--space-8) var(--space-6); min-height: auto; }
  .brand-title { font-size: var(--text-3xl); }
  .login-right { padding: var(--space-8) var(--space-6); }
  .demo-grid { grid-template-columns: 1fr; }
}
@media (max-width: 768px) {
  .login-page { flex-direction: column; }
  .login-left { min-height: 350px; padding: var(--space-8); }
  .brand-title { font-size: var(--text-2xl); }
  .login-right { width: 100%; padding: var(--space-6); }
  .demo-grid { grid-template-columns: 1fr; }
}
@media (max-width: 480px) {
  .login-left { padding: var(--space-6) var(--space-4); }
  .brand-title { font-size: var(--text-xl); }
  .brand-tagline { font-size: var(--text-md); }
  .login-right { padding: var(--space-4); }
  .login-card { max-width: 100%; }
}
</style>