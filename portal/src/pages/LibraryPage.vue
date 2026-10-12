<template>
  <div class="library-page">
    <PageHeader 
      title="Library" 
      subtitle="Book issues, returns, and transaction history"
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
      <div class="stats-grid" v-if="stats">
        <StatCard :value="stats.active" label="Checked Out" color="#d97706" icon="📖" variant="amber" />
        <StatCard :value="stats.overdue" label="Overdue" color="#dc2626" icon="⚠️" variant="danger" />
        <StatCard :value="stats.total_transactions" label="Total Transactions" color="#0f172a" icon="📋" variant="default" />
      </div>

      <!-- Currently Checked Out -->
      <div class="card card-hover" v-if="activeItems.length" style="margin-bottom: var(--space-4)">
        <div class="card-header">
          <h3>Currently Checked Out</h3>
          <StatusBadge v-if="overdueCount > 0" :text="`${overdueCount} Overdue`" variant="danger" size="sm" dot />
        </div>
        <div class="card-body">
          <div class="active-grid">
            <div v-for="item in activeItems" :key="item.name" class="active-card" :class="{ overdue: isOverdue(item.due_date) }">
              <div class="active-header">
                <div class="book-icon">📖</div>
                <StatusBadge :text="isOverdue(item.due_date) ? 'Overdue' : 'Active'" :variant="isOverdue(item.due_date) ? 'danger' : 'success'" size="sm" dot />
              </div>
              <div class="book-title">{{ item.library_item_name || item.library_item }}</div>
              <div class="book-meta">
                <div class="meta-row">
                  <span class="meta-label">Issued</span>
                  <span>{{ formatDate(item.transaction_date) }}</span>
                </div>
                <div class="meta-row">
                  <span class="meta-label">Due</span>
                  <span :class="{ 'text-danger': isOverdue(item.due_date), 'text-bold': isOverdue(item.due_date) }">
                    {{ formatDate(item.due_date) }}
                    <span v-if="isOverdue(item.due_date)" class="overdue-badge">Overdue by {{ daysOverdue(item.due_date) }} day(s)</span>
                  </span>
                </div>
              </div>
              <div class="book-progress" v-if="item.due_date">
                <div class="progress-bar">
                  <div class="progress-fill" :style="{ width: dueProgress(item.due_date) + '%', background: isOverdue(item.due_date) ? 'var(--color-danger)' : 'var(--color-warning)' }"></div>
                </div>
                <span class="progress-text">{{ dueProgress(item.due_date) }}% through loan period</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Transaction History -->
      <div class="card card-hover">
        <div class="card-header">
          <h3>Transaction History</h3>
        </div>
        <DataTable 
          v-if="transactions.length"
          :columns="transactionColumns"
          :data="transactions"
          :striped="true"
          :hover="true"
          :loading="false"
        >
          <template #cell(status)="{ row }">
            <StatusBadge :text="row.status === 'Issue' ? 'Checked Out' : 'Returned'" :variant="row.status === 'Issue' ? 'warning' : 'success'" size="sm" />
          </template>
          <template #cell(fine_amount)="{ row }">
            <span v-if="row.fine_amount > 0" class="text-danger font-mono">{{ formatCurrency(row.fine_amount) }}</span>
            <span v-else class="text-muted">—</span>
          </template>
        </DataTable>
        <EmptyState v-else title="No transactions" description="No library transactions found" icon="📚" size="md" />
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
import Skeleton from '../components/Skeleton.vue'

const props = defineProps({ selectedChild: String })
const activeItems = ref([])
const transactions = ref([])
const loading = ref(true)

const stats = computed(() => ({
  active: activeItems.value.length,
  overdue: activeItems.value.filter(isOverdue).length,
  total_transactions: transactions.value.length
}))

const overdueCount = computed(() => activeItems.value.filter(isOverdue).length)

const metaItems = computed(() => [
  { label: 'Active', value: stats.value.active, icon: '📖' },
  { label: 'Overdue', value: stats.value.overdue, icon: '⚠️' }
])

const transactionColumns = [
  { key: 'library_item_name', label: 'Item', format: (v, row) => row.library_item_name || row.library_item },
  { key: 'transaction_date', label: 'Date', format: (v) => v ? new Date(v).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }) : '—' },
  { key: 'due_date', label: 'Due Date', format: (v) => v ? new Date(v).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }) : '—' },
  { key: 'status', label: 'Status' },
  { key: 'fine_amount', label: 'Fine', align: 'right' }
]

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

function daysOverdue(dueDate) {
  if (!dueDate) return 0
  const diff = new Date() - new Date(dueDate)
  return Math.ceil(diff / (1000 * 60 * 60 * 24))
}

function dueProgress(dueDate) {
  if (!dueDate) return 0
  const issueDate = new Date()
  // Find the issue date from active items - simplified for now
  const totalDays = 14 // Standard loan period
  const daysPassed = totalDays - daysOverdue(dueDate)
  return Math.max(0, Math.min(100, Math.round((daysPassed / totalDays) * 100)))
}

async function load() {
  loading.value = true
  const user = getSessionUser()
  if (!user) { loading.value = false; return }
  const student = user.role === 'Guardian' ? (props.selectedChild || undefined) : undefined
  try {
    const result = await callAPI('portal_get_library', { student })
    activeItems.value = result.active_items || []
    transactions.value = result.transactions || []
  } catch (e) {
    console.error('Library load error:', e)
  } finally {
    loading.value = false
  }
}

onMounted(load)
watch(() => props.selectedChild, load)
</script>

<style scoped>
.library-page { animation: fadeIn var(--transition-base); }
.page-loading { padding: var(--space-6); }
.stats-skeleton { display: grid; grid-template-columns: repeat(3, 1fr); gap: var(--space-4); }

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-4);
  margin-bottom: var(--space-6);
}

.active-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: var(--space-4);
}

.active-card {
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  padding: var(--space-5);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--color-border-light);
  border-left: 4px solid var(--color-warning);
  transition: all var(--transition-base);
}
.active-card:hover { box-shadow: var(--shadow-md); transform: translateY(-2px); }
.active-card.overdue { border-left-color: var(--color-danger); }

.active-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-3);
}
.book-icon { font-size: 1.5rem; }

.book-title {
  font-size: var(--text-md);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text);
  margin-bottom: var(--space-3);
}

.book-meta {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  margin-bottom: var(--space-3);
}
.meta-row {
  display: flex;
  justify-content: space-between;
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
}
.meta-label { color: var(--color-text-muted); }
.text-bold { font-weight: var(--font-weight-semibold); }
.text-danger { color: var(--color-danger); }
.overdue-badge {
  display: inline-block;
  margin-left: var(--space-2);
  padding: 2px var(--space-2);
  font-size: 10px;
  font-weight: var(--font-weight-semibold);
  color: white;
  background: var(--color-danger);
  border-radius: var(--radius-full);
}

.book-progress { margin-top: var(--space-2); }
.progress-bar { height: 6px; background: var(--gray-200); border-radius: var(--radius-full); overflow: hidden; }
.progress-fill { height: 100%; border-radius: var(--radius-full); transition: width 1s ease-out; }
.progress-text { font-size: var(--text-xs); color: var(--color-text-muted); margin-top: var(--space-1); display: block; }

@media (max-width: 768px) {
  .stats-grid { grid-template-columns: 1fr; }
  .active-grid { grid-template-columns: 1fr; }
}
</style>