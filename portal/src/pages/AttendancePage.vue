<template>
  <div class="attendance-page">
    <PageHeader title="Attendance" subtitle="Your attendance records and summary" />

    <div v-if="!data" class="loading-overlay"><div class="spinner spinner-lg"></div></div>

    <template v-else>
      <div class="summary-grid">
        <StatCard :value="data.percentage + '%'" label="ATTENDANCE RATE" color="#059669" icon="&#9776;" />
        <StatCard :value="data.total" label="TOTAL DAYS" color="#1e40af" icon="&#9719;" />
        <StatCard :value="data.summary?.Present || 0" label="PRESENT" color="#059669" icon="&#10003;" />
        <StatCard :value="data.summary?.Absent || 0" label="ABSENT" color="#dc2626" icon="&#10007;" />
      </div>

      <div class="card">
        <div class="card-header">
          <h3>Attendance Records</h3>
        </div>
        <div class="table-wrapper" v-if="data.records?.length">
          <table class="data-table">
            <thead>
              <tr>
                <th>Date</th>
                <th>Group</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="r in data.records" :key="r.name">
                <td>{{ formatDate(r.attendance_date) }}</td>
                <td>{{ r.student_group }}</td>
                <td>
                  <StatusBadge :text="r.status" :variant="attVariant(r.status)" dot />
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <EmptyState v-else title="No attendance records" description="Your attendance hasn't been recorded yet" icon="&#9776;" />
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { getSessionUser, callAPI } from '../utils/api.js'
import PageHeader from '../components/PageHeader.vue'
import StatCard from '../components/StatCard.vue'
import StatusBadge from '../components/StatusBadge.vue'
import EmptyState from '../components/EmptyState.vue'

const props = defineProps({ selectedChild: String })
const data = ref(null)

function formatDate(d) {
  return d ? new Date(d).toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric', year: 'numeric' }) : ''
}

function attVariant(status) {
  const map = { Present: 'success', Absent: 'danger', Late: 'warning', Excused: 'purple' }
  return map[status] || 'neutral'
}

async function load() {
  const user = getSessionUser()
  if (!user) return
  const student = user.role === 'Guardian' ? (props.selectedChild || undefined) : undefined
  data.value = await callAPI('portal_get_attendance', { student })
}

onMounted(load)
watch(() => props.selectedChild, load)
</script>

<style scoped>
.summary-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--space-4);
  margin-bottom: var(--space-6);
}
@media (max-width: 1024px) { .summary-grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 640px) { .summary-grid { grid-template-columns: 1fr; } }
</style>
