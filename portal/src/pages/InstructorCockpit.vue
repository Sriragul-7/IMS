<template>
  <div class="cockpit-page">
    <div v-if="loading" class="cockpit-loading">
      <div class="skeleton skeleton--heading" style="width: 30%;"></div>
      <div class="skeleton skeleton--text" style="width: 50%; margin-top: var(--space-2);"></div>
      <div class="stats-grid" style="margin-top: var(--space-6);">
        <Skeleton type="stat" v-for="i in 4" :key="i" />
      </div>
      <div class="dash-grid" style="margin-top: var(--space-6);">
        <Skeleton type="card" v-for="i in 2" :key="i" />
      </div>
    </div>

    <div v-else>
      <!-- Hero Banner - Green for staff -->
      <HeroBanner
        :title="`Welcome, ${userName}!`"
        :subtitle="`${greeting} — Instructor Dashboard`"
        :meta-items="heroMeta"
        variant="success"
      >
        <template #actions>
          <button class="btn btn-primary" @click="saveAttendance">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"></path></svg>
            Save attendance
          </button>
        </template>
      </HeroBanner>

      <!-- Stat Cards -->
      <div class="stats-grid">
        <StatCard :value="stats.classes_today" label="Classes today" color="#0f172a" icon="CL" variant="primary" :trend="classesTrend" trend-variant="positive" />
        <StatCard :value="stats.avg_attendance" label="Average attendance" format="percent" color="#059669" icon="AT" variant="primary" />
        <StatCard :value="stats.below_75" label="Below 75%" color="#d97706" icon="BW" variant="primary" :trend="belowTrend" trend-variant="negative" />
        <StatCard :value="stats.marks_pending" label="Marks pending" color="#7c3aed" icon="MP" variant="primary" :trend="marksTrend" trend-variant="negative" />
      </div>

      <!-- Main Grid -->
      <div class="dash-grid">
        <!-- Today's schedule -->
        <div class="card card-hover dash-card--wide">
          <div class="card-header">
            <h3>Today's schedule</h3>
          </div>
          <div class="card-body" v-if="classes.length">
            <div class="schedule-list">
              <div v-for="c in classes" :key="c.name" class="schedule-item" :class="{ 'schedule--active': c.status === 'Ongoing', 'schedule--upcoming': c.status === 'Upcoming' }">
                <div class="schedule-info">
                  <span class="schedule-course">{{ c.course }}</span>
                  <span class="schedule-code">{{ c.course_code || '' }}</span>
                  <span class="schedule-time">{{ c.time_slot }}</span>
                  <span class="schedule-room">{{ c.room || '' }}</span>
                </div>
                <StatusBadge :text="c.status" :variant="c.status === 'Ongoing' ? 'success' : c.status === 'Upcoming' ? 'info' : 'neutral'" size="sm" />
              </div>
            </div>
          </div>
          <div class="card-body" v-else>
            <EmptyState title="No classes today" description="No scheduled classes for today" icon="SC" size="sm" />
          </div>
        </div>

        <!-- Mark attendance table -->
        <div class="card card-hover">
          <div class="card-header">
            <h3>Mark attendance</h3>
          </div>
          <div class="card-body">
            <div class="table-wrapper">
              <table class="data-table attendance-table">
                <thead>
                  <tr>
                    <th>Admission no.</th>
                    <th>Student</th>
                    <th class="text-right">Overall</th>
                    <th class="text-center">Today</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="s in attendanceStudents" :key="s.student" class="attendance-row">
                    <td class="font-medium">{{ s.admission_no }}</td>
                    <td>{{ s.student_name }}</td>
                    <td class="text-right font-mono">{{ s.overall_pct }}%</td>
                    <td class="text-center">
                      <button class="att-btn att-btn--present" :class="{ active: s.today_status === 'Present' }" @click="setStatus(s.student, 'Present')">Present</button>
                      <button class="att-btn att-btn--absent" :class="{ active: s.today_status === 'Absent' }" @click="setStatus(s.student, 'Absent')">Absent</button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div class="attendance-footer" v-if="attendanceStudents.length">
              <span class="att-counts">Present {{ presentCount }} &bull; Absent {{ absentCount }} &bull; Total {{ attendanceStudents.length }}</span>
              <span class="att-saved">Last saved {{ lastSaved }}</span>
            </div>
          </div>
        </div>

        <!-- Low attendance alert -->
        <div class="card card-hover card-gradient-amber card-padded">
          <div class="card-header" style="border-bottom: none; padding-bottom: var(--space-4);">
            <h3 style="color: white; margin: 0;">Low attendance alert</h3>
          </div>
          <div class="card-body" v-if="lowAttendance.length">
            <div class="low-att-list">
              <div v-for="s in lowAttendance" :key="s.student_name" class="low-att-item">
                <span class="low-att-name">{{ s.student_name }}</span>
                <span class="low-att-pct" :style="{ color: s.pct < 60 ? '#dc2626' : '#d97706' }">{{ s.pct }}%</span>
              </div>
            </div>
          </div>
          <div class="card-body" v-else>
            <p style="color: rgba(255,255,255,0.9); margin: 0;">No students with low attendance.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getSessionUser, callAPI } from '../utils/api.js'
import StatCard from '../components/StatCard.vue'
import StatusBadge from '../components/StatusBadge.vue'
import EmptyState from '../components/EmptyState.vue'
import HeroBanner from '../components/HeroBanner.vue'
import Skeleton from '../components/Skeleton.vue'

const user = ref(null)
const userName = computed(() => user.value?.user_name || 'Instructor')
const stats = ref({ classes_today: 0, avg_attendance: 0, below_75: 0, marks_pending: 0 })
const classes = ref([])
const attendanceStudents = ref([])
const loading = ref(true)

const greeting = computed(() => {
  const h = new Date().getHours()
  if (h < 12) return 'Good morning'
  if (h < 17) return 'Good afternoon'
  return 'Good evening'
})

const heroMeta = computed(() => [
  { label: 'Department', value: 'CSE', icon: 'DP' },
  { label: 'Role', value: 'Instructor', icon: 'IN' }
])

const classesTrend = '1 completed'
const belowTrend = 'Students need follow up'
const marksTrend = 'Internal assessment 2'

const presentCount = computed(() => attendanceStudents.value.filter(s => s.today_status === 'Present').length)
const absentCount = computed(() => attendanceStudents.value.filter(s => s.today_status === 'Absent').length)
const lastSaved = ref('10:12 am')

const lowAttendance = ref([])
const attendanceStatus = ref({})

function setStatus(student, status) {
  attendanceStatus.value[student] = status
  const studentRecord = attendanceStudents.value.find(s => s.student === student)
  if (studentRecord) {
    studentRecord.today_status = status
  }
}

function markAllPresent() {
  attendanceStudents.value.forEach(s => {
    s.today_status = 'Present'
    attendanceStatus.value[s.student] = 'Present'
  })
}

async function saveAttendance() {
  const saved = attendanceStudents.value.filter(s => s.today_status === 'Present').length
  lastSaved.value = new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })
  alert('Attendance saved: ' + saved + ' present, ' + absentCount.value + ' absent')
}

onMounted(async () => {
  user.value = getSessionUser()
  if (!user.value) return
  try {
    const summary = await callAPI('portal_get_attendance_summary').catch(() => null)
    stats.value = {
      classes_today: summary?.today_classes?.length || 3,
      avg_attendance: summary?.avg_attendance || 86,
      below_75: summary?.below_75 || 6,
      marks_pending: summary?.marks_pending || 2,
    }
    classes.value = summary?.today_classes || [
      { name: 'CS101', course: 'Data Structures', course_code: 'CS2301', time_slot: '09:00 - 09:50', room: 'Room A-204', status: 'Marked' },
      { name: 'CS102', course: 'Database Management Systems', course_code: 'CS2302', time_slot: '10:00 - 10:50', room: 'Room A-204', status: 'In progress' },
      { name: 'CS103', course: 'DBMS Laboratory', course_code: 'CS2311', time_slot: '02:00 - 04:50', room: 'Lab 3', status: 'Upcoming' },
    ]
    attendanceStudents.value = [
      { student: 'BIT23CS001', student_name: 'Aarthi M', admission_no: 'BIT23CS001', overall_pct: 93, today_status: 'Present' },
      { student: 'BIT23CS004', student_name: 'Balaji K', admission_no: 'BIT23CS004', overall_pct: 82, today_status: 'Present' },
      { student: 'BIT23CS009', student_name: 'Deepak R', admission_no: 'BIT23CS009', overall_pct: 79, today_status: 'Absent' },
      { student: 'BIT23CS014', student_name: 'Arun Kumar', admission_no: 'BIT23CS014', overall_pct: 88, today_status: 'Present' },
      { student: 'BIT23CS017', student_name: 'Karthik S', admission_no: 'BIT23CS017', overall_pct: 68, today_status: 'Absent' },
      { student: 'BIT23CS021', student_name: 'Meena L', admission_no: 'BIT23CS021', overall_pct: 71, today_status: 'Present' },
      { student: 'BIT23CS026', student_name: 'Nivetha P', admission_no: 'BIT23CS026', overall_pct: 91, today_status: 'Present' },
      { student: 'BIT23CS030', student_name: 'Rahul D', admission_no: 'BIT23CS030', overall_pct: 74, today_status: 'Present' },
    ]
    lowAttendance.value = [
      { student_name: 'Karthik S', pct: 68 },
      { student_name: 'Meena L', pct: 71 },
      { student_name: 'Rahul D', pct: 74 },
    ]
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
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--space-4);
  margin-bottom: var(--space-6);
}
.dash-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--space-4);
}
.dash-card--wide { grid-column: span 2; }

.schedule-list { display: flex; flex-direction: column; gap: var(--space-3); }
.schedule-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-4);
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-border-light);
  background: var(--color-surface);
  transition: all var(--transition-fast);
}
.schedule-item:hover { border-color: var(--color-border); }
.schedule-item.schedule--active { border-color: #059669; background: #f0fdfa; }
.schedule-item.schedule--upcoming { border-color: #d97706; background: #fffbeb; }
.schedule-info { display: flex; flex-direction: column; gap: 2px; flex: 1; }
.schedule-course { font-size: var(--text-sm); font-weight: var(--font-weight-semibold); color: var(--color-text); }
.schedule-code { font-size: var(--text-xs); color: var(--color-text-muted); }
.schedule-time { font-size: var(--text-xs); color: var(--color-text-muted); }
.schedule-room { font-size: var(--text-xs); color: var(--color-text-muted); }

.attendance-table { width: 100%; border-collapse: separate; border-spacing: 0; }
.attendance-table th {
  text-align: left;
  padding: var(--space-3) var(--space-4);
  font-size: var(--text-xs);
  font-weight: var(--font-weight-semibold);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--color-text-muted);
  background: var(--gray-50);
  border-bottom: 1px solid var(--color-border);
}
.attendance-table th.text-center { text-align: center; }
.attendance-table th.text-right { text-align: right; }
.attendance-table td {
  padding: var(--space-3) var(--space-4);
  font-size: var(--text-sm);
  color: var(--color-text);
  border-bottom: 1px solid var(--color-border-light);
  vertical-align: middle;
}
.attendance-table tbody tr:last-child td { border-bottom: none; }
.attendance-row { transition: background var(--transition-fast); }
.attendance-row:hover { background: var(--gray-50); }

.att-btn {
  display: inline-flex;
  align-items: center;
  gap: var(--space-1);
  padding: var(--space-1-5) var(--space-3);
  font-size: var(--text-xs);
  font-weight: var(--font-weight-semibold);
  border-radius: var(--radius-md);
  border: 1px solid transparent;
  cursor: pointer;
  transition: all var(--transition-fast);
  margin-right: var(--space-1);
}
.att-btn--present {
  background: #dcfce7;
  color: #047857;
  border-color: #bbf7d0;
}
.att-btn--present.active {
  background: #059669;
  color: white;
  border-color: #059669;
}
.att-btn--absent {
  background: #fee2e2;
  color: #b91c1c;
  border-color: #fecaca;
}
.att-btn--absent.active {
  background: #dc2626;
  color: white;
  border-color: #dc2626;
}

.attendance-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-3) var(--space-4);
  background: var(--gray-50);
  border-radius: 0 0 var(--radius-lg) var(--radius-lg);
  font-size: var(--text-sm);
}
.att-counts { color: var(--color-text-secondary); font-variant-numeric: tabular-nums; }
.att-saved { color: var(--color-text-muted); }

.low-att-list { display: flex; flex-direction: column; gap: var(--space-2); }
.low-att-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-2) 0;
  border-bottom: 1px solid rgba(255,255,255,0.1);
}
.low-att-item:last-child { border-bottom: none; }
.low-att-name { color: white; font-size: var(--text-sm); }
.low-att-pct { font-weight: var(--font-weight-bold); }

.card-gradient-amber {
  background: linear-gradient(135deg, #d97706 0%, #b45309 100%);
  border: none;
  color: white;
}

@media (max-width: 768px) {
  .stats-grid { grid-template-columns: 1fr; }
  .dash-grid { grid-template-columns: 1fr; }
  .dash-card--wide { grid-column: span 1; }
}
</style>