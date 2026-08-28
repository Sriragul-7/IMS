<template>
  <div class="dashboard">
    <div v-if="loading" class="loading-overlay">
      <div class="spinner spinner-lg"></div>
    </div>

    <template v-else>
      <div class="welcome-banner">
        <div>
          <h2>Welcome, {{ user?.user_name }}!</h2>
          <p>{{ greeting }}</p>
        </div>
      </div>

      <div class="stats-grid" v-if="stats">
        <StatCard :value="stats.attendance_pct + '%'" label="ATTENDANCE" color="#059669" icon="&#9776;" />
        <StatCard :value="stats.fees_count" label="FEE RECORDS" color="#1e40af" icon="&#9830;" />
        <StatCard :value="formatCurrency(stats.outstanding)" label="OUTSTANDING" color="#d97706" icon="&#9888;" />
        <StatCard :value="stats.active_books" label="LIBRARY BOOKS" color="#7c3aed" icon="&#9734;" />
      </div>

      <div class="dash-grid">
        <div class="card">
          <div class="card-header">
            <h3>Recent Notices</h3>
            <router-link to="/notices" class="btn btn-ghost btn-sm">View All</router-link>
          </div>
          <div class="card-body" v-if="notices.length">
            <div v-for="n in notices.slice(0, 5)" :key="n.name" class="notice-row">
              <div class="notice-dot"></div>
              <div class="notice-content">
                <span class="notice-title">{{ n.title }}</span>
                <span class="notice-date">{{ formatDate(n.publish_date) }}</span>
              </div>
            </div>
          </div>
          <div class="card-body" v-else>
            <EmptyState title="No notices" description="No recent notices to display" icon="&#9998;" />
          </div>
        </div>

        <div class="card">
          <div class="card-header">
            <h3>Fee Overview</h3>
            <router-link to="/fees" class="btn btn-ghost btn-sm">View All</router-link>
          </div>
          <div class="card-body" v-if="recentFees.length">
            <div v-for="f in recentFees.slice(0, 5)" :key="f.name" class="fee-row">
              <div class="fee-info">
                <span class="fee-name">{{ f.fee_schedule || f.name }}</span>
                <span class="fee-program">{{ f.academic_year }}</span>
              </div>
              <div class="fee-right">
                <span class="fee-amount">{{ formatCurrency(f.total_amount) }}</span>
                <StatusBadge :text="f.status" :variant="feeStatusVariant(f.status)" />
              </div>
            </div>
          </div>
          <div class="card-body" v-else>
            <EmptyState title="No fees" description="No fee records yet" icon="&#9830;" />
          </div>
        </div>

        <div class="card attendance-card">
          <div class="card-header">
            <h3>Attendance</h3>
            <router-link to="/attendance" class="btn btn-ghost btn-sm">Details</router-link>
          </div>
          <div class="card-body" v-if="attendance">
            <div class="att-overview">
              <div class="att-ring">
                <svg viewBox="0 0 36 36" class="circular-chart">
                  <path class="circle-bg" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
                  <path class="circle" :stroke-dasharray="`${attendance.percentage}, 100`" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
                  <text x="18" y="20.35" class="percentage">{{ attendance.percentage }}%</text>
                </svg>
              </div>
              <div class="att-breakdown">
                <div class="att-stat-row">
                  <span class="att-dot" style="background:#059669"></span>
                  <span>Present</span>
                  <strong>{{ attendance.summary.Present }}</strong>
                </div>
                <div class="att-stat-row">
                  <span class="att-dot" style="background:#dc2626"></span>
                  <span>Absent</span>
                  <strong>{{ attendance.summary.Absent }}</strong>
                </div>
                <div class="att-stat-row">
                  <span class="att-dot" style="background:#d97706"></span>
                  <span>Late</span>
                  <strong>{{ attendance.summary.Late }}</strong>
                </div>
              </div>
            </div>
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

const user = ref(null)
const stats = ref(null)
const notices = ref([])
const recentFees = ref([])
const attendance = ref(null)
const loading = ref(true)

const greeting = computed(() => {
  const h = new Date().getHours()
  if (h < 12) return 'Good morning! Here\'s your overview for today.'
  if (h < 17) return 'Good afternoon! Here\'s your overview for today.'
  return 'Good evening! Here\'s your overview for today.'
})

function formatDate(d) {
  return d ? new Date(d).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }) : ''
}

function formatCurrency(v) {
  return '\u20b9' + Number(v || 0).toLocaleString('en-IN', { minimumFractionDigits: 0 })
}

function feeStatusVariant(status) {
  const map = { Paid: 'success', Partial: 'warning', Unpaid: 'danger', Overdue: 'danger' }
  return map[status] || 'neutral'
}

onMounted(async () => {
  user.value = getSessionUser()
  if (!user.value) return

  try {
    const [att, fees, lib] = await Promise.all([
      callAPI('portal_get_attendance', { student: user.value.record_name }),
      callAPI('portal_get_fees', { student: user.value.record_name }),
      callAPI('portal_get_library', { student: user.value.record_name }),
    ])
    attendance.value = att
    recentFees.value = fees.fees || []
    notices.value = (await callAPI('portal_get_notices')).notices || []
    stats.value = {
      attendance_pct: att.percentage,
      fees_count: fees.fees?.length || 0,
      outstanding: fees.fees?.reduce((s, f) => s + (f.outstanding_amount || 0), 0) || 0,
      active_books: lib.active_items?.length || 0,
    }
  } catch (e) {
    console.error('Dashboard load error:', e)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.welcome-banner {
  background: linear-gradient(135deg, var(--color-primary) 0%, #2563eb 100%);
  color: white;
  padding: var(--space-6) var(--space-8);
  border-radius: var(--radius-xl);
  margin-bottom: var(--space-6);
}
.welcome-banner h2 { font-size: var(--text-2xl); font-weight: 700; margin-bottom: var(--space-1); }
.welcome-banner p { font-size: var(--text-sm); opacity: 0.85; }

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--space-4);
  margin-bottom: var(--space-6);
}

.dash-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-4);
}

/* ── Notice Rows ── */
.notice-row {
  display: flex;
  align-items: flex-start;
  gap: var(--space-3);
  padding: var(--space-3) 0;
  border-bottom: 1px solid var(--color-border-light);
}
.notice-row:last-child { border-bottom: none; }
.notice-dot {
  width: 8px; height: 8px;
  border-radius: 50%;
  background: var(--color-primary-light);
  flex-shrink: 0;
  margin-top: 5px;
}
.notice-content { flex: 1; min-width: 0; }
.notice-title { display: block; font-size: var(--text-sm); font-weight: 500; color: var(--color-text); }
.notice-date { font-size: var(--text-xs); color: var(--color-text-muted); }

/* ── Fee Rows ── */
.fee-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-3) 0;
  border-bottom: 1px solid var(--color-border-light);
}
.fee-row:last-child { border-bottom: none; }
.fee-info { flex: 1; min-width: 0; }
.fee-name { display: block; font-size: var(--text-sm); font-weight: 500; }
.fee-program { font-size: var(--text-xs); color: var(--color-text-muted); }
.fee-right { display: flex; align-items: center; gap: var(--space-3); }
.fee-amount { font-size: var(--text-sm); font-weight: 600; white-space: nowrap; }

/* ── Attendance Card ── */
.att-overview { display: flex; align-items: center; gap: var(--space-6); }
.att-ring { width: 90px; flex-shrink: 0; }
.circular-chart { width: 100%; }
.circle-bg { fill: none; stroke: var(--gray-200); stroke-width: 3; }
.circle { fill: none; stroke: var(--color-success); stroke-width: 3; stroke-linecap: round; }
.percentage { fill: var(--color-success); font-size: 0.5em; font-weight: 700; text-anchor: middle; }
.att-breakdown { flex: 1; }
.att-stat-row {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-1-5) 0;
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
}
.att-stat-row strong { margin-left: auto; color: var(--color-text); }
.att-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }

@media (max-width: 1024px) {
  .stats-grid { grid-template-columns: repeat(2, 1fr); }
  .dash-grid { grid-template-columns: 1fr; }
}
@media (max-width: 640px) {
  .stats-grid { grid-template-columns: 1fr; }
  .welcome-banner { padding: var(--space-5); }
  .welcome-banner h2 { font-size: var(--text-xl); }
}
</style>
