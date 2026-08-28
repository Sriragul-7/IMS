<template>
  <div class="cockpit">
    <div v-if="loading" class="loading-overlay">
      <div class="spinner spinner-lg"></div>
    </div>

    <template v-else>
      <div class="welcome-banner">
        <div>
          <h2>Welcome, {{ user?.user_name }}!</h2>
          <p>{{ greeting }} — Instructor Dashboard</p>
        </div>
        <a href="/app" class="btn btn-glass" target="_blank">Open Full Admin &#8599;</a>
      </div>

      <div class="stats-grid">
        <StatCard :value="stats.total_students" label="MY STUDENTS" color="#1e40af" icon="&#128218;" />
        <StatCard :value="stats.total_groups" label="ASSIGNED GROUPS" color="#7c3aed" icon="&#127979;" />
        <StatCard :value="stats.attendance_marked_today" label="ATTENDANCE TODAY" color="#059669" icon="&#9989;" />
        <StatCard :value="stats.pending_marks" label="PENDING MARKS" color="#d97706" icon="&#9998;" />
      </div>

      <div class="dash-grid">
        <div class="card">
          <div class="card-header">
            <h3>Today's Classes</h3>
          </div>
          <div class="card-body" v-if="classes.length">
            <div v-for="c in classes" :key="c.name" class="class-row">
              <div class="class-info">
                <span class="class-course">{{ c.course }}</span>
                <span class="class-schedule">{{ c.course_code }} — {{ c.time_slot }}</span>
              </div>
              <div class="class-right">
                <StatusBadge :text="c.status" :variant="c.status === 'Ongoing' ? 'success' : c.status === 'Upcoming' ? 'info' : 'neutral'" />
              </div>
            </div>
          </div>
          <div class="card-body" v-else>
            <EmptyState title="No classes today" description="No scheduled classes for today" icon="&#127979;" />
          </div>
        </div>

        <div class="card">
          <div class="card-header">
            <h3>Quick Actions</h3>
          </div>
          <div class="card-body">
            <div class="action-list">
              <a href="/app/student-attendance/new" class="action-item" target="_blank">
                <span class="action-icon" style="background:rgba(5,150,105,0.1);color:#059669">&#9989;</span>
                <div class="action-text">
                  <span class="action-label">Mark Attendance</span>
                  <span class="action-desc">Bulk attendance for a class</span>
                </div>
              </a>
              <a href="/app/assessment-result/new" class="action-item" target="_blank">
                <span class="action-icon" style="background:rgba(217,119,6,0.1);color:#d97706">&#9998;</span>
                <div class="action-text">
                  <span class="action-label">Enter Marks</span>
                  <span class="action-desc">Bulk marks entry for assessments</span>
                </div>
              </a>
              <a href="/app/assessment-plan" class="action-item" target="_blank">
                <span class="action-icon" style="background:rgba(30,64,175,0.1);color:#1e40af">&#128203;</span>
                <div class="action-text">
                  <span class="action-label">Assessment Plans</span>
                  <span class="action-desc">View and manage assessments</span>
                </div>
              </a>
            </div>
          </div>
        </div>

        <div class="card">
          <div class="card-header">
            <h3>Pending Marks Entry</h3>
          </div>
          <div class="card-body" v-if="pendingAssessments.length">
            <div v-for="a in pendingAssessments" :key="a.name" class="pending-row">
              <div class="pending-info">
                <span class="pending-name">{{ a.assessment_name }}</span>
                <span class="pending-date">Due: {{ formatDate(a.due_date) }}</span>
              </div>
              <a :href="`/app/assessment-result?assessment_plan=${a.name}`" class="btn btn-sm btn-outline" target="_blank">Enter</a>
            </div>
          </div>
          <div class="card-body" v-else>
            <EmptyState title="All caught up" description="No pending marks entry" icon="&#10003;" />
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
const stats = ref({ total_students: 0, total_groups: 0, attendance_marked_today: 0, pending_marks: 0 })
const classes = ref([])
const pendingAssessments = ref([])
const loading = ref(true)

const greeting = computed(() => {
  const h = new Date().getHours()
  if (h < 12) return 'Good morning'
  if (h < 17) return 'Good afternoon'
  return 'Good evening'
})

function formatDate(d) {
  return d ? new Date(d).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }) : '—'
}

onMounted(async () => {
  user.value = getSessionUser()
  if (!user.value) return
  try {
    const [attSummary, pending] = await Promise.all([
      callAPI('portal_get_attendance_summary').catch(() => null),
      callAPI('portal_get_pending_assessments').catch(() => []),
    ])
    stats.value = {
      total_students: attSummary?.total_students || 0,
      total_groups: attSummary?.total_groups || 0,
      attendance_marked_today: attSummary?.marked_today || 0,
      pending_marks: Array.isArray(pending) ? pending.length : 0,
    }
    classes.value = attSummary?.today_classes || []
    pendingAssessments.value = Array.isArray(pending) ? pending : []
  } catch (e) {
    console.error('Instructor cockpit load error:', e)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.welcome-banner {
  background: linear-gradient(135deg, #059669 0%, #047857 100%);
  color: white;
  padding: var(--space-6) var(--space-8);
  border-radius: var(--radius-xl);
  margin-bottom: var(--space-6);
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.welcome-banner h2 { font-size: var(--text-2xl); font-weight: 700; margin-bottom: var(--space-1); }
.welcome-banner p { font-size: var(--text-sm); opacity: 0.85; }

.btn-glass {
  padding: var(--space-2) var(--space-4);
  border-radius: var(--radius-md);
  background: rgba(255,255,255,0.15);
  color: white;
  font-size: var(--text-sm);
  font-weight: 600;
  text-decoration: none;
  transition: all var(--transition-fast);
  white-space: nowrap;
}
.btn-glass:hover { background: rgba(255,255,255,0.25); }

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

.class-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-3) 0;
  border-bottom: 1px solid var(--color-border-light);
}
.class-row:last-child { border-bottom: none; }
.class-info { flex: 1; min-width: 0; }
.class-course { display: block; font-size: var(--text-sm); font-weight: 600; color: var(--color-text); }
.class-schedule { font-size: var(--text-xs); color: var(--color-text-muted); }

.action-list { display: flex; flex-direction: column; gap: var(--space-2); }
.action-item {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3);
  border-radius: var(--radius-md);
  border: 1px solid var(--color-border-light);
  text-decoration: none;
  transition: all var(--transition-fast);
}
.action-item:hover { border-color: var(--color-primary-light); background: var(--color-primary-50); }
.action-icon { width: 36px; height: 36px; border-radius: var(--radius-md); display: flex; align-items: center; justify-content: center; font-size: 16px; flex-shrink: 0; }
.action-text { flex: 1; }
.action-label { display: block; font-size: var(--text-sm); font-weight: 600; color: var(--color-text); }
.action-desc { font-size: var(--text-xs); color: var(--color-text-muted); }

.pending-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-3) 0;
  border-bottom: 1px solid var(--color-border-light);
}
.pending-row:last-child { border-bottom: none; }
.pending-info { flex: 1; min-width: 0; }
.pending-name { display: block; font-size: var(--text-sm); font-weight: 500; }
.pending-date { font-size: var(--text-xs); color: var(--color-text-muted); }

.btn-outline {
  padding: var(--space-1) var(--space-3);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  background: transparent;
  color: var(--color-primary);
  font-size: var(--text-xs);
  font-weight: 600;
  text-decoration: none;
  cursor: pointer;
}
.btn-outline:hover { background: var(--color-primary-50); }

@media (max-width: 1024px) {
  .stats-grid { grid-template-columns: repeat(2, 1fr); }
  .dash-grid { grid-template-columns: 1fr; }
}
@media (max-width: 640px) {
  .stats-grid { grid-template-columns: 1fr; }
  .welcome-banner { flex-direction: column; gap: var(--space-3); }
}
</style>
