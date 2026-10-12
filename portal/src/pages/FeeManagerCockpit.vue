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
        :subtitle="`${greeting} — Fee Manager Dashboard`"
        :meta-items="heroMeta"
        illustration="dashboard"
        variant="amber"
      >
        <template #actions>
          <a href="/app" class="btn btn-glass" target="_blank">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
            Open Full Desk
          </a>
        </template>
      </HeroBanner>

      <div class="stats-grid">
        <StatCard :value="stats.total_outstanding" label="Total Outstanding" format="currency" color="#d97706" icon="⚠️" variant="amber" :trend="outstandingTrend" trend-variant="negative" />
        <StatCard :value="stats.total_fee_records" label="Fee Records" color="#0f172a" icon="📋" variant="default" />
        <StatCard :value="stats.payments_today" label="Payments Today" format="currency" color="#059669" icon="💳" variant="success" :trend="paymentsTrend" trend-variant="positive" />
        <StatCard :value="stats.pending_discounts" label="Discounts Pending" color="#7c3aed" icon="🏷️" variant="purple" />
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
              empty-icon="✅"
            >
              <template #actions="{ item }">
                <a :href="`/app/fees/${item.feeId}`" target="_blank" class="btn btn-accent btn-sm">Collect</a>
              </template>
            </TimelineList>
          </div>
          <div class="card-body" v-else>
            <EmptyState title="All clear" description="No outstanding fees" icon="✅" size="sm" />
          </div>
        </div>

        <div class="card card-hover">
          <div class="card-header">
            <h3>Quick Actions</h3>
          </div>
          <div class="card-body">
            <div class="action-grid">
              <a href="/app/fee-payment/new" class="action-card" target="_blank">
                <div class="action-icon" style="background:rgba(5,150,105,0.1);color:#059669">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="1" x2="12" y2="23"></line><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path></svg>
                </div>
                <div class="action-content">
                  <span class="action-label">Record Payment</span>
                  <span class="action-desc">Record a fee payment</span>
                </div>
              </a>
              <a href="/app/fees" class="action-card" target="_blank">
                <div class="action-icon" style="background:rgba(30,64,175,0.1);color:#1e40af">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
                </div>
                <div class="action-content">
                  <span class="action-label">Fee Records</span>
                  <span class="action-desc">Manage all fee records</span>
                </div>
              </a>
              <a href="/app/fee-schedule" class="action-card" target="_blank">
                <div class="action-icon" style="background:rgba(124,58,237,0.1);color:#7c3aed">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>
                </div>
                <div class="action-content">
                  <span class="action-label">Fee Schedules</span>
                  <span class="action-desc">View and create schedules</span>
                </div>
              </a>
              <a href="/app/fee-discount" class="action-card" target="_blank">
                <div class="action-icon" style="background:rgba(220,38,38,0.1);color:#dc2626">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="16"></line><line x1="8" y1="12" x2="16" y2="12"></line></svg>
                </div>
                <div class="action-content">
                  <span class="action-label">Discount Approvals</span>
                  <span class="action-desc">Review pending discounts</span>
                </div>
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
              empty-icon="✅"
            >
              <template #actions="{ item }">
                <a :href="`/app/fees/${item.feeId}`" target="_blank" class="btn btn-accent btn-sm">Review</a>
              </template>
            </TimelineList>
          </div>
          <div class="card-body" v-else>
            <EmptyState title="No pending discounts" description="All discount requests are processed" icon="✅" size="sm" />
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
import StatCard from '../components/StatCard.vue'
import StatusBadge from '../components/StatusBadge.vue'
import EmptyState from '../components/EmptyState.vue'
import HeroBanner from '../components/HeroBanner.vue'
import ChartCard from '../components/ChartCard.vue'
import TimelineList from '../components/TimelineList.vue'
import Skeleton from '../components/Skeleton.vue'

const user = ref(null)
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
  { label: 'Role', value: 'Fee Manager', icon: '💰' }
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