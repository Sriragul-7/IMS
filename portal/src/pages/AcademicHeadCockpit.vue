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
      <HeroBanner 
        :title="`Welcome, ${user?.user_name}!`"
        :subtitle="`${greeting} — Academic Head Dashboard`"
        :meta-items="heroMeta"
        illustration="books"
        variant="dark"
      >
        <template #actions>
          <a href="/app" class="btn btn-glass" target="_blank">
            <span class="icon-svg" v-html="icons.layers"></span>
            Open Full Desk
          </a>
        </template>
      </HeroBanner>

      <div class="stats-grid">
        <StatCard :value="stats.total_programs" label="Programs" color="#0f172a" :icon="icons.graduation" variant="default" />
        <StatCard :value="stats.total_students" label="Students" color="#059669" :icon="icons.users" variant="success" />
        <StatCard :value="stats.avg_attendance" label="Avg Attendance" format="percent" color="#d97706" :icon="icons.chart" variant="amber" :trend="attendanceTrend" trend-variant="positive" />
        <StatCard :value="stats.total_courses" label="Courses" color="#0d9488" :icon="icons.books" variant="default" />
      </div>

      <div class="dash-grid">
        <div class="card card-hover">
          <div class="card-header">
            <h3>Cross-Module Navigation</h3>
          </div>
          <div class="card-body">
            <div class="action-grid">
              <a href="/app/student" class="action-card" target="_blank">
                <div class="action-card__icon" style="background:rgba(15,23,42,0.08);color:#0f172a" v-html="icons.user"></div>
                <span class="action-card__title">Students</span>
                <span class="action-card__desc">View and manage all students</span>
              </a>
              <a href="/app/student-group" class="action-card" target="_blank">
                <div class="action-card__icon" style="background:rgba(5,150,105,0.1);color:#059669" v-html="icons.users"></div>
                <span class="action-card__title">Student Groups</span>
                <span class="action-card__desc">Manage groups and sections</span>
              </a>
              <a href="/app/course" class="action-card" target="_blank">
                <div class="action-card__icon" style="background:rgba(13,148,136,0.1);color:#0d9488" v-html="icons.book"></div>
                <span class="action-card__title">Courses</span>
                <span class="action-card__desc">Manage course catalog</span>
              </a>
              <a href="/app/program" class="action-card" target="_blank">
                <div class="action-card__icon" style="background:rgba(217,119,6,0.1);color:#d97706" v-html="icons.graduation"></div>
                <span class="action-card__title">Programs</span>
                <span class="action-card__desc">Manage academic programs</span>
              </a>
            </div>
          </div>
        </div>

        <div class="card card-hover">
          <div class="card-header">
            <h3>Attendance Overview</h3>
            <a href="/app/student-attendance" class="btn btn-ghost btn-sm" target="_blank">Details</a>
          </div>
          <div class="card-body" v-if="attendanceOverview.length">
            <TimelineList 
              :items="attendanceTimelineItems"
              :vertical="true"
              empty-title="No attendance data"
              empty-description="Attendance data not available"
              :empty-icon="icons.calendar"
            >
              <template #actions="{ item }">
                <a :href="`/app/student-attendance?group=${item.groupId}`" target="_blank" class="btn btn-ghost btn-xs">View</a>
              </template>
            </TimelineList>
          </div>
          <div class="card-body" v-else>
            <EmptyState title="No attendance data" description="Attendance data not available" :icon="icons.calendar" size="sm" />
          </div>
        </div>

        <div class="card card-hover">
          <div class="card-header">
            <h3>Exam Performance Snapshot</h3>
          </div>
          <div class="card-body" v-if="examPerformance.length">
            <TimelineList 
              :items="examTimelineItems"
              :vertical="true"
              empty-title="No exam data"
              empty-description="Exam performance data not available"
              :empty-icon="icons.document"
            >
              <template #actions="{ item }">
                <a :href="`/app/assessment-result?assessment_plan=${item.planId}`" target="_blank" class="btn btn-ghost btn-xs">View</a>
              </template>
            </TimelineList>
          </div>
          <div class="card-body" v-else>
            <EmptyState title="No exam data" description="Exam performance data not available" :icon="icons.document" size="sm" />
          </div>
        </div>

        <div class="card card-hover dash-card--wide">
          <div class="card-header">
            <h3>Program-wise Student Distribution</h3>
          </div>
          <div class="card-body">
            <ChartCard 
              type="doughnut"
              :chart-data="programDistributionChartData"
              :height="280"
              :loading="chartLoading"
              :legend-items="programLegendItems"
            />
          </div>
        </div>

        <div class="card card-hover dash-card--wide">
          <div class="card-header">
            <h3>Exam Performance Trend (3 Assessments)</h3>
          </div>
          <div class="card-body">
            <ChartCard 
              type="line"
              :chart-data="examTrendChartData"
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
import { icons } from '../utils/icons.js'
import StatCard from '../components/StatCard.vue'
import StatusBadge from '../components/StatusBadge.vue'
import EmptyState from '../components/EmptyState.vue'
import HeroBanner from '../components/HeroBanner.vue'
import ChartCard from '../components/ChartCard.vue'
import TimelineList from '../components/TimelineList.vue'
import Skeleton from '../components/Skeleton.vue'

const user = ref(null)
const stats = ref({ total_programs: 0, total_students: 0, avg_attendance: 0, total_courses: 0 })
const attendanceOverview = ref([])
const examPerformance = ref([])
const loading = ref(true)
const chartLoading = ref(false)

const greeting = computed(() => {
  const h = new Date().getHours()
  if (h < 12) return 'Good morning'
  if (h < 17) return 'Good afternoon'
  return 'Good evening'
})

const heroMeta = computed(() => [
  { label: 'Role', value: 'Academic Head', icon: icons.books }
])

const attendanceTrend = '+1.5% this term'

const attendanceTimelineItems = computed(() => {
  return attendanceOverview.value.slice(0, 6).map(att => ({
    id: att.group,
    title: att.group,
    time: new Date(),
    groupId: att.group_id,
    badge: { text: `${att.pct}%`, variant: att.pct >= 80 ? 'success' : att.pct >= 60 ? 'warning' : 'danger', dot: true },
    meta: [{ label: 'Marked', value: `${att.marked}/${att.total}` }]
  }))
})

const examTimelineItems = computed(() => {
  return examPerformance.value.slice(0, 6).map(ex => ({
    id: ex.assessment,
    title: ex.assessment,
    time: new Date(),
    planId: ex.assessment_id,
    badge: { text: ex.status, variant: ex.status === 'Complete' ? 'success' : 'warning', dot: true },
    meta: [{ label: 'Submitted', value: `${ex.submitted}/${ex.total}` }]
  }))
})

const programLegendItems = computed(() => [
  { label: 'B.E. CSE', value: '120', color: '#0f172a' },
  { label: 'B.E. ECE', value: '95', color: '#0d9488' },
  { label: 'B.E. Mechanical', value: '85', color: '#334155' },
  { label: 'B.Tech AI&DS', value: '70', color: '#d97706' },
  { label: 'B.Tech IT', value: '65', color: '#2563eb' },
  { label: 'MBA', value: '45', color: '#059669' }
])

const programDistributionChartData = computed(() => {
  return {
    labels: ['B.E. CSE', 'B.E. ECE', 'B.E. Mechanical', 'B.Tech AI&DS', 'B.Tech IT', 'MBA'],
    datasets: [{
      data: [120, 95, 85, 70, 65, 45],
      backgroundColor: ['#0f172a', '#0d9488', '#334155', '#d97706', '#2563eb', '#059669'],
      borderWidth: 0,
      hoverOffset: 8
    }]
  }
})

const examTrendChartData = computed(() => {
  return {
    labels: ['Unit Test 1', 'Mid Term', 'Final'],
    datasets: [
      {
        label: 'Avg Score %',
        data: [68, 72, 75],
        borderColor: 'rgba(14, 184, 166, 1)',
        backgroundColor: 'rgba(14, 184, 166, 0.1)',
        fill: true,
        tension: 0.3,
        pointBackgroundColor: 'rgba(14, 184, 166, 1)',
        pointBorderColor: '#fff',
        pointBorderWidth: 2,
        pointRadius: 6
      },
      {
        label: 'Pass Rate %',
        data: [78, 85, 89],
        borderColor: 'rgba(5, 150, 105, 1)',
        backgroundColor: 'rgba(5, 150, 105, 0.1)',
        fill: true,
        tension: 0.3,
        pointBackgroundColor: 'rgba(5, 150, 105, 1)',
        pointBorderColor: '#fff',
        pointBorderWidth: 2,
        pointRadius: 6
      }
    ]
  }
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
      total_programs: overview.programs || 6,
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
.cockpit-page { animation: fadeIn var(--transition-base); }
.cockpit-loading { padding: var(--space-6); }
.stats-skeleton { display: grid; grid-template-columns: repeat(4, 1fr); gap: var(--space-4); }
.dash-skeleton { display: grid; grid-template-columns: repeat(3, 1fr); gap: var(--space-4); }

.dash-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-4);
}

.dash-card--wide {
  grid-column: span 2;
}

.action-grid {
  grid-template-columns: repeat(2, 1fr);
}

@media (max-width: 1024px) {
  .dash-grid { grid-template-columns: repeat(2, 1fr); }
  .dash-card--wide { grid-column: span 2; }
  .action-grid { grid-template-columns: 1fr; }
}
@media (max-width: 768px) {
  .dash-grid { grid-template-columns: 1fr; }
  .dash-card--wide { grid-column: span 1; }
}
</style>
