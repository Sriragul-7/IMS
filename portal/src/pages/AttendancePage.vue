<template>
  <div class="attendance-page">
    <PageHeader 
      title="Attendance" 
      subtitle="Your attendance records and summary"
      :meta-items="metaItems"
    />

    <div v-if="loading" class="page-loading">
      <div class="stats-skeleton" style="margin-bottom: var(--space-6);">
        <Skeleton type="stat" v-for="i in 4" :key="i" />
      </div>
      <Skeleton type="card" />
    </div>

    <template v-else>
      <!-- Summary Stats -->
      <div class="stats-grid" v-if="data">
        <StatCard :value="data.percentage" label="Attendance Rate" format="percent" color="#059669" :icon="icons.chart" variant="success" />
        <StatCard :value="data.total" label="Total Days" format="number" color="#0f172a" :icon="icons.calendar" variant="default" />
        <StatCard :value="data.summary?.Present || 0" label="Present" format="number" color="#059669" :icon="icons.check" variant="success" />
        <StatCard :value="data.summary?.Absent || 0" label="Absent" format="number" color="#dc2626" :icon="icons.x" variant="danger" />
      </div>

      <!-- Monthly Calendar Heatmap -->
      <div class="card card-hover" v-if="monthlyData">
        <div class="card-header">
          <h3>Monthly Attendance Heatmap</h3>
          <div class="heatmap-nav">
            <button class="btn btn-ghost btn-sm" @click="prevMonth" :disabled="isOldestMonth">Prev</button>
            <span class="heatmap-month">{{ currentMonthLabel }}</span>
            <button class="btn btn-ghost btn-sm" @click="nextMonth" :disabled="isCurrentMonth">Next</button>
          </div>
        </div>
        <div class="card-body">
          <div class="heatmap-container">
            <div class="heatmap-legend">
              <span class="legend-label">Less</span>
              <div class="legend-gradient">
                <div v-for="i in 5" :key="i" class="legend-color" :style="{ background: heatmapColors[i - 1] }"></div>
              </div>
              <span class="legend-label">More</span>
            </div>
            <div class="heatmap-grid" role="grid" aria-label="Attendance heatmap">
              <div class="heatmap-weekdays">
                <span v-for="d in weekdays" :key="d" class="weekday">{{ d }}</span>
              </div>
              <div class="heatmap-days">
                <div 
                  v-for="day in heatmapDays" 
                  :key="day.date || ('pad-' + day.day)" 
                  class="heatmap-day" 
                  :class="{ 'heatmap-day--empty': !day.inMonth, 'heatmap-day--today': day.isToday, 'heatmap-day--has-data': day.hasData }"
                  :style="{ background: day.color }"
                  :title="day.tooltip"
                  role="gridcell"
                  :aria-label="day.ariaLabel"
                >
                  <span class="day-number">{{ day.day }}</span>
                  <span v-if="day.hasData" class="day-indicator" :style="{ background: day.color }"></span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Attendance Records Table -->
      <div class="card card-hover">
        <div class="card-header">
          <h3>Attendance Records</h3>
        </div>
        <DataTable 
          v-if="data.records?.length"
          :columns="attendanceColumns"
          :data="data.records"
          :striped="true"
          :hover="true"
          :loading="false"
        >
          <template #cell(status)="{ row }">
            <StatusBadge :text="row.status" :variant="attVariant(row.status)" size="sm" dot />
          </template>
        </DataTable>
        <EmptyState v-else title="No attendance records" description="Your attendance hasn't been recorded yet" :icon="icons.calendar" size="md" />
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { getSessionUser, callAPI } from '../utils/api.js'
import { icons } from '../utils/icons.js'
import PageHeader from '../components/PageHeader.vue'
import StatCard from '../components/StatCard.vue'
import StatusBadge from '../components/StatusBadge.vue'
import EmptyState from '../components/EmptyState.vue'
import DataTable from '../components/DataTable.vue'
import Skeleton from '../components/Skeleton.vue'

const props = defineProps({ selectedChild: String })
const data = ref(null)
const monthlyData = ref(null)
const loading = ref(true)

const currentMonth = ref(new Date())
const currentMonthLabel = computed(() => currentMonth.value.toLocaleDateString('en-US', { month: 'long', year: 'numeric' }))
const isCurrentMonth = computed(() => {
  const now = new Date()
  return currentMonth.value.getMonth() === now.getMonth() && currentMonth.value.getFullYear() === now.getFullYear()
})
const isOldestMonth = computed(() => {
  const now = new Date()
  const oldest = new Date(now.getFullYear(), now.getMonth() - 12, 1)
  return currentMonth.value.getFullYear() === oldest.getFullYear() && currentMonth.value.getMonth() === oldest.getMonth()
})

const weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
const heatmapColors = ['rgba(15, 23, 42, 0.05)', 'rgba(5, 150, 105, 0.2)', 'rgba(5, 150, 105, 0.4)', 'rgba(5, 150, 105, 0.6)', 'rgba(5, 150, 105, 0.8)']

const heatmapDays = computed(() => {
  if (!monthlyData.value) return []
  const year = currentMonth.value.getFullYear()
  const month = currentMonth.value.getMonth()
  const firstDay = new Date(year, month, 1)
  const lastDay = new Date(year, month + 1, 0)
  const startDay = firstDay.getDay() === 0 ? 6 : firstDay.getDay() - 1 // Monday = 0
  const daysInMonth = lastDay.getDate()
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  
  const days = []
  const recordsMap = new Map()
  if (monthlyData.value.records) {
    monthlyData.value.records.forEach(r => {
      const date = new Date(r.attendance_date)
      if (date.getMonth() === month && date.getFullYear() === year) {
        recordsMap.set(date.getDate(), r.status)
      }
    })
  }
  
  // Previous month days
  const prevMonthLastDay = new Date(year, month, 0).getDate()
  for (let i = startDay - 1; i >= 0; i--) {
    const day = prevMonthLastDay - i
    days.push({ date: '', day, inMonth: false, isToday: false, hasData: false, color: 'transparent', tooltip: '', ariaLabel: '' })
  }
  
  // Current month days
  for (let d = 1; d <= daysInMonth; d++) {
    const date = new Date(year, month, d)
    const status = recordsMap.get(d)
    const isToday = date.getTime() === today.getTime()
    let color = heatmapColors[0]
    let hasData = false
    let tooltip = `${date.toLocaleDateString('en-US', { weekday: 'long', month: 'short', day: 'numeric' })}`
    
    if (status) {
      hasData = true
      const statusColors = { Present: heatmapColors[4], Absent: 'rgba(220, 38, 38, 0.6)', Late: 'rgba(217, 119, 6, 0.6)', Excused: 'rgba(124, 58, 237, 0.6)' }
      color = statusColors[status] || heatmapColors[2]
      tooltip += ` - ${status}`
    }
    
    days.push({ 
      date: date.toISOString().split('T')[0], 
      day: d, 
      inMonth: true, 
      isToday, 
      hasData, 
      color, 
      tooltip,
      ariaLabel: tooltip
    })
  }
  
  // Next month days to fill grid
  const totalCells = Math.ceil(days.length / 7) * 7
  const nextMonthDays = totalCells - days.length
  for (let d = 1; d <= nextMonthDays; d++) {
    days.push({ date: '', day: d, inMonth: false, isToday: false, hasData: false, color: 'transparent', tooltip: '', ariaLabel: '' })
  }
  
  return days
})

function prevMonth() {
  if (isOldestMonth.value) return
  currentMonth.value = new Date(currentMonth.value.getFullYear(), currentMonth.value.getMonth() - 1, 1)
  loadMonthlyData()
}
function nextMonth() {
  if (isCurrentMonth.value) return
  currentMonth.value = new Date(currentMonth.value.getFullYear(), currentMonth.value.getMonth() + 1, 1)
  loadMonthlyData()
}

const metaItems = computed(() => [
  { label: 'Current Month', value: currentMonthLabel.value, icon: icons.calendar }
])

const attendanceColumns = [
  { key: 'attendance_date', label: 'Date', format: (v) => v ? new Date(v).toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric', year: 'numeric' }) : '—' },
  { key: 'student_group', label: 'Group' },
  { key: 'status', label: 'Status' }
]

function attVariant(status) {
  const map = { Present: 'success', Absent: 'danger', Late: 'warning', Excused: 'purple' }
  return map[status] || 'neutral'
}

async function load() {
  loading.value = true
  const user = getSessionUser()
  if (!user) { loading.value = false; return }
  const student = user.role === 'Guardian' ? (props.selectedChild || undefined) : undefined
  try {
    const [att, monthly] = await Promise.all([
      callAPI('portal_get_attendance', { student }),
      callAPI('portal_get_attendance_monthly', { student, month: currentMonth.value.getMonth() + 1, year: currentMonth.value.getFullYear() }).catch(() => null)
    ])
    data.value = att
    monthlyData.value = monthly || { records: [] }
  } catch (e) {
    console.error('Attendance load error:', e)
  } finally {
    loading.value = false
  }
}

async function loadMonthlyData() {
  const user = getSessionUser()
  if (!user) return
  const student = user.role === 'Guardian' ? (props.selectedChild || undefined) : undefined
  try {
    monthlyData.value = await callAPI('portal_get_attendance_monthly', { student, month: currentMonth.value.getMonth() + 1, year: currentMonth.value.getFullYear() }) || { records: [] }
  } catch (e) {
    monthlyData.value = { records: [] }
  }
}

onMounted(load)
watch(() => props.selectedChild, load)
</script>

<style scoped>
.attendance-page { animation: fadeIn var(--transition-base); }
.page-loading { padding: var(--space-6); }
.stats-skeleton { display: grid; grid-template-columns: repeat(4, 1fr); gap: var(--space-4); }

.heatmap-nav { display: flex; align-items: center; gap: var(--space-2); }
.heatmap-month { font-weight: var(--font-weight-semibold); color: var(--color-text); min-width: 140px; text-align: center; }

.heatmap-container { overflow-x: auto; }
.heatmap-legend { display: flex; align-items: center; gap: var(--space-3); margin-bottom: var(--space-4); font-size: var(--text-xs); color: var(--color-text-muted); }
.legend-gradient { display: flex; gap: 2px; }
.legend-color { width: 24px; height: 8px; border-radius: var(--radius-sm); }

.heatmap-grid { display: flex; flex-direction: column; gap: 4px; }
.heatmap-weekdays { display: grid; grid-template-columns: repeat(7, 1fr); gap: 4px; margin-bottom: 4px; }
.weekday { text-align: center; font-size: var(--text-xs); font-weight: var(--font-weight-semibold); color: var(--color-text-muted); text-transform: uppercase; }
.heatmap-days { display: grid; grid-template-columns: repeat(7, 1fr); gap: 4px; }
.heatmap-day { aspect-ratio: 1; border-radius: var(--radius-sm); display: flex; flex-direction: column; align-items: center; justify-content: center; font-size: var(--text-xs); font-weight: var(--font-weight-medium); color: var(--color-text); position: relative; transition: transform var(--transition-fast); cursor: default; }
.heatmap-day:hover { transform: scale(1.1); z-index: 1; box-shadow: var(--shadow-md); }
.heatmap-day--empty { color: var(--color-text-muted); }
.heatmap-day--today { outline: 2px solid var(--color-accent); outline-offset: -2px; }
.heatmap-day--has-data { color: white; text-shadow: 0 1px 2px rgba(0,0,0,0.3); }
.day-number { line-height: 1; }
.day-indicator { width: 6px; height: 6px; border-radius: 50%; margin-top: 2px; opacity: 0.8; }

@media (max-width: 640px) {
  .heatmap-day { font-size: 10px; }
  .weekday { font-size: 9px; }
}
</style>
