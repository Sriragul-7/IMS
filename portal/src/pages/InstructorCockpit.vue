<template>
  <div class="cockpit-page">
    <div v-if="loading" class="cockpit-loading">
      <div class="skeleton skeleton--heading" style="width: 30%;"></div>
      <div class="skeleton skeleton--text" style="width: 50%; margin-top: var(--space-2);"></div>
      <div class="stats-skeleton" style="margin-top: var(--space-6);">
        <Skeleton type="stat" v-for="i in 4" :key="i" />
      </div>
      <div class="dash-skeleton" style="margin-top: var(--space-6);">
        <Skeleton type="card" v-for="i in 3" :key="i" />
      </div>
    </div>

    <template v-else>
      <!-- Hero Banner -->
      <HeroBanner 
        :title="`Welcome, ${user?.user_name}!`"
        :subtitle="`${greeting} — Instructor Dashboard`"
        :meta-items="heroMeta"
        illustration="dashboard"
        variant="success"
      >
        <template #actions>
          <a href="/app" class="btn btn-glass" target="_blank">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
            Open Full Desk
          </a>
        </template>
      </HeroBanner>

      <!-- Stat Cards -->
      <div class="stats-grid">
        <StatCard :value="stats.total_students" label="My Students" color="#0f172a" icon="👥" variant="default" :trend="studentsTrend" trend-variant="positive" />
        <StatCard :value="stats.total_groups" label="Assigned Groups" color="#7c3aed" icon="📚" variant="purple" />
        <StatCard :value="stats.attendance_marked_today" label="Attendance Today" color="#059669" icon="✅" variant="success" :trend="attendanceTrend" trend-variant="positive" />
        <StatCard :value="stats.pending_marks" label="Pending Marks" color="#d97706" icon="✏️" variant="amber" :trend="marksTrend" trend-variant="negative" />
      </div>

      <!-- Main Grid -->
      <div class="dash-grid">
        <!-- Today's Classes -->
        <div class="card card-hover dash-card--wide">
          <div class="card-header">
            <h3>Today's Classes</h3>
          </div>
          <div class="card-body" v-if="classes.length">
            <TimelineList 
              :items="classTimelineItems"
              :vertical="true"
              empty-title="No classes today"
              empty-description="No scheduled classes for today"
              empty-icon="📅"
            >
              <template #actions="{ item }">
                <a :href="`/app/course-schedule/${item.scheduleId}`" target="_blank" class="btn btn-ghost btn-xs">View</a>
              </template>
            </TimelineList>
          </div>
          <div class="card-body" v-else>
            <EmptyState title="No classes today" description="No scheduled classes for today" icon="📅" size="sm" />
          </div>
        </div>

        <!-- Quick Actions -->
        <div class="card card-hover">
          <div class="card-header">
            <h3>Quick Actions</h3>
          </div>
          <div class="card-body">
            <div class="action-grid">
              <a href="/app/student-attendance/new" class="action-card" target="_blank">
                <div class="action-icon" style="background:rgba(5,150,105,0.1);color:#059669">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="8.5" cy="7" r="4"></circle><line x1="18" y1="8" x2="18" y2="14"></line><line x1="22" y1="8" x2="22" y2="14"></line></svg>
                </div>
                <div class="action-content">
                  <span class="action-label">Mark Attendance</span>
                  <span class="action-desc">Bulk attendance for a class</span>
                </div>
              </a>
              <a href="/app/assessment-result/new" class="action-card" target="_blank">
                <div class="action-icon" style="background:rgba(217,119,6,0.1);color:#d97706">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 3a2.828 2.828 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5L17 3z"></path></svg>
                </div>
                <div class="action-content">
                  <span class="action-label">Enter Marks</span>
                  <span class="action-desc">Bulk marks entry for assessments</span>
                </div>
              </a>
              <a href="/app/assessment-plan" class="action-card" target="_blank">
                <div class="action-icon" style="background:rgba(30,64,175,0.1);color:#1e40af">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>
                </div>
                <div class="action-content">
                  <span class="action-label">Assessment Plans</span>
                  <span class="action-desc">View and manage assessments</span>
                </div>
              </a>
              <a href="/app/course-schedule" class="action-card" target="_blank">
                <div class="action-icon" style="background:rgba(14,184,166,0.1);color:#0d9488">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
                </div>
                <div class="action-content">
                  <span class="action-label">My Schedule</span>
                  <span class="action-desc">View all scheduled classes</span>
                </div>
              </a>
            </div>
          </div>
        </div>

        <!-- Pending Marks Entry -->
        <div class="card card-hover">
          <div class="card-header">
            <h3>Pending Marks Entry</h3>
          </div>
          <div class="card-body" v-if="pendingAssessments.length">
            <TimelineList 
              :items="pendingTimelineItems"
              :vertical="true"
              empty-title="All caught up"
              empty-description="No pending marks entry"
              empty-icon="✅"
            >
              <template #actions="{ item }">
                <a :href="`/app/assessment-result?assessment_plan=${item.planName}`" target="_blank" class="btn btn-accent btn-sm">Enter</a>
              </template>
            </TimelineList>
          </div>
          <div class="card-body" v-else>
            <EmptyState title="All caught up" description="No pending marks entry" icon="✅" size="sm" />
          </div>
        </div>

        <!-- Class Strength Chart -->
        <div class="card card-hover dash-card--wide">
          <div class="card-header">
            <h3>Class Strength Overview</h3>
          </div>
          <div class="card-body">
            <ChartCard 
              type="bar"
              :chart-data="classStrengthChartData"
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
import TimelineList from '../components/TimelineList.vue'
import Skeleton from '../components/Skeleton.vue'

const user = ref(null)
const stats = ref({ total_students: 0, total_groups: 0, attendance_marked_today: 0, pending_marks: 0 })
const classes = ref([])
const pendingAssessments = ref([])
const loading = ref(true)
const chartLoading = ref(false)

const greeting = computed(() => {
  const h = new Date().getHours()
  if (h < 12) return 'Good morning'
  if (h < 17) return 'Good afternoon'
  return 'Good evening'
})

const heroMeta = computed(() => [
  { label: 'Department', value: user.value?.department || '—', icon: '🏢' },
  { label: 'Role', value: user.value?.role || 'Instructor', icon: '👨‍🏫' }
])

const studentsTrend = '+3 this term'
const attendanceTrend = '+2 vs yesterday'
const marksTrend = '5 pending'

const classTimelineItems = computed(() => {
  return classes.value.map(c => ({
    id: c.name,
    title: `${c.course} (${c.course_code})`,
    time: c.time_slot,
    scheduleId: c.schedule_id,
    badge: { text: c.status, variant: c.status === 'Ongoing' ? 'success' : c.status === 'Upcoming' ? 'info' : 'neutral', dot: true },
    meta: c.room ? [{ label: 'Room', value: c.room }] : []
  }))
})

const pendingTimelineItems = computed(() => {
  return pendingAssessments.value.map(a => ({
    id: a.name,
    title: a.assessment_name,
    time: a.due_date,
    planName: a.name,
    badge: { text: 'Due Soon', variant: 'warning', dot: true },
    meta: [{ label: 'Course', value: a.course }, { label: 'Group', value: a.student_group }]
  }))
})

const classStrengthChartData = computed(() => {
  if (!classes.value.length) return null
  return {
    labels: classes.value.map(c => c.course_code),
    datasets: [{
      label: 'Students',
      data: classes.value.map(c => c.student_count || 0),
      backgroundColor: 'rgba(14, 184, 166, 0.7)',
      borderColor: 'rgba(14, 184, 166, 1)',
      borderWidth: 1,
      borderRadius: 6
    }]
  }
})

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
.cockpit-page { animation: fadeIn var(--transition-base); }
.cockpit-loading { padding: var(--space-6); }
.stats-skeleton { display: grid; grid-template-columns: repeat(4, 1fr); gap: var(--space-4); }
.dash-skeleton { display: grid; grid-template-columns: repeat(3, 1fr); gap: var(--space-4); }

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

.dash-card--wide {
  grid-column: span 2;
}

.action-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--space-3);
}

.action-card {
  display: flex;
  align-items: flex-start;
  gap: var(--space-3);
  padding: var(--space-4);
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-border-light);
  text-decoration: none;
  transition: all var(--transition-fast);
}
.action-card:hover { border-color: var(--color-accent-light); background: var(--color-accent-50); transform: translateY(-2px); box-shadow: var(--shadow-md); }
.action-icon { width: 44px; height: 44px; border-radius: var(--radius-lg); display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.action-content { display: flex; flex-direction: column; gap: 2px; }
.action-label { font-size: var(--text-sm); font-weight: var(--font-weight-semibold); color: var(--color-text); }
.action-desc { font-size: var(--text-xs); color: var(--color-text-muted); }

@media (max-width: 1024px) {
  .stats-grid { grid-template-columns: repeat(2, 1fr); }
  .dash-grid { grid-template-columns: repeat(2, 1fr); }
  .dash-card--wide { grid-column: span 2; }
  .action-grid { grid-template-columns: 1fr; }
}
@media (max-width: 768px) {
  .stats-grid { grid-template-columns: 1fr; }
  .dash-grid { grid-template-columns: 1fr; }
  .dash-card--wide { grid-column: span 1; }
}
</style>