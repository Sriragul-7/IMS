<template>
  <div class="library-page">
    <PageHeader title="Library" subtitle="Book issues, returns, and transaction history" />

    <div v-if="!loaded" class="loading-overlay"><div class="spinner spinner-lg"></div></div>

    <template v-else>
      <div v-if="activeItems.length" class="section">
        <h3 class="section-title">Currently Checked Out</h3>
        <div class="active-grid">
          <div v-for="item in activeItems" :key="item.name" class="active-card" :class="{ overdue: isOverdue(item.due_date) }">
            <div class="active-top">
              <span class="book-icon">&#128214;</span>
              <StatusBadge :text="isOverdue(item.due_date) ? 'Overdue' : 'Active'" :variant="isOverdue(item.due_date) ? 'danger' : 'success'" dot />
            </div>
            <div class="book-title">{{ item.library_item_name || item.library_item }}</div>
            <div class="book-dates">
              <div class="date-row">
                <span class="date-label">Issued</span>
                <span>{{ formatDate(item.transaction_date) }}</span>
              </div>
              <div class="date-row">
                <span class="date-label">Due</span>
                <span :class="{ 'text-danger': isOverdue(item.due_date) }">{{ formatDate(item.due_date) }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="card-header"><h3>Transaction History</h3></div>
        <div class="table-wrapper" v-if="transactions.length">
          <table class="data-table">
            <thead>
              <tr>
                <th>Item</th>
                <th>Issue Date</th>
                <th>Due Date</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="t in transactions" :key="t.name">
                <td class="font-medium">{{ t.library_item_name || t.library_item }}</td>
                <td>{{ formatDate(t.transaction_date) }}</td>
                <td>{{ formatDate(t.due_date) }}</td>
                <td>
                  <StatusBadge :text="t.status === 'Issue' ? 'Checked Out' : 'Returned'"
                    :variant="t.status === 'Issue' ? 'warning' : 'success'" />
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <EmptyState v-else title="No transactions" description="No library transactions found" icon="&#9734;" />
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { getSessionUser, callAPI } from '../utils/api.js'
import PageHeader from '../components/PageHeader.vue'
import StatusBadge from '../components/StatusBadge.vue'
import EmptyState from '../components/EmptyState.vue'

const props = defineProps({ selectedChild: String })
const activeItems = ref([])
const transactions = ref([])
const loaded = ref(false)

function formatDate(d) {
  return d ? new Date(d).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }) : ''
}

function isOverdue(dueDate) {
  if (!dueDate) return false
  return new Date(dueDate) < new Date()
}

async function load() {
  const user = getSessionUser()
  if (!user) return
  const student = user.role === 'Guardian' ? (props.selectedChild || undefined) : undefined
  const result = await callAPI('portal_get_library', { student })
  activeItems.value = result.active_items || []
  transactions.value = result.transactions || []
  loaded.value = true
}

onMounted(load)
watch(() => props.selectedChild, load)
</script>

<style scoped>
.section { margin-bottom: var(--space-6); }
.section-title {
  font-size: var(--text-md);
  font-weight: 600;
  margin-bottom: var(--space-4);
}

.active-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: var(--space-4);
}

.active-card {
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  padding: var(--space-5);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--color-border-light);
  border-left: 4px solid var(--color-success);
  transition: box-shadow var(--transition-base);
}
.active-card:hover { box-shadow: var(--shadow-md); }
.active-card.overdue { border-left-color: var(--color-danger); }

.active-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--space-3);
}
.book-icon { font-size: 1.25rem; }

.book-title {
  font-size: var(--text-md);
  font-weight: 600;
  color: var(--color-text);
  margin-bottom: var(--space-3);
}

.book-dates {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}
.date-row {
  display: flex;
  justify-content: space-between;
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
}
.date-label { color: var(--color-text-muted); }
.text-danger { color: var(--color-danger); font-weight: 600; }
</style>
