<template>
  <div class="dashboard-page">
    <div v-if="loading" class="page-loading">
      <div class="skeleton skeleton--heading" style="width: 40%;"></div>
      <div class="skeleton skeleton--text" style="width: 60%; margin-top: var(--space-2);"></div>
      <div class="stats-grid" style="margin-top: var(--space-6);">
        <Skeleton type="stat" v-for="i in 4" :key="i" />
      </div>
      <div class="dash-grid" style="margin-top: var(--space-6);">
        <Skeleton type="card" v-for="i in 3" :key="i" />
      </div>
    </div>

    <template v-else>
      <!-- Hero Banner - Dark Blue -->
      <div class="hero-banner dashboard-hero" :style="{ background: roleGradient }">
        <div class="hero-content">
          <div class="hero-badge" :style="{ background: roleBadgeBg, color: roleBadgeText }">
            {{ roleBadge }}
          </div>
          <h1 class="hero-title">Welcome back, {{ userName }}</h1>
          <p class="hero-subtitle">{{ programInfo }} · {{ academicInfo }}</p>
          <div class="hero-notification" @click="toggleNotifications" :class="{ 'has-notice': notices.length > 0 }">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path>
              <path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
            </svg>
            <span v-if="notices.length > 0" class="notice-count">{{ notices.length }}</span>
          </div>
        </div>
      </div>

      <!-- Stat Cards - 4 cards -->
      <div class="stats-grid" v-if="stats">
        <StatCard
          :value="stats.attendance_pct"
          label="Attendance"
          format="percent"
          :color="roleColor"
          icon="ATT"
          variant="primary"
        />
        <StatCard
          :value="stats.cgpa"
          label="Current CGPA"
          format="number"
          :color="roleColor"
          icon="GPA"
          variant="primary"
        />
        <StatCard
          :value="stats.outstanding"
          label="Fees outstanding"
          format="currency"
          :color="'#d97706'"
          icon="&#8377;"
          variant="primary"
        />
        <StatCard
          :value="stats.active_books"
          label="Books issued"
          format="number"
          :color="'#7c3aed'"
          icon="BK"
          variant="primary"
        />
      </div>

      <!-- Main Grid - 3 columns -->
      <div class="dash-grid">
        <!-- Latest notices -->
        <div class="card card-hover">
          <div class="card-header">
            <h3>Latest notices</h3>
            <router-link to="/notices" class="btn btn-ghost btn-sm">View all</router-link>
          </div>
          <div class="card-body" v-if="notices.length">
            <div class="notice-list">
              <div v-for="n in notices.slice(0, 5)" :key="n.name" class="notice-item">
                <div class="notice-date" :style="{ color: roleColor }">{{ formatNoticeDate(n.publish_date) }}</div>
                <div class="notice-content">
                  <span class="notice-title">{{ n.title }}</span>
                  <span class="notice-source">{{ n.audience_type || 'General' }}</span>
                </div>
              </div>
            </div>
          </div>
          <div class="card-body" v-else>
            <EmptyState title="No notices" description="No recent notices to display" icon="NT" size="sm" />
          </div>
        </div>

        <!-- Fee summary -->
        <div class="card card-hover">
          <div class="card-header">
            <h3>Fee summary</h3>
            <router-link to="/fees" class="btn btn-ghost btn-sm">View all</router-link>
          </div>
          <div class="card-body" v-if="feeSummary.length">
            <div class="fee-summary-list">
              <div v-for="f in feeSummary" :key="f.category" class="fee-summary-item">
                <span class="fee-category">{{ f.category }}</span>
                <StatusBadge :text="f.status" :variant="feeStatusVariant(f.status)" size="sm" class="fee-status" />
              </div>
            </div>
            <div class="fee-total">
              <span class="fee-total-label">Total outstanding</span>
              <span class="fee-total-value">{{ formatCurrency(totalOutstanding) }}</span>
            </div>
          </div>
          <div class="card-body" v-else>
            <EmptyState title="No fees" description="No fee records found" icon="FE" size="sm" />
          </div>
        </div>

        <!-- Attendance donut -->
        <div class="card card-hover">
          <div class="card-header">
            <h3>Attendance</h3>
          </div>
          <div class="card-body" v-if="attendance">
            <div class="attendance-donut-wrapper">
              <ProgressRing
                :value="attendance.percentage"
                :size="140"
                :stroke-width="10"
                stroke-color="#059669"
                label="Attendance"
                unit="%"
              />
              <div class="attendance-stats">
                <div class="att-stat">
                  <span class="att-value">{{ attendance.summary?.Present || 0 }}</span>
                  <span class="att-label">Present</span>
                </div>
                <div class="att-stat">
                  <span class="att-value">{{ attendance.summary?.Absent || 0 }}</span>
                  <span class="att-label">Absent</span>
                </div>
                <div class="att-stat">
                  <span class="att-value">{{ attendance.summary?.Late || 0 }}</span>
                  <span class="att-label">Late</span>
                </div>
                <div class="att-stat">
                  <span class="att-value">{{ attendance.summary?.Excused || 0 }}</span>
                  <span class="att-label">Excused</span>
                </div>
              </div>
            </div>
            <div class="attendance-breakdown" style="margin-top: var(--space-4);">
              <div class="att-row">
                <span class="att-dot" style="background:#059669"></span>
                <span class="att-text">Present</span>
                <span class="att-count">{{ attendance.summary?.Present || 0 }} classes</span>
              </div>
              <div class="att-row">
                <span class="att-dot" style="background:#dc2626"></span>
                <span class="att-text">Absent</span>
                <span class="att-count">{{ attendance.summary?.Absent || 0 }} classes</span>
              </div>
              <div class="att-row">
                <span class="att-dot" style="background:#d97706"></span>
                <span class="att-text">Late</span>
                <span class="att-count">{{ attendance.summary?.Late || 0 }} classes</span>
              </div>
              <div class="att-row">
                <span class="att-dot" style="background:#7c3aed"></span>
                <span class="att-text">Excused</span>
                <span class="att-count">{{ attendance.summary?.Excused || 0 }} classes</span>
              </div>
            </div>
          </div>
          <div class="card-body" v-else>
            <EmptyState title="Loading attendance..." description="Please wait" icon="⏳" size="sm" />
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getSessionUser, callAPI } from '../utils/api.js'
import StatCard from '../components/StatCard.vue'
import StatusBadge from '../components/StatusBadge.vue'
import EmptyState from '../components/EmptyState.vue'
import ProgressRing from '../components/ProgressRing.vue'
import Skeleton from '../components/Skeleton.vue'

const user = ref(null)
const stats = ref(null)
const attendance = ref(null)
const notices = ref([])
const loading = ref(true)

const userName = computed(() => user.value?.user_name || 'User')
const programInfo = computed(() => user.value?.program || 'Program')
const academicInfo = computed(() => user.value?.academic_year || 'Academic Year')

const roleColor = computed(() => {
  const r = user.value?.role
  const map = {
    'Student': '#2563eb',
    'Guardian': '#2563eb',
    'Instructor': '#059669',
    'Fee Manager': '#059669',
    'Facility Manager': '#059669',
    'Communication Officer': '#059669',
    'System Manager': '#7c3aed',
    'Admissions Officer': '#d97706',
    'Academic Head': '#d97706',
  }
  return map[r] || '#2563eb'
})

const roleGradient = computed(() => {
  const r = user.value?.role
  const map = {
    'Student': 'linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%)',
    'Guardian': 'linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%)',
    'Instructor': 'linear-gradient(135deg, #059669 0%, #047857 100%)',
    'Fee Manager': 'linear-gradient(135deg, #059669 0%, #047857 100%)',
    'Facility Manager': 'linear-gradient(135deg, #059669 0%, #047857 100%)',
    'Communication Officer': 'linear-gradient(135deg, #059669 0%, #047857 100%)',
    'System Manager': 'linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%)',
    'Admissions Officer': 'linear-gradient(135deg, #d97706 0%, #b45309 100%)',
    'Academic Head': 'linear-gradient(135deg, #d97706 0%, #b45309 100%)',
  }
  return map[r] || 'linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%)'
})

const roleBadgeBg = computed(() => {
  const c = roleColor.value
  const lightMap = {
    '#2563eb': 'rgba(37, 99, 235, 0.15)',
    '#059669': 'rgba(5, 150, 105, 0.15)',
    '#7c3aed': 'rgba(124, 58, 237, 0.15)',
    '#d97706': 'rgba(217, 119, 6, 0.15)',
  }
  return lightMap[c] || 'rgba(37, 99, 235, 0.15)'
})

const roleBadgeText = computed(() => {
  const c = roleColor.value
  const textMap = {
    '#2563eb': '#2563eb',
    '#059669': '#059669',
    '#7c3aed': '#7c3aed',
    '#d97706': '#d97706',
  }
  return textMap[c] || '#2563eb'
})

const roleBadge = computed(() => {
  const r = user.value?.role
  const map = {
    'Student': 'Student Portal',
    'Guardian': 'Guardian Portal',
    'Instructor': 'Staff Cockpit',
    'Fee Manager': 'Staff Cockpit',
    'Facility Manager': 'Staff Cockpit',
    'Communication Officer': 'Staff Cockpit',
    'System Manager': 'Admin Cockpit',
    'Admissions Officer': 'Staff Cockpit',
    'Academic Head': 'Staff Cockpit',
  }
  return map[r] || 'Student Portal'
})

const totalOutstanding = computed(() => {
  if (!stats.value) return 0
  return stats.value.outstanding || 0
})

function formatCurrency(v) {
  return '₹' + Number(v || 0).toLocaleString('en-IN', { minimumFractionDigits: 0 })
}

function formatNoticeDate(d) {
  if (!d) return ''
  const date = new Date(d)
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }).toUpperCase()
}

function feeStatusVariant(status) {
  const map = { Paid: 'success', Partial: 'warning', Unpaid: 'danger', Overdue: 'danger' }
  return map[status] || 'neutral'
}

const feeSummary = computed(() => {
  if (!stats.value) return []
  return (recentFees.value || []).map(f => ({
    category: f.fee_schedule || f.name,
    status: f.status || 'Unpaid',
  }))
})

const recentFees = ref([])
const libActiveItems = ref([])

onMounted(async () => {
  user.value = getSessionUser()
  if (!user.value) return

  try {
    const [att, fees, notif] = await Promise.all([
      callAPI('portal_get_attendance', { student: user.value.record_name }),
      callAPI('portal_get_fees', { student: user.value.record_name }),
      callAPI('portal_get_notices'),
    ])

    attendance.value = att
    recentFees.value = fees.fees || []
    notices.value = notif.notices || []

    const totalFees = fees.fees?.reduce((s, f) => s + (f.total_amount || 0), 0) || 0
    const totalPaid = fees.fees?.reduce((s, f) => s + (f.paid_amount || 0), 0) || 0
    const totalOutstandingVal = fees.fees?.reduce((s, f) => s + (f.outstanding_amount || 0), 0) || 0

    stats.value = {
      attendance_pct: att.percentage || 0,
      cgpa: 8.5,
      outstanding: totalOutstandingVal,
      active_books: libActiveItems.value?.length || 0,
    }
  } catch (e) {
    console.error('Dashboard load error:', e)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.dashboard-page { animation: fadeIn var(--transition-base); }

.page-loading { padding: var(--space-6); }

.dashboard-hero {
  padding: var(--space-8);
  color: white;
  position: relative;
  overflow: hidden;
}
.dashboard-hero::before {
  content: '';
  position: absolute;
  top: -50%;
  right: -50%;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle at center, rgba(255,255,255,0.08) 0%, transparent 70%);
  pointer-events: none;
}
.hero-content {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}
.hero-badge {
  display: inline-flex;
  align-items: center;
  padding: var(--space-1) var(--space-3);
  border-radius: var(--radius-full);
  font-size: var(--text-xs);
  font-weight: var(--font-weight-semibold);
  margin-bottom: var(--space-1);
}
.hero-title {
  font-size: var(--text-3xl);
  font-weight: var(--font-weight-bold);
  line-height: var(--leading-tight);
  margin: 0;
  letter-spacing: -0.02em;
}
.hero-subtitle {
  font-size: var(--text-sm);
  opacity: 0.85;
  margin: 0;
  display: flex;
  align-items: center;
  gap: var(--space-3);
}
.hero-subtitle::before {
  content: '•';
  color: rgba(255,255,255,0.4);
}
.hero-notification {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  cursor: pointer;
  padding: var(--space-2) var(--space-4);
  background: rgba(255,255,255,0.1);
  border-radius: var(--radius-lg);
  border: 1px solid rgba(255,255,255,0.15);
  transition: all var(--transition-fast);
  margin-left: auto;
}
.hero-notification:hover {
  background: rgba(255,255,255,0.2);
}
.hero-notification.has-notice {
  background: rgba(217, 119, 6, 0.15);
  border-color: rgba(217, 119, 6, 0.3);
}
.notice-count {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #f59e0b;
  color: white;
  font-size: var(--text-xs);
  font-weight: var(--font-weight-bold);
  display: flex;
  align-items: center;
  justify-content: center;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--space-4);
  margin: var(--space-6) 0;
}

.dash-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-4);
}

.notice-list { display: flex; flex-direction: column; gap: var(--space-3); }
.notice-item {
  display: flex;
  gap: var(--space-3);
  padding: var(--space-3);
  border-radius: var(--radius-md);
  border: 1px solid var(--color-border-light);
  transition: all var(--transition-fast);
}
.notice-item:hover { background: var(--gray-50); border-color: var(--color-border); }
.notice-date {
  font-size: var(--text-xs);
  font-weight: var(--font-weight-bold);
  white-space: nowrap;
  flex-shrink: 0;
  padding-top: 2px;
}
.notice-content { flex: 1; min-width: 0; }
.notice-title {
  font-size: var(--text-sm);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.notice-source {
  font-size: var(--text-xs);
  color: var(--color-text-muted);
}

.fee-summary-list { display: flex; flex-direction: column; gap: var(--space-3); }
.fee-summary-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-3);
  border-radius: var(--radius-md);
  border: 1px solid var(--color-border-light);
  background: var(--gray-50);
}
.fee-category {
  font-size: var(--text-sm);
  font-weight: var(--font-weight-medium);
  color: var(--color-text);
}
.fee-status { flex-shrink: 0; }
.fee-total {
  margin-top: var(--space-4);
  padding-top: var(--space-4);
  border-top: 1px solid var(--color-border-light);
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.fee-total-label {
  font-size: var(--text-sm);
  font-weight: var(--font-weight-medium);
  color: var(--color-text-secondary);
}
.fee-total-value {
  font-size: var(--text-lg);
  font-weight: var(--font-weight-bold);
  color: var(--color-text);
  font-variant-numeric: tabular-nums;
}

.attendance-donut-wrapper {
  display: flex;
  align-items: center;
  gap: var(--space-6);
  margin-bottom: var(--space-4);
}
.attendance-stats {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--space-3);
}
.att-stat {
  text-align: center;
  padding: var(--space-2);
  background: var(--gray-50);
  border-radius: var(--radius-md);
}
.att-value {
  display: block;
  font-size: var(--text-xl);
  font-weight: var(--font-weight-bold);
  color: var(--color-text);
}
.att-label {
  font-size: var(--text-xs);
  color: var(--color-text-muted);
}
.attendance-breakdown { display: flex; flex-direction: column; gap: var(--space-1); }
.att-row {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-size: var(--text-sm);
}
.att-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
.att-text { color: var(--color-text-secondary); flex: 1; }
.att-count { color: var(--color-text-muted); font-variant-numeric: tabular-nums; }

@media (max-width: 1024px) {
  .stats-grid { grid-template-columns: repeat(2, 1fr); }
  .dash-grid { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 768px) {
  .stats-grid { grid-template-columns: 1fr; }
  .dash-grid { grid-template-columns: 1fr; }
  .hero-title { font-size: var(--text-2xl); }
  .dashboard-hero { padding: var(--space-6); }
}
</style>