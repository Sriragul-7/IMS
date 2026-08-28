<template>
  <div class="cockpit">
    <div v-if="loading" class="loading-overlay"><div class="spinner spinner-lg"></div></div>
    <template v-else>
      <div class="welcome-banner academic-banner">
        <div>
          <h2>Welcome, {{ user?.user_name }}!</h2>
          <p>{{ greeting }} — Academic Head Dashboard</p>
        </div>
        <a href="/app" class="btn btn-glass" target="_blank">Open Full Admin &#8599;</a>
      </div>

      <div class="stats-grid">
        <StatCard :value="stats.total_programs" label="PROGRAMS" color="#1e40af" icon="&#127891;" />
        <StatCard :value="stats.total_students" label="STUDENTS" color="#059669" icon="&#128218;" />
        <StatCard :value="stats.avg_attendance + '%'" label="AVG ATTENDANCE" color="#d97706" icon="&#9776;" />
        <StatCard :value="stats.total_courses" label="COURSES" color="#7c3aed" icon="&#128214;" />
      </div>

      <div class="dash-grid">
        <div class="card">
          <div class="card-header">
            <h3>Cross-Module Navigation</h3>
          </div>
          <div class="card-body">
            <div class="action-list">
              <a href="/app/student" class="action-item" target="_blank">
                <span class="action-icon" style="background:rgba(30,64,175,0.1);color:#1e40af">&#128100;</span>
                <div class="action-text">
                  <span class="action-label">Students</span>
                  <span class="action-desc">View and manage all students</span>
                </div>
              </a>
              <a href="/app/student-group" class="action-item" target="_blank">
                <span class="action-icon" style="background:rgba(5,150,105,0.1);color:#059669">&#127979;</span>
                <div class="action-text">
                  <span class="action-label">Student Groups</span>
                  <span class="action-desc">Manage student groups and sections</span>
                </div>
              </a>
              <a href="/app/course" class="action-item" target="_blank">
                <span class="action-icon" style="background:rgba(124,58,237,0.1);color:#7c3aed">&#128214;</span>
                <div class="action-text">
                  <span class="action-label">Courses</span>
                  <span class="action-desc">Manage course catalog</span>
                </div>
              </a>
              <a href="/app/program" class="action-item" target="_blank">
                <span class="action-icon" style="background:rgba(217,119,6,0.1);color:#d97706">&#127891;</span>
                <div class="action-text">
                  <span class="action-label">Programs</span>
                  <span class="action-desc">Manage academic programs</span>
                </div>
              </a>
            </div>
          </div>
        </div>

        <div class="card">
          <div class="card-header">
            <h3>Attendance Overview</h3>
            <a href="/app/student-attendance" class="btn btn-ghost btn-sm" target="_blank">Details</a>
          </div>
          <div class="card-body" v-if="attendanceOverview.length">
            <div v-for="att in attendanceOverview.slice(0, 6)" :key="att.group" class="att-row">
              <div class="att-info">
                <span class="att-group">{{ att.group }}</span>
                <span class="att-detail">{{ att.marked }}/{{ att.total }} marked</span>
              </div>
              <div class="att-pct" :class="att.pct >= 80 ? 'good' : att.pct >= 60 ? 'warn' : 'low'">
                {{ att.pct }}%
              </div>
            </div>
          </div>
          <div class="card-body" v-else>
            <EmptyState title="No attendance data" description="Attendance data not available" icon="&#9776;" />
          </div>
        </div>

        <div class="card">
          <div class="card-header">
            <h3>Exam Performance Snapshot</h3>
          </div>
          <div class="card-body" v-if="examPerformance.length">
            <div v-for="ex in examPerformance.slice(0, 6)" :key="ex.assessment" class="exam-row">
              <div class="exam-info">
                <span class="exam-name">{{ ex.assessment }}</span>
                <span class="exam-detail">{{ ex.submitted }}/{{ ex.total }} submitted</span>
              </div>
              <StatusBadge :text="ex.status" :variant="ex.status === 'Complete' ? 'success' : 'warning'" />
            </div>
          </div>
          <div class="card-body" v-else>
            <EmptyState title="No exam data" description="Exam performance data not available" icon="&#128202;" />
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
const stats = ref({ total_programs: 0, total_students: 0, avg_attendance: 0, total_courses: 0 })
const attendanceOverview = ref([])
const examPerformance = ref([])
const loading = ref(true)

const greeting = computed(() => {
  const h = new Date().getHours()
  if (h < 12) return 'Good morning'
  if (h < 17) return 'Good afternoon'
  return 'Good evening'
})

onMounted(async () => {
  user.value = getSessionUser()
  if (!user.value) return
  try {
    const [overview, att, exams] = await Promise.all([
      callAPI('portal_get_academic_overview').catch(() => ({})),
      callAPI('portal_get_attendance_overview').catch(() => []),
      callAPI('portal_get_exam_performance').catch(() => []),
    ])
    stats.value = {
      total_programs: overview.programs || 0,
      total_students: overview.students || 0,
      avg_attendance: overview.avg_attendance || 0,
      total_courses: overview.courses || 0,
    }
    attendanceOverview.value = Array.isArray(att) ? att : []
    examPerformance.value = Array.isArray(exams) ? exams : []
  } catch (e) {
    console.error('Academic Head cockpit load error:', e)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.welcome-banner { background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); color: white; padding: var(--space-6) var(--space-8); border-radius: var(--radius-xl); margin-bottom: var(--space-6); display: flex; justify-content: space-between; align-items: center; }
.welcome-banner h2 { font-size: var(--text-2xl); font-weight: 700; margin-bottom: var(--space-1); }
.welcome-banner p { font-size: var(--text-sm); opacity: 0.85; }
.btn-glass { padding: var(--space-2) var(--space-4); border-radius: var(--radius-md); background: rgba(255,255,255,0.15); color: white; font-size: var(--text-sm); font-weight: 600; text-decoration: none; transition: all var(--transition-fast); white-space: nowrap; }
.btn-glass:hover { background: rgba(255,255,255,0.25); }
.stats-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: var(--space-4); margin-bottom: var(--space-6); }
.dash-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: var(--space-4); }

.action-list { display: flex; flex-direction: column; gap: var(--space-2); }
.action-item { display: flex; align-items: center; gap: var(--space-3); padding: var(--space-3); border-radius: var(--radius-md); border: 1px solid var(--color-border-light); text-decoration: none; transition: all var(--transition-fast); }
.action-item:hover { border-color: var(--color-primary-light); background: var(--color-primary-50); }
.action-icon { width: 36px; height: 36px; border-radius: var(--radius-md); display: flex; align-items: center; justify-content: center; font-size: 16px; flex-shrink: 0; }
.action-text { flex: 1; }
.action-label { display: block; font-size: var(--text-sm); font-weight: 600; color: var(--color-text); }
.action-desc { font-size: var(--text-xs); color: var(--color-text-muted); }

.att-row { display: flex; align-items: center; justify-content: space-between; padding: var(--space-3) 0; border-bottom: 1px solid var(--color-border-light); }
.att-row:last-child { border-bottom: none; }
.att-info { flex: 1; min-width: 0; }
.att-group { display: block; font-size: var(--text-sm); font-weight: 500; }
.att-detail { font-size: var(--text-xs); color: var(--color-text-muted); }
.att-pct { font-size: var(--text-sm); font-weight: 700; }
.att-pct.good { color: var(--color-success); }
.att-pct.warn { color: var(--color-warning); }
.att-pct.low { color: var(--color-danger); }

.exam-row { display: flex; align-items: center; justify-content: space-between; padding: var(--space-3) 0; border-bottom: 1px solid var(--color-border-light); }
.exam-row:last-child { border-bottom: none; }
.exam-info { flex: 1; min-width: 0; }
.exam-name { display: block; font-size: var(--text-sm); font-weight: 500; }
.exam-detail { font-size: var(--text-xs); color: var(--color-text-muted); }

@media (max-width: 1024px) { .stats-grid { grid-template-columns: repeat(2, 1fr); } .dash-grid { grid-template-columns: 1fr; } }
@media (max-width: 640px) { .stats-grid { grid-template-columns: 1fr; } .welcome-banner { flex-direction: column; gap: var(--space-3); } }
</style>
