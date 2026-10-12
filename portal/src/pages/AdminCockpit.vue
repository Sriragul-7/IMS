<template>
  <div class="cockpit-page">
    <div v-if="loading" class="cockpit-loading">
      <div class="skeleton skeleton--heading" style="width: 30%;"></div>
      <div class="skeleton skeleton--text" style="width: 50%; margin-top: var(--space-2);"></div>
      <div class="stats-skeleton" style="margin-top: var(--space-6);">
        <Skeleton type="stat" v-for="i in 8" :key="i" />
      </div>
      <div class="dash-skeleton" style="margin-top: var(--space-6);">
        <Skeleton type="card" v-for="i in 3" :key="i" />
      </div>
    </div>

    <template v-else>
      <HeroBanner 
        title="Administration Mission Control"
        :subtitle="`${greeting} — Institution-wide overview for ${user?.user_name}`"
        :meta-items="heroMeta"
        illustration="campus"
        variant="dark"
      >
        <template #actions>
          <a href="/app" class="btn btn-glass" target="_blank">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
            Open Full Desk
          </a>
        </template>
      </HeroBanner>

      <div class="stats-grid stats-grid--8">
        <StatCard :value="stats.total_students" label="Active Students" color="#0f172a" icon="👥" variant="default" :trend="studentsTrend" trend-variant="positive" />
        <StatCard :value="stats.total_staff" label="Staff Members" color="#059669" icon="👨‍🏫" variant="success" />
        <StatCard :value="stats.avg_attendance" label="Avg Attendance" format="percent" color="#d97706" icon="📊" variant="amber" />
        <StatCard :value="stats.total_outstanding" label="Outstanding Fees" format="currency" color="#dc2626" icon="💰" variant="danger" :trend="outstandingTrend" trend-variant="negative" />
        <StatCard :value="stats.total_programs" label="Programs" color="#7c3aed" icon="🎓" variant="purple" />
        <StatCard :value="stats.total_courses" label="Courses" color="#2563eb" icon="📚" variant="info" />
        <StatCard :value="stats.open_feedback" label="Open Feedback" color="#d97706" icon="💬" variant="amber" />
        <StatCard :value="stats.library_active" label="Library Active" color="#059669" icon="📖" variant="success" />
      </div>

      <div class="dash-grid">
        <div class="card card-hover dash-card--wide">
          <div class="card-header">
            <h3>Module Quick Access</h3>
          </div>
          <div class="card-body">
            <div class="module-grid">
              <a v-for="module in modules" :key="module.key" :href="module.href" class="module-card" target="_blank">
                <div class="module-icon" :style="{ background: module.color + '15', color: module.color }">
                  <span v-html="module.icon"></span>
                </div>
                <span class="module-label">{{ module.label }}</span>
              </a>
            </div>
          </div>
        </div>

        <div class="card card-hover">
          <div class="card-header">
            <h3>Admissions Pipeline</h3>
            <a href="/app/student" class="btn btn-ghost btn-sm" target="_blank">View All</a>
          </div>
          <div class="card-body">
            <div class="pipeline-summary">
              <div class="pipeline-summary-item">
                <span class="pipeline-count">{{ pipeline.active }}</span>
                <span class="pipeline-label">Active</span>
              </div>
              <div class="pipeline-arrow">→</div>
              <div class="pipeline-summary-item">
                <span class="pipeline-count">{{ pipeline.inactive }}</span>
                <span class="pipeline-label">Inactive</span>
              </div>
            </div>
            <div class="pipeline-detail">
              <div class="pipeline-stage-mini" v-for="stage in pipelineStages" :key="stage.key">
                <span class="stage-dot" :style="{ background: stage.color }"></span>
                <span class="stage-name">{{ stage.label }}</span>
                <span class="stage-count-mini">{{ pipeline[stage.key] || 0 }}</span>
              </div>
            </div>
          </div>
        </div>

        <div class="card card-hover">
          <div class="card-header">
            <h3>System Health</h3>
          </div>
          <div class="card-body">
            <div class="health-grid">
              <div class="health-item" v-for="item in healthItems" :key="item.label">
                <div class="health-icon" :style="{ background: item.color + '15', color: item.color }">
                  <span v-html="item.icon"></span>
                </div>
                <div class="health-content">
                  <span class="health-label">{{ item.label }}</span>
                  <span class="health-value" :class="item.variant">{{ item.value }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="card card-hover dash-card--wide">
          <div class="card-header">
            <h3>Enrollment Trend (6 Months)</h3>
          </div>
          <div class="card-body">
            <ChartCard 
              type="bar"
              :chart-data="enrollmentChartData"
              :height="280"
              :loading="chartLoading"
            />
          </div>
        </div>

        <div class="card card-hover dash-card--wide">
          <div class="card-header">
            <h3>Fee Collection Health</h3>
          </div>
          <div class="card-body">
            <ChartCard 
              type="line"
              :chart-data="feeHealthChartData"
              :height="280"
              :loading="chartLoading"
            />
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
import HeroBanner from '../components/HeroBanner.vue'
import ChartCard from '../components/ChartCard.vue'
import Skeleton from '../components/Skeleton.vue'

const user = ref(null)
const stats = ref({
  total_students: 0, total_staff: 0, avg_attendance: 0, total_outstanding: 0,
  total_programs: 0, total_courses: 0, open_feedback: 0, library_active: 0,
})
const pipeline = ref({ active: 0, inactive: 0, open: 0, applied: 0, review: 0, approved: 0, rejected: 0 })
const loading = ref(true)
const chartLoading = ref(false)

const greeting = computed(() => {
  const h = new Date().getHours()
  if (h < 12) return 'Good morning'
  if (h < 17) return 'Good afternoon'
  return 'Good evening'
})

const heroMeta = computed(() => [
  { label: 'Role', value: 'System Manager', icon: '⚙️' }
])

const studentsTrend = '+45 this term'
const outstandingTrend = '-8% vs last month'

const modules = [
  { key: 'students', label: 'Students', icon: '👥', color: '#0f172a', href: '/app/student' },
  { key: 'instructors', label: 'Instructors', icon: '👨‍🏫', color: '#059669', href: '/app/instructor' },
  { key: 'fees', label: 'Fees', icon: '💰', color: '#d97706', href: '/app/fees' },
  { key: 'attendance', label: 'Attendance', icon: '📅', color: '#0d9488', href: '/app/student-attendance' },
  { key: 'assessments', label: 'Assessments', icon: '📝', color: '#7c3aed', href: '/app/assessment-plan' },
  { key: 'library', label: 'Library', icon: '📚', color: '#2563eb', href: '/app/library-transaction' },
  { key: 'notices', label: 'Notices', icon: '📢', color: '#ec4899', href: '/app/notice' },
  { key: 'hostel', label: 'Hostel', icon: '🏠', color: '#f59e0b', href: '/app/hostel' },
]

const pipelineStages = [
  { key: 'open', label: 'Open', color: '#6b7280' },
  { key: 'applied', label: 'Applied', color: '#d97706' },
  { key: 'review', label: 'Review', color: '#7c3aed' },
  { key: 'approved', label: 'Approved', color: '#059669' },
  { key: 'rejected', label: 'Rejected', color: '#dc2626' }
]

const healthItems = computed(() => [
  { label: 'Total DocTypes', value: stats.total_doctypes || 48, icon: '📋', color: '#0f172a', variant: '' },
  { label: 'Active Users', value: stats.active_users || 156, icon: '👤', color: '#0d9488', variant: '' },
  { label: 'Open Feedback', value: stats.open_feedback || 0, icon: '💬', color: '#d97706', variant: stats.open_feedback > 0 ? 'warn' : 'good' },
  { label: 'Outstanding Fees', value: formatCurrency(stats.total_outstanding || 0), icon: '💰', color: '#dc2626', variant: stats.total_outstanding > 0 ? 'warn' : 'good' },
])

const enrollmentChartData = computed(() => {
  return {
    labels: ['Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    datasets: [{
      label: 'New Enrollments',
      data: [120, 145, 130, 160, 155, 170],
      backgroundColor: 'rgba(14, 184, 166, 0.7)',
      borderColor: 'rgba(14, 184, 166, 1)',
      borderWidth: 1,
      borderRadius: 6
    }]
  }
})

const feeHealthChartData = computed(() => {
  return {
    labels: ['Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    datasets: [
      {
        label: 'Collected (₹L)',
        data: [12.5, 14.5, 13.8, 16.2, 15.8, 17.5],
        borderColor: 'rgba(14, 184, 166, 1)',
        backgroundColor: 'rgba(14, 184, 166, 0.1)',
        fill: true,
        tension: 0.3,
        pointBackgroundColor: 'rgba(14, 184, 166, 1)',
        pointBorderColor: '#fff',
        pointBorderWidth: 2,
        pointRadius: 5
      },
      {
        label: 'Outstanding (₹L)',
        data: [8.2, 7.1, 6.5, 5.8, 6.1, 5.2],
        borderColor: 'rgba(220, 38, 38, 1)',
        backgroundColor: 'rgba(220, 38, 38, 0.1)',
        fill: true,
        tension: 0.3,
        pointBackgroundColor: 'rgba(220, 38, 38, 1)',
        pointBorderColor: '#fff',
        pointBorderWidth: 2,
        pointRadius: 5
      }
    ]
  }
})

function formatCurrency(v) {
  return '₹' + Number(v || 0).toLocaleString('en-IN', { minimumFractionDigits: 0 })
}

onMounted(async () => {
  user.value = getSessionUser()
  if (!user.value) return
  try {
    const data = await callAPI('portal_get_admin_overview')
    stats.value = data.stats || stats.value
    pipeline.value = data.pipeline || pipeline.value
  } catch (e) {
    console.error('Admin cockpit load error:', e)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.cockpit-page { animation: fadeIn var(--transition-base); }
.cockpit-loading { padding: var(--space-6); }
.stats-skeleton { display: grid; grid-template-columns: repeat(4, 1fr); gap: var(--space-4); }
.dash-skeleton { display: grid; grid-template-columns: repeat(3, 1fr); gap: var(--space-4); }

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--space-4);
  margin-bottom: var(--space-4);
}
.stats-grid--8 { margin-bottom: var(--space-6); }

.dash-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-4);
}

.dash-card--wide {
  grid-column: span 2;
}

.module-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--space-3);
}

.module-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-4) var(--space-2);
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-border-light);
  text-decoration: none;
  transition: all var(--transition-fast);
  text-align: center;
}
.module-card:hover { border-color: var(--color-accent-light); background: var(--color-accent-50); transform: translateY(-2px); box-shadow: var(--shadow-md); }
.module-icon { width: 44px; height: 44px; border-radius: var(--radius-lg); display: flex; align-items: center; justify-content: center; font-size: 1.25rem; }
.module-label { font-size: var(--text-xs); font-weight: var(--font-weight-semibold); color: var(--color-text); }

.pipeline-summary {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-4);
  padding: var(--space-4) 0;
}
.pipeline-summary-item { text-align: center; }
.pipeline-count { display: block; font-size: var(--text-3xl); font-weight: var(--font-weight-bold); color: var(--color-text); }
.pipeline-label { font-size: var(--text-xs); color: var(--color-text-muted); font-weight: var(--font-weight-medium); }
.pipeline-arrow { color: var(--gray-300); font-size: 20px; font-weight: var(--font-weight-bold); }

.pipeline-detail {
  display: flex;
  justify-content: center;
  gap: var(--space-4);
  flex-wrap: wrap;
}
.pipeline-stage-mini {
  display: flex;
  align-items: center;
  gap: var(--space-1-5);
  padding: var(--space-2) var(--space-3);
  background: var(--gray-50);
  border-radius: var(--radius-full);
  font-size: var(--text-xs);
}
.stage-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
.stage-name { color: var(--color-text-secondary); }
.stage-count-mini { font-weight: var(--font-weight-bold); color: var(--color-text); font-variant-numeric: tabular-nums; }

.health-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--space-3);
}

.health-item {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3);
  border-radius: var(--radius-md);
  border: 1px solid var(--color-border-light);
  background: var(--gray-50);
  transition: all var(--transition-fast);
}
.health-item:hover { border-color: var(--color-accent-light); box-shadow: var(--shadow-sm); }
.health-icon { width: 36px; height: 36px; border-radius: var(--radius-md); display: flex; align-items: center; justify-content: center; font-size: 1rem; flex-shrink: 0; }
.health-content { display: flex; flex-direction: column; gap: 2px; }
.health-label { font-size: var(--text-sm); color: var(--color-text-secondary); }
.health-value { font-size: var(--text-sm); font-weight: var(--font-weight-semibold); color: var(--color-text); font-variant-numeric: tabular-nums; }
.health-value.good { color: var(--color-success); }
.health-value.warn { color: var(--color-warning); }

@media (max-width: 1024px) {
  .stats-grid { grid-template-columns: repeat(2, 1fr); }
  .stats-grid--8 { grid-template-columns: repeat(2, 1fr); }
  .dash-grid { grid-template-columns: repeat(2, 1fr); }
  .dash-card--wide { grid-column: span 2; }
  .module-grid { grid-template-columns: repeat(2, 1fr); }
  .health-grid { grid-template-columns: 1fr; }
}
@media (max-width: 768px) {
  .stats-grid { grid-template-columns: 1fr; }
  .stats-grid--8 { grid-template-columns: 1fr; }
  .dash-grid { grid-template-columns: 1fr; }
  .dash-card--wide { grid-column: span 1; }
  .module-grid { grid-template-columns: repeat(2, 1fr); }
  .pipeline-summary { flex-direction: column; gap: var(--space-2); }
  .pipeline-arrow { transform: rotate(90deg); }
}
</style>