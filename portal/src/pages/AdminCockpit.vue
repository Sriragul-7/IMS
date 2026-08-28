<template>
  <div class="cockpit">
    <div v-if="loading" class="loading-overlay"><div class="spinner spinner-lg"></div></div>
    <template v-else>
      <div class="welcome-banner admin-banner">
        <div>
          <h2>Administration Mission Control</h2>
          <p>{{ greeting }} — Institution-wide overview for {{ user?.user_name }}</p>
        </div>
        <a href="/app" class="btn btn-glass" target="_blank">Open Full Admin &#8599;</a>
      </div>

      <div class="stats-grid">
        <StatCard :value="stats.total_students" label="ACTIVE STUDENTS" color="#1e40af" icon="&#128218;" />
        <StatCard :value="stats.total_staff" label="STAFF MEMBERS" color="#059669" icon="&#128101;" />
        <StatCard :value="stats.avg_attendance + '%'" label="AVG ATTENDANCE" color="#d97706" icon="&#9776;" />
        <StatCard :value="formatCurrency(stats.total_outstanding)" label="OUTSTANDING FEES" color="#dc2626" icon="&#128176;" />
      </div>

      <div class="stats-grid secondary">
        <StatCard :value="stats.total_programs" label="PROGRAMS" color="#7c3aed" icon="&#127891;" />
        <StatCard :value="stats.total_courses" label="COURSES" color="#2563eb" icon="&#128214;" />
        <StatCard :value="stats.open_feedback" label="OPEN FEEDBACK" color="#d97706" icon="&#10084;" />
        <StatCard :value="stats.library_active" label="LIBRARY ACTIVE" color="#059669" icon="&#128218;" />
      </div>

      <div class="dash-grid">
        <div class="card">
          <div class="card-header">
            <h3>Module Quick Access</h3>
          </div>
          <div class="card-body">
            <div class="action-grid">
              <a href="/app/student" class="action-item" target="_blank">
                <span class="action-icon" style="background:rgba(30,64,175,0.1);color:#1e40af">&#128218;</span>
                <span class="action-label">Students</span>
              </a>
              <a href="/app/instructor" class="action-item" target="_blank">
                <span class="action-icon" style="background:rgba(5,150,105,0.1);color:#059669">&#128101;</span>
                <span class="action-label">Instructors</span>
              </a>
              <a href="/app/fees" class="action-item" target="_blank">
                <span class="action-icon" style="background:rgba(217,119,6,0.1);color:#d97706">&#128176;</span>
                <span class="action-label">Fees</span>
              </a>
              <a href="/app/student-attendance" class="action-item" target="_blank">
                <span class="action-icon" style="background:rgba(16,185,129,0.1);color:#10b981">&#9989;</span>
                <span class="action-label">Attendance</span>
              </a>
              <a href="/app/assessment-plan" class="action-item" target="_blank">
                <span class="action-icon" style="background:rgba(124,58,237,0.1);color:#7c3aed">&#128202;</span>
                <span class="action-label">Assessments</span>
              </a>
              <a href="/app/library-transaction" class="action-item" target="_blank">
                <span class="action-icon" style="background:rgba(6,182,212,0.1);color:#06b6d4">&#128214;</span>
                <span class="action-label">Library</span>
              </a>
              <a href="/app/notice" class="action-item" target="_blank">
                <span class="action-icon" style="background:rgba(236,72,153,0.1);color:#ec4899">&#9998;</span>
                <span class="action-label">Notices</span>
              </a>
              <a href="/app/hostel" class="action-item" target="_blank">
                <span class="action-icon" style="background:rgba(245,158,11,0.1);color:#f59e0b">&#127968;</span>
                <span class="action-label">Hostel</span>
              </a>
            </div>
          </div>
        </div>

        <div class="card">
          <div class="card-header">
            <h3>Admissions Pipeline</h3>
            <a href="/app/student" class="btn btn-ghost btn-sm" target="_blank">View All</a>
          </div>
          <div class="card-body">
            <div class="pipeline-stages">
              <div class="pipeline-col">
                <div class="stage-header" style="border-top-color: #6b7280;">
                  <span class="stage-count">{{ pipeline.active }}</span>
                  <span class="stage-label">Active</span>
                </div>
              </div>
              <div class="pipeline-arrow">&#8594;</div>
              <div class="pipeline-col">
                <div class="stage-header" style="border-top-color: #d97706;">
                  <span class="stage-count">{{ pipeline.inactive }}</span>
                  <span class="stage-label">Inactive</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="card">
          <div class="card-header">
            <h3>System Health</h3>
          </div>
          <div class="card-body">
            <div class="health-list">
              <div class="health-row">
                <span class="health-label">Total Doctypes</span>
                <span class="health-value">{{ stats.total_doctypes }}</span>
              </div>
              <div class="health-row">
                <span class="health-label">Active Users</span>
                <span class="health-value">{{ stats.active_users }}</span>
              </div>
              <div class="health-row">
                <span class="health-label">Open Feedback</span>
                <span class="health-value" :class="stats.open_feedback > 0 ? 'warn' : 'good'">{{ stats.open_feedback }}</span>
              </div>
              <div class="health-row">
                <span class="health-label">Outstanding Fees</span>
                <span class="health-value" :class="stats.total_outstanding > 0 ? 'warn' : 'good'">{{ formatCurrency(stats.total_outstanding) }}</span>
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

const user = ref(null)
const stats = ref({
  total_students: 0, total_staff: 0, avg_attendance: 0, total_outstanding: 0,
  total_programs: 0, total_courses: 0, open_feedback: 0, library_active: 0,
  total_doctypes: 0, active_users: 0,
})
const pipeline = ref({ active: 0, inactive: 0 })
const loading = ref(true)

const greeting = computed(() => {
  const h = new Date().getHours()
  if (h < 12) return 'Good morning'
  if (h < 17) return 'Good afternoon'
  return 'Good evening'
})

function formatCurrency(v) {
  return '\u20b9' + Number(v || 0).toLocaleString('en-IN', { minimumFractionDigits: 0 })
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
.welcome-banner { background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%); color: white; padding: var(--space-6) var(--space-8); border-radius: var(--radius-xl); margin-bottom: var(--space-6); display: flex; justify-content: space-between; align-items: center; }
.welcome-banner h2 { font-size: var(--text-2xl); font-weight: 700; margin-bottom: var(--space-1); }
.welcome-banner p { font-size: var(--text-sm); opacity: 0.85; }
.btn-glass { padding: var(--space-2) var(--space-4); border-radius: var(--radius-md); background: rgba(255,255,255,0.15); color: white; font-size: var(--text-sm); font-weight: 600; text-decoration: none; transition: all var(--transition-fast); white-space: nowrap; }
.btn-glass:hover { background: rgba(255,255,255,0.25); }

.stats-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: var(--space-4); margin-bottom: var(--space-4); }
.stats-grid.secondary { margin-bottom: var(--space-6); }
.dash-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: var(--space-4); }

.action-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: var(--space-3); }
.action-item { display: flex; flex-direction: column; align-items: center; gap: var(--space-2); padding: var(--space-4) var(--space-2); border-radius: var(--radius-md); border: 1px solid var(--color-border-light); text-decoration: none; transition: all var(--transition-fast); text-align: center; }
.action-item:hover { border-color: var(--color-primary-light); background: var(--color-primary-50); transform: translateY(-1px); box-shadow: var(--shadow-sm); }
.action-icon { width: 40px; height: 40px; border-radius: var(--radius-md); display: flex; align-items: center; justify-content: center; font-size: 18px; }
.action-label { font-size: var(--text-xs); font-weight: 600; color: var(--color-text); }

.pipeline-stages { display: flex; align-items: center; justify-content: center; gap: var(--space-4); padding: var(--space-6) 0; }
.pipeline-col { flex: 1; text-align: center; }
.stage-header { border-top: 3px solid; padding-top: var(--space-3); display: flex; flex-direction: column; align-items: center; gap: var(--space-1); }
.stage-count { font-size: var(--text-3xl); font-weight: 700; color: var(--color-text); }
.stage-label { font-size: var(--text-xs); color: var(--color-text-muted); font-weight: 500; }
.pipeline-arrow { color: var(--gray-300); font-size: 20px; flex-shrink: 0; }

.health-list { display: flex; flex-direction: column; gap: var(--space-1); }
.health-row { display: flex; justify-content: space-between; align-items: center; padding: var(--space-3) 0; border-bottom: 1px solid var(--color-border-light); }
.health-row:last-child { border-bottom: none; }
.health-label { font-size: var(--text-sm); color: var(--color-text-secondary); }
.health-value { font-size: var(--text-sm); font-weight: 600; color: var(--color-text); }
.health-value.good { color: var(--color-success); }
.health-value.warn { color: var(--color-warning); }

@media (max-width: 1024px) { .stats-grid { grid-template-columns: repeat(2, 1fr); } .dash-grid { grid-template-columns: 1fr; } .action-grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 640px) { .stats-grid { grid-template-columns: 1fr; } .welcome-banner { flex-direction: column; gap: var(--space-3); } .action-grid { grid-template-columns: repeat(2, 1fr); } }
</style>
