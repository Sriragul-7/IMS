<template>
  <div class="fees-page">
    <PageHeader title="Fees" subtitle="Fee records and payment history" />

    <div v-if="!loaded" class="loading-overlay"><div class="spinner spinner-lg"></div></div>

    <template v-else>
      <div class="summary-grid" v-if="fees.length">
        <StatCard :value="formatCurrency(totalFees)" label="TOTAL FEES" color="#1e40af" icon="&#9830;" />
        <StatCard :value="formatCurrency(totalPaid)" label="PAID" color="#059669" icon="&#10003;" />
        <StatCard :value="formatCurrency(totalOutstanding)" label="OUTSTANDING" color="#d97706" icon="&#9888;" />
      </div>

      <div class="card">
        <div class="card-header"><h3>Fee Records</h3></div>
        <div class="table-wrapper" v-if="fees.length">
          <table class="data-table">
            <thead>
              <tr>
                <th>Fee Schedule</th>
                <th>Academic Year</th>
                <th>Due Date</th>
                <th class="text-right">Total</th>
                <th class="text-right">Paid</th>
                <th class="text-right">Outstanding</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="f in fees" :key="f.name">
                <td class="font-medium">{{ f.fee_schedule || f.name }}</td>
                <td>{{ f.academic_year }}</td>
                <td>{{ formatDate(f.due_date) }}</td>
                <td class="text-right">{{ formatCurrency(f.total_amount) }}</td>
                <td class="text-right">{{ formatCurrency(f.paid_amount) }}</td>
                <td class="text-right" :class="{ 'text-danger': f.outstanding_amount > 0 }">
                  {{ formatCurrency(f.outstanding_amount) }}
                </td>
                <td>
                  <StatusBadge :text="f.status" :variant="feeVariant(f.status)" />
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <EmptyState v-else title="No fee records" description="No fees have been assigned to you yet" icon="&#9830;" />
      </div>

      <div class="card" v-if="payments.length" style="margin-top: var(--space-4)">
        <div class="card-header"><h3>Payment History</h3></div>
        <div class="table-wrapper">
          <table class="data-table">
            <thead>
              <tr>
                <th>Date</th>
                <th class="text-right">Amount</th>
                <th>Method</th>
                <th>Reference</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="p in payments" :key="p.name">
                <td>{{ formatDate(p.payment_date) }}</td>
                <td class="text-right font-medium">{{ formatCurrency(p.amount) }}</td>
                <td>{{ p.payment_mode }}</td>
                <td class="text-muted">{{ p.reference_number || '\u2014' }}</td>
              </tr>
            </tbody>
          </table>
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

const props = defineProps({ selectedChild: String })
const fees = ref([])
const payments = ref([])
const loaded = ref(false)

const totalFees = computed(() => fees.value.reduce((s, f) => s + (f.total_amount || 0), 0))
const totalPaid = computed(() => fees.value.reduce((s, f) => s + (f.paid_amount || 0), 0))
const totalOutstanding = computed(() => fees.value.reduce((s, f) => s + (f.outstanding_amount || 0), 0))

function formatCurrency(v) {
  return '\u20b9' + Number(v || 0).toLocaleString('en-IN', { minimumFractionDigits: 0 })
}

function formatDate(d) {
  return d ? new Date(d).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }) : ''
}

function feeVariant(status) {
  const map = { Paid: 'success', Partial: 'warning', Unpaid: 'danger', Overdue: 'danger' }
  return map[status] || 'neutral'
}

async function load() {
  const user = getSessionUser()
  if (!user) return
  const student = user.role === 'Guardian' ? (props.selectedChild || undefined) : undefined
  const result = await callAPI('portal_get_fees', { student })
  fees.value = result.fees || []
  payments.value = result.payments || []
  loaded.value = true
}

onMounted(load)
watch(() => props.selectedChild, load)
</script>

<style scoped>
.summary-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-4);
  margin-bottom: var(--space-6);
}
.text-right { text-align: right; }
.text-danger { color: var(--color-danger); font-weight: 600; }
.text-muted { color: var(--color-text-muted); }
@media (max-width: 768px) { .summary-grid { grid-template-columns: 1fr; } }
</style>
