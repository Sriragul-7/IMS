<template>
  <div class="data-table-container">
    <div class="data-table-toolbar" v-if="showToolbar">
      <div class="toolbar-left">
        <slot name="toolbar-left" />
      </div>
      <div class="toolbar-right">
        <slot name="toolbar-right" />
      </div>
    </div>
    
    <div class="table-wrapper">
      <table class="data-table" :class="{ 'data-table--striped': striped, 'data-table--hover': hover, 'data-table--sticky-header': stickyHeader }">
        <thead v-if="columns.length">
          <tr>
            <th v-for="col in columns" :key="col.key" :class="col.class" :style="{ width: col.width, textAlign: col.align }">
              <div class="th-content">
                <span>{{ col.label }}</span>
                <span v-if="col.sortable" class="sort-indicator" @click="handleSort(col.key)">
                  <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
                    <path d="M6 2L10 6M6 2L2 6M6 10L2 6M6 10L10 6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </span>
              </div>
            </th>
          </tr>
        </thead>
        <tbody v-if="!loading">
          <tr v-for="(row, rowIndex) in data" :key="getRowKey(row, rowIndex)" :class="getRowClass(row, rowIndex)" @click="handleRowClick(row, rowIndex)">
            <td v-for="col in columns" :key="col.key" :class="col.class" :style="{ textAlign: col.align }">
              <slot :name="cell(col.key)" :row="row" :column="col" :index="rowIndex">
                <template v-if="col.render">
                  <component :is="col.render" :row="row" :value="row[col.key]" :column="col" :index="rowIndex" />
                </template>
                <template v-else>
                  {{ formatValue(row[col.key], col) }}
                </template>
              </slot>
            </td>
          </tr>
          <tr v-if="data.length === 0 && !emptyStateHidden" class="empty-row">
            <td :colspan="columns.length">
              <EmptyState :title="emptyTitle" :description="emptyDescription" :icon="emptyIcon" />
            </td>
          </tr>
        </tbody>
        <tbody v-else>
          <tr v-for="i in skeletonRows" :key="i">
            <td v-for="col in columns" :key="col.key">
              <div class="skeleton skeleton-text" style="width: 80%;"></div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <div class="data-table-pagination" v-if="pagination && totalPages > 1">
      <div class="pagination-info">
        Showing {{ (page - 1) * pageSize + 1 }} to {{ Math.min(page * pageSize, total) }} of {{ total }} entries
      </div>
      <div class="pagination-controls">
        <button class="btn btn-sm btn-secondary" :disabled="page <= 1" @click="page = page - 1">Previous</button>
        <div class="pagination-pages">
          <button v-for="p in visiblePages" :key="p" :class="['btn', 'btn-sm', p === page ? 'btn-primary' : 'btn-secondary']" @click="page = p">{{ p }}</button>
        </div>
        <button class="btn btn-sm btn-secondary" :disabled="page >= totalPages" @click="page = page + 1">Next</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import EmptyState from './EmptyState.vue'

const props = defineProps({
  columns: { type: Array, required: true },
  data: { type: Array, default: () => [] },
  loading: { type: Boolean, default: false },
  striped: { type: Boolean, default: true },
  hover: { type: Boolean, default: true },
  stickyHeader: { type: Boolean, default: true },
  showToolbar: { type: Boolean, default: false },
  pagination: { type: Boolean, default: false },
  page: { type: Number, default: 1 },
  pageSize: { type: Number, default: 10 },
  total: { type: Number, default: 0 },
  rowKey: { type: [String, Function], default: 'name' },
  rowClass: { type: Function, default: () => '' },
  rowClickable: { type: Boolean, default: false },
  emptyTitle: { type: String, default: 'No data' },
  emptyDescription: { type: String, default: 'No records found' },
  emptyIcon: { type: String, default: '📄' },
  emptyStateHidden: { type: Boolean, default: false },
  skeletonRows: { type: Number, default: 5 }
})

const emit = defineEmits(['sort', 'page-change', 'row-click'])

const sortKey = ref(null)
const sortOrder = ref('asc')
const currentPage = ref(props.page)

const totalPages = computed(() => Math.ceil(props.total / props.pageSize) || 1)
const visiblePages = computed(() => {
  const pages = []
  const total = totalPages.value
  const current = currentPage.value
  
  if (total <= 7) {
    for (let i = 1; i <= total; i++) pages.push(i)
  } else {
    pages.push(1)
    if (current > 3) pages.push('...')
    for (let i = Math.max(2, current - 1); i <= Math.min(total - 1, current + 1); i++) {
      pages.push(i)
    }
    if (current < total - 2) pages.push('...')
    pages.push(total)
  }
  return pages
})

function getRowKey(row, index) {
  if (typeof props.rowKey === 'function') return props.rowKey(row, index)
  return row[props.rowKey] || index
}

function getRowClass(row, index) {
  const base = []
  if (props.striped && index % 2 === 1) base.push('striped')
  if (props.rowClickable) base.push('clickable')
  const custom = props.rowClass(row, index)
  if (custom) base.push(custom)
  return base.join(' ')
}

function formatValue(value, column) {
  if (value === null || value === undefined || value === '') return '—'
  if (column.format) return column.format(value, column)
  if (typeof value === 'number' && column.type === 'currency') {
    return '₹' + value.toLocaleString('en-IN', { minimumFractionDigits: 0, maximumFractionDigits: 2 })
  }
  if (typeof value === 'number' && column.type === 'number') {
    return value.toLocaleString('en-IN')
  }
  if (value instanceof Date) {
    return value.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
  }
  return String(value)
}

function handleSort(key) {
  if (!key) return
  if (sortKey.value === key) {
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortKey.value = key
    sortOrder.value = 'asc'
  }
  emit('sort', { key, order: sortOrder.value })
}

function handleRowClick(row, index) {
  if (props.rowClickable) {
    emit('row-click', { row, index })
  }
}

watch(() => props.page, (val) => {
  currentPage.value = val
})
watch(currentPage, (val) => {
  emit('page-change', val)
})
</script>

<style scoped>
.data-table-container {
  background: var(--color-surface);
  border-radius: var(--radius-xl);
  border: 1px solid var(--color-border-light);
  overflow: hidden;
}
.data-table-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-4) var(--space-6);
  border-bottom: 1px solid var(--color-border-light);
  gap: var(--space-4);
  flex-wrap: wrap;
}
.toolbar-left, .toolbar-right { display: flex; align-items: center; gap: var(--space-3); }
.table-wrapper { overflow-x: auto; }
.data-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  font-size: var(--text-sm);
}
.data-table th {
  padding: var(--space-3) var(--space-4);
  font-size: var(--text-xs);
  font-weight: var(--font-weight-semibold);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--color-text-muted);
  background: var(--gray-50);
  border-bottom: 1px solid var(--color-border);
  white-space: nowrap;
  text-align: left;
}
.data-table th:first-child { border-radius: var(--radius-xl) 0 0 0; }
.data-table th:last-child { border-radius: 0 var(--radius-xl) 0 0; }
.th-content { display: flex; align-items: center; gap: var(--space-1-5); }
.sort-indicator { display: inline-flex; align-items: center; color: var(--color-text-muted); cursor: pointer; opacity: 0.5; transition: opacity var(--transition-fast); }
.sort-indicator:hover { opacity: 1; }
.data-table td {
  padding: var(--space-3-5) var(--space-4);
  color: var(--color-text);
  border-bottom: 1px solid var(--color-border-light);
  vertical-align: middle;
}
.data-table--striped tbody tr.striped td { background: var(--gray-50); }
.data-table--hover tbody tr.clickable { cursor: pointer; }
.data-table--hover tbody tr:hover td { background: var(--color-primary-50); }
.data-table tbody tr:last-child td { border-bottom: none; }
.data-table tbody tr:last-child td:first-child { border-radius: 0 0 0 var(--radius-xl); }
.data-table tbody tr:last-child td:last-child { border-radius: 0 0 var(--radius-xl) 0; }
.empty-row td { padding: var(--space-12) var(--space-6); }
.pagination-info { font-size: var(--text-sm); color: var(--color-text-secondary); }
.pagination-controls { display: flex; align-items: center; gap: var(--space-2); }
.pagination-pages { display: flex; gap: var(--space-1); }
.pagination-pages .btn { min-width: 36px; }
</style>