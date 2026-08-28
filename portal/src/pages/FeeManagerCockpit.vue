<template>
  <div class="cockpit">
    <div v-if="loading" class="loading-overlay">
      <div class="spinner spinner-lg"></div>
    </div>

    <template v-else>
      <div class="welcome-banner fee-banner">
        <div>
          <h2>Welcome, {{ user?.user_name }}!</h2>
          <p>{{ greeting }} — Fee Manager Dashboard</p>
        </div>
        <a href="/app" class="btn btn-glass" target="_blank">Open Full Admin &#8599;</a>
      </div>

      <div class="stats-grid">
        <StatCard :value="formatCurrency(stats.total_outstanding)" label="TOTAL OUTSTANDING" color="#d97706" icon="&#9888;" />
        <StatCard :value="stats.total_fee_records" label="FEE RECORDS" color="#1e40af" icon="&#128179;" />
        <StatCard :value="stats.payments_today" label="PAYMENTS TODAY" color="#059669" icon="&#10003;" />
        <StatCard :value="stats.pending_discounts" label="DISCOUNTS PENDING" color="#7c3aed" icon="&#9733;" />
      </div>

      <div class="dash-grid">
        <div class="card">
          <div class="card-header">
            <h3>Outstanding Fees</h3>
            <a href="/app/fees?fee_status=Unpaid" class="btn btn-ghost btn-sm" target="_blank">View All</a>
          </div>
          <div class="card-body" v-if="outstanding.length">
            <div v-for="f in outstanding.slice(0, 6)" :key="f.name" class="fee-row">
              <div class="fee-info">
                <span class="fee-student">{{ f.student_name }}</span>
                <span class="fee-schedule">{{ f.fee_schedule || f.name }}</span>
              </div>
              <div class="fee-right">
                <span class="fee-amount">{{ formatCurrency(f.outstanding_amount) }}</span>
                <StatusBadge :text="f.status" :variant="statusVariant(f.status)" />
              </div>
            </div>
          </div>
          <div class="card-body" v-else>
            <EmptyState title="All clear" description="No outstanding fees" icon="&#10003;" />
          </div>
        </div>

        <div class="card">
          <div class="card-header">
            <h3>Quick Actions</h3>
          </div>
          <div class="card-body">
            <div class="action-list">
              <a href="/app/fee-payment/new" class="action-item" target="_blank">
                <span class="action-icon" style="background:rgba(5,150,105,0.1);color:#059669">&#128179;</span>
                <div class="action-text">
                  <span class="action-label">Record Payment</span>
                  <span class="action-desc">Record a fee payment</span>
                </div>
              </a>
              <a href="/app/fees" class="action-item" target="_blank">
                <span class="action-icon" style="background:rgba(30,64,175,0.1);color:#1e40af">&#128203;</span>
                <div class="action-text">
                  <span class="action-label">Fee Records</span>
                  <span class="action-desc">Manage all fee records</span>
                </div>
              </a>
              <a href="/app/fee-schedule" class="action-item" target="_blank">
                <span class="action-icon" style="background:rgba(124,58,237,0.1);color:#7c3aed">&#128197;</span>
                <div class="action-text">
                  <span class="action-label">Fee Schedules</span>
                  <span class="action-desc">View and create fee schedules</span>
                </div>
              </a>
            </div>
          </div>
        </div>

        <div class="card">
          <div class="card-header">
            <h3>Pending Discount Approvals</h3>
          </div>
          <div class="card-body" v-if="discounts.length">
            <div v-for="d in discounts" :key="d.name" class="pending-row">
              <div class="pending-info">
                <span class="pending-name">{{ d.student_name }}</span>
                <span class="pending-date">{{ d.discount_type }} — {{ formatCurrency(d.amount) }}</span>
              </div>
              <a :href="`/app/fees/${d.fees}`" class="btn btn-sm btn-outline" target="_blank">Review</a>
            </div>
          </div>
          <div class="card-body" v-else>
            <EmptyState title="No pending discounts" description="All discount requests are processed" icon="&#10003;" />
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
const stats = ref({ total_outstanding: 0, total_fee_records: 0, payments_today: 0, pending_discounts: 0 })
const outstanding = ref([])
const discounts = ref([])
const loading = ref(true)

const greeting = computed(() => {
  const h = new Date().getHours()
  if (h < 12) return 'Good morning'
  if (h < 17) return 'Good afternoon'
  return 'Good evening'
})

function formatCurrency(v) {
  return '\u20b9' + Number(v || 0).toLocaleString('en-IN', { minimumFractionDigits: 0 })
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
.welcome-banner {
  background: linear-gradient(135deg, #d97706 0%, #b45309 100%);
  color: white;
  padding: var(--space-6) var(--space-8);
  border-radius: var(--radius-xl);
  margin-bottom: var(--space-6);
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.welcome-banner h2 { font-size: var(--text-2xl); font-weight: 700; margin-bottom: var(--space-1); }
.welcome-banner p { font-size: var(--text-sm); opacity: 0.85; }

.btn-glass {
  padding: var(--space-2) var(--space-4);
  border-radius: var(--radius-md);
  background: rgba(255,255,255,0.15);
  color: white;
  font-size: var(--text-sm);
  font-weight: 600;
  text-decoration: none;
  transition: all var(--transition-fast);
  white-space: nowrap;
}
.btn-glass:hover { background: rgba(255,255,255,0.25); }

.stats-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: var(--space-4); margin-bottom: var(--space-6); }
.dash-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: var(--space-4); }

.fee-row { display: flex; align-items: center; justify-content: space-between; padding: var(--space-3) 0; border-bottom: 1px solid var(--color-border-light); }
.fee-row:last-child { border-bottom: none; }
.fee-info { flex: 1; min-width: 0; }
.fee-student { display: block; font-size: var(--text-sm); font-weight: 600; color: var(--color-text); }
.fee-schedule { font-size: var(--text-xs); color: var(--color-text-muted); }
.fee-right { display: flex; align-items: center; gap: var(--space-3); }
.fee-amount { font-size: var(--text-sm); font-weight: 600; white-space: nowrap; }

.action-list { display: flex; flex-direction: column; gap: var(--space-2); }
.action-item { display: flex; align-items: center; gap: var(--space-3); padding: var(--space-3); border-radius: var(--radius-md); border: 1px solid var(--color-border-light); text-decoration: none; transition: all var(--transition-fast); }
.action-item:hover { border-color: var(--color-primary-light); background: var(--color-primary-50); }
.action-icon { width: 36px; height: 36px; border-radius: var(--radius-md); display: flex; align-items: center; justify-content: center; font-size: 16px; flex-shrink: 0; }
.action-text { flex: 1; }
.action-label { display: block; font-size: var(--text-sm); font-weight: 600; color: var(--color-text); }
.action-desc { font-size: var(--text-xs); color: var(--color-text-muted); }

.pending-row { display: flex; align-items: center; justify-content: space-between; padding: var(--space-3) 0; border-bottom: 1px solid var(--color-border-light); }
.pending-row:last-child { border-bottom: none; }
.pending-info { flex: 1; min-width: 0; }
.pending-name { display: block; font-size: var(--text-sm); font-weight: 500; }
.pending-date { font-size: var(--text-xs); color: var(--color-text-muted); }

.btn-outline { padding: var(--space-1) var(--space-3); border: 1px solid var(--color-border); border-radius: var(--radius-sm); background: transparent; color: var(--color-primary); font-size: var(--text-xs); font-weight: 600; text-decoration: none; cursor: pointer; }
.btn-outline:hover { background: var(--color-primary-50); }

@media (max-width: 1024px) { .stats-grid { grid-template-columns: repeat(2, 1fr); } .dash-grid { grid-template-columns: 1fr; } }
@media (max-width: 640px) { .stats-grid { grid-template-columns: 1fr; } .welcome-banner { flex-direction: column; gap: var(--space-3); } }
</style>
