<template>
  <div class="fees-page">
    <PageHeader 
      title="Fees" 
      subtitle="Fee records and payment history"
      :meta-items="metaItems"
    />

    <div v-if="loading" class="page-loading">
      <div class="stats-skeleton" style="margin-bottom: var(--space-6);">
        <Skeleton type="stat" v-for="i in 3" :key="i" />
      </div>
      <Skeleton type="card" />
      <Skeleton type="card" style="margin-top: var(--space-4);" />
    </div>

    <template v-else>
      <!-- Summary Stats -->
      <div class="stats-grid" v-if="fees.length">
        <StatCard :value="totalFees" label="Total Fees" format="currency" color="#0f172a" icon="💰" variant="default" />
        <StatCard :value="totalPaid" label="Paid" format="currency" color="#059669" icon="✅" variant="success" :trend="paidTrend" trend-variant="positive" />
        <StatCard :value="totalOutstanding" label="Outstanding" format="currency" color="#d97706" icon="⚠️" variant="amber" />
      </div>

      <!-- Fee Records Table -->
      <div class="card card-hover">
        <div class="card-header">
          <h3>Fee Records</h3>
        </div>
        <DataTable 
          v-if="fees.length"
          :columns="feeColumns"
          :data="fees"
          :striped="true"
          :hover="true"
          :loading="false"
        >
          <template #cell(due_date)="{ row }">
            <span :class="{ overdue: isOverdue(row.due_date) && row.status !== 'Paid' }">{{ formatDate(row.due_date) }}</span>
          </template>
          <template #cell(total_amount)="{ row }">
            <span class="font-mono">{{ formatCurrency(row.total_amount) }}</span>
          </template>
          <template #cell(paid_amount)="{ row }">
            <span class="font-mono text-success">{{ formatCurrency(row.paid_amount) }}</span>
          </template>
          <template #cell(outstanding_amount)="{ row }">
            <span class="font-mono" :class="{ 'text-danger': row.outstanding_amount > 0 }">{{ formatCurrency(row.outstanding_amount) }}</span>
          </template>
          <template #cell(status)="{ row }">
            <StatusBadge :text="row.status" :variant="feeVariant(row.status)" size="sm" />
          </template>
        </DataTable>
        <EmptyState v-else title="No fee records" description="No fees have been assigned to you yet" icon="💰" size="md" />
      </div>

      <!-- Payment History -->
      <div class="card card-hover" v-if="payments.length" style="margin-top: var(--space-4)">
        <div class="card-header">
          <h3>Payment History</h3>
        </div>
        <DataTable 
          :columns="paymentColumns"
          :data="payments"
          :striped="true"
          :hover="true"
          :loading="false"
        >
          <template #cell(amount)="{ row }">
            <span class="font-mono text-success">{{ formatCurrency(row.amount) }}</span>
          </template>
          <template #cell(payment_date)="{ row }">
            {{ formatDate(row.payment_date) }}
          </template>
        </DataTable>
      </div>

      <!-- Fee Payment Timeline (Visual) -->
      <div class="card card-hover" v-if="payments.length" style="margin-top: var(--space-4)">
        <div class="card-header">
          <h3>Payment Timeline</h3>
        </div>
        <div class="card-body">
          <TimelineList 
            :items="paymentTimelineItems"
            :vertical="true"
            empty-title="No payments"
            empty-description="No payment history available"
            empty-icon="💳"
          />
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { getSessionUser, callAPI } from '../utils/api.js'
import PageHeader from '../components/PageHeader.vue'
import StatCard from '../components/StatCard.vue'
import StatusBadge from '../components/StatusBadge.vue'
import EmptyState from '../components/EmptyState.vue'
import DataTable from '../components/DataTable.vue'
import TimelineList from '../components/TimelineList.vue'
import Skeleton from '../components/Skeleton.vue'

const props = defineProps({ selectedChild: String })
const fees = ref([])
const payments = ref([])
const loading = ref(true)

const totalFees = computed(() => fees.value.reduce((s, f) => s + (f.total_amount || 0), 0))
const totalPaid = computed(() => fees.value.reduce((s, f) => s + (f.paid_amount || 0), 0))
const totalOutstanding = computed(() => fees.value.reduce((s, f) => s + (f.outstanding_amount || 0), 0))
const paidTrend = '+12% vs last term'

const metaItems = computed(() => [
  { label: 'Outstanding', value: formatCurrency(totalOutstanding.value), icon: '⚠️' }
])

const feeColumns = [
  { key: 'fee_schedule', label: 'Fee Schedule', format: (v, row) => row.fee_schedule || row.name },
  { key: 'academic_year', label: 'Academic Year' },
  { key: 'due_date', label: 'Due Date' },
  { key: 'total_amount', label: 'Total', align: 'right' },
  { key: 'paid_amount', label: 'Paid', align: 'right' },
  { key: 'outstanding_amount', label: 'Outstanding', align: 'right' },
  { key: 'status', label: 'Status' }
]

const paymentColumns = [
  { key: 'payment_date', label: 'Date' },
  { key: 'amount', label: 'Amount', align: 'right' },
  { key: 'payment_mode', label: 'Method' },
  { key: 'reference_number', label: 'Reference' }
]

const paymentTimelineItems = computed(() => {
  return payments.value.slice().reverse().map(p => ({
    id: p.name,
    title: `Payment of ${formatCurrency(p.amount)} via ${p.payment_mode}`,
    time: p.payment_date,
    badge: { text: 'Completed', variant: 'success', dot: true },
    meta: p.reference_number ? [{ label: 'Ref', value: p.reference_number }] : []
  }))
})

function formatCurrency(v) {
  return '₹' + Number(v || 0).toLocaleString('en-IN', { minimumFractionDigits: 0 })
}

function formatDate(d) {
  return d ? new Date(d).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }) : ''
}

function isOverdue(dueDate) {
  if (!dueDate) return false
  return new Date(dueDate) < new Date()
}

function feeVariant(status) {
  const map = { Paid: 'success', Partial: 'warning', Unpaid: 'danger', Overdue: 'danger' }
  return map[status] || 'neutral'
}

async function load() {
  loading.value = true
  const user = getSessionUser()
  if (!user) { loading.value = false; return }
  const student = user.role === 'Guardian' ? (props.selectedChild || undefined) : undefined
  try {
    const result = await callAPI('portal_get_fees', { student })
    fees.value = result.fees || []
    payments.value = result.payments || []
  } catch (e) {
    console.error('Fees load error:', e)
  } finally {
    loading.value = false
  }
}

onMounted(load)
watch(() => props.selectedChild, load)
</script>

<style scoped>
.fees-page { animation: fadeIn var(--transition-base); }
.page-loading { padding: var(--space-6); }
.stats-skeleton { display: grid; grid-template-columns: repeat(3, 1fr); gap: var(--space-4); }

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-4);
  margin-bottom: var(--space-6);
}

.text-success { color: var(--color-success); }
.text-danger { color: var(--color-danger); font-weight: var(--font-weight-semibold); }
.font-mono { font-family: var(--font-family-mono); font-variant-numeric: tabular-nums; }
.overdue { color: var(--color-danger); font-weight: var(--font-weight-semibold); }

@media (max-width: 768px) {
  .stats-grid { grid-template-columns: 1fr; }
}
</style>