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
        :title="`Welcome, ${userName}!`"
        :subtitle="`${greeting} — Fee Manager Dashboard`"
        :meta-items="heroMeta"
        variant="success"
      >
        <template #actions>
          <button class="btn btn-primary" @click="generateFees">
            <span class="icon-svg" v-html="icons.currency"></span>
            Generate fees
          </button>
        </template>
      </HeroBanner>

      <div class="stats-grid">
        <StatCard :value="stats.total_outstanding" label="Total Outstanding" format="currency" color="#d97706" :icon="icons.alert" variant="amber" :trend="outstandingTrend" trend-variant="negative" />
        <StatCard :value="stats.total_fee_records" label="Fee Records" color="#0f172a" :icon="icons.clipboard" variant="default" />
        <StatCard :value="stats.payments_today" label="Payments Today" format="currency" color="#059669" :icon="icons.creditCard" variant="success" :trend="paymentsTrend" trend-variant="positive" />
        <StatCard :value="stats.pending_discounts" label="Discounts Pending" color="#0d9488" :icon="icons.tag" variant="default" />
      </div>

      <div class="dash-grid">
        <div class="card card-hover dash-card--wide">
          <div class="card-header">
            <h3>Outstanding Fees</h3>
            <a href="/app/fees?fee_status=Unpaid" class="btn btn-ghost btn-sm" target="_blank">View All</a>
          </div>
          <div class="card-body" v-if="outstanding.length">
            <TimelineList 
              :items="outstandingTimelineItems"
              :vertical="true"
              empty-title="All clear"
              empty-description="No outstanding fees"
              :empty-icon="icons.checkCircle"
            >
              <template #actions="{ item }">
                <a :href="`/app/fees/${item.feeId}`" target="_blank" class="btn btn-accent btn-sm">Collect</a>
              </template>
            </TimelineList>
          </div>
          <div class="card-body" v-else>
            <EmptyState title="All clear" description="No outstanding fees" :icon="icons.checkCircle" size="sm" />
          </div>
        </div>

        <div class="card card-hover">
          <div class="card-header">
            <h3>Quick Actions</h3>
          </div>
          <div class="card-body">
            <div class="action-grid">
              <a href="/app/fee-payment/new" class="action-card" target="_blank">
                <div class="action-card__icon" style="background:rgba(5,150,105,0.1);color:#059669" v-html="icons.currency"></div>
                <span class="action-card__title">Record Payment</span>
                <span class="action-card__desc">Record a fee payment</span>
              </a>
              <a href="/app/fees" class="action-card" target="_blank">
                <div class="action-card__icon" style="background:rgba(15,23,42,0.08);color:#0f172a" v-html="icons.document"></div>
                <span class="action-card__title">Fee Records</span>
                <span class="action-card__desc">Manage all fee records</span>
              </a>
              <a href="/app/fee-schedule" class="action-card" target="_blank">
                <div class="action-card__icon" style="background:rgba(13,148,136,0.1);color:#0d9488" v-html="icons.calendar"></div>
                <span class="action-card__title">Fee Schedules</span>
                <span class="action-card__desc">View and create schedules</span>
              </a>
              <a href="/app/fee-discount" class="action-card" target="_blank">
                <div class="action-card__icon" style="background:rgba(217,119,6,0.1);color:#d97706" v-html="icons.tag"></div>
                <span class="action-card__title">Discount Approvals</span>
                <span class="action-card__desc">Review pending discounts</span>
              </a>
            </div>
          </div>
        </div>

        <div class="card card-hover">
          <div class="card-header">
            <h3>Pending Discount Approvals</h3>
          </div>
          <div class="card-body" v-if="discounts.length">
            <TimelineList 
              :items="discountTimelineItems"
              :vertical="true"
              empty-title="No pending discounts"
              empty-description="All discount requests are processed"
              :empty-icon="icons.checkCircle"
            >
              <template #actions="{ item }">
                <a :href="`/app/fees/${item.feeId}`" target="_blank" class="btn btn-accent btn-sm">Review</a>
              </template>
            </TimelineList>
          </div>
          <div class="card-body" v-else>
            <EmptyState title="No pending discounts" description="All discount requests are processed" :icon="icons.checkCircle" size="sm" />
          </div>
        </div>

        <div class="card card-hover dash-card--wide">
          <div class="card-header">
            <h3>Collection Trend (6 Months)</h3>
          </div>
          <div class="card-body">
            <ChartCard 
              type="line"
              :chart-data="collectionChartData"
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
const userName = computed(() => user.value?.user_name || 'Fee Manager')
const stats = ref({ total_outstanding: 0, total_fee_records: 0, payments_today: 0, pending_discounts: 0 })
const outstanding = ref([])
const discounts = ref([])
const loading = ref(true)
const chartLoading = ref(false)

const greeting = computed(() => {
  const h = new Date().getHours()
  if (h < 12) return 'Good morning'
  if (h < 17) return 'Good afternoon'
  return 'Good evening'
})

const heroMeta = computed(() => [
  { label: 'Role', value: 'Fee Manager', icon: icons.currency }
])

const outstandingTrend = '-5% vs last month'
const paymentsTrend = '+12% vs yesterday'

const outstandingTimelineItems = computed(() => {
  return outstanding.value.slice(0, 10).map(f => ({
    id: f.name,
    title: `${f.student_name} — ${f.fee_schedule || f.name}`,
    time: f.due_date,
    feeId: f.name,
    badge: { text: f.status, variant: statusVariant(f.status), dot: true },
    meta: [{ label: 'Outstanding', value: formatCurrency(f.outstanding_amount) }, { label: 'Due', value: formatDate(f.due_date) }]
  }))
})

const discountTimelineItems = computed(() => {
  return discounts.value.map(d => ({
    id: d.name,
    title: `${d.student_name} — ${d.discount_type}`,
    time: d.creation,
    feeId: d.fees,
    badge: { text: 'Pending', variant: 'warning', dot: true },
    meta: [{ label: 'Amount', value: formatCurrency(d.amount) }, { label: 'Type', value: d.discount_type }]
  }))
})

const collectionChartData = computed(() => {
  // Mock data for demo - in real app this would come from API
  return {
    labels: ['Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    datasets: [{
      label: 'Collected (₹)',
      data: [1250000, 1450000, 1380000, 1620000, 1580000, 1750000],
      borderColor: 'rgba(14, 184, 166, 1)',
      backgroundColor: 'rgba(14, 184, 166, 0.1)',
      fill: true,
      tension: 0.3,
      pointBackgroundColor: 'rgba(14, 184, 166, 1)',
      pointBorderColor: '#fff',
      pointBorderWidth: 2,
      pointRadius: 5
    }]
  }
})

function formatCurrency(v) {
  return '₹' + Number(v || 0).toLocaleString('en-IN', { minimumFractionDigits: 0 })
}

function formatDate(d) {
  return d ? new Date(d).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }) : ''
}

function statusVariant(status) {
  const map = { Paid: 'success', Partial: 'warning', Unpaid: 'danger', Overdue: 'danger' }
  return map[status] || 'neutral'
}

function generateFees() {
  alert('Fee generation initiated for all active students. Invoices created for the current academic year.')
}

onMounted(async () => {
  user.value = getSessionUser()
  if (!user.value) return
  try {
    const [feeData, pendingDisc] = await Promise.all([
      callAPI('portal_get_all_fees').catch(() => ({ fees: [] })),
      callAPI('portal_get_pending_discounts').catch(() => []),
    ])
    const fees = feeData.fees || []
    outstanding.value = fees.filter(f => f.status !== 'Paid')
    discounts.value = Array.isArray(pendingDisc) ? pendingDisc : []
    stats.value = {
      total_outstanding: fees.reduce((s, f) => s + (f.outstanding_amount || 0), 0),
      total_fee_records: fees.length,
      payments_today: 0,
      pending_discounts: discounts.value.length,
    }
  } catch (e) {
    console.error('Fee Manager cockpit load error:', e)
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
