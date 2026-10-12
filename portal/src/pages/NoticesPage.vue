<template>
  <div class="notices-page">
    <PageHeader 
      title="Notices" 
      subtitle="Institution announcements and updates"
      :meta-items="metaItems"
    />

    <div v-if="loading" class="page-loading">
      <div class="notices-skeleton">
        <Skeleton type="card" v-for="i in 5" :key="i" />
      </div>
    </div>

    <template v-else>
      <div v-if="notices.length" class="notices-list">
        <div v-for="n in notices" :key="n.name" class="notice-card card card-hover" :class="{ expanded: expanded === n.name }">
          <button class="notice-header" @click="toggle(n.name)" aria-expanded="expanded === n.name">
            <div class="notice-left">
              <div class="notice-date-badge">
                <span class="date-month">{{ formatMonth(n.publish_date) }}</span>
                <span class="date-day">{{ formatDay(n.publish_date) }}</span>
              </div>
              <div class="notice-info">
                <h4 class="notice-title">{{ n.title }}</h4>
                <div class="notice-badges">
                  <StatusBadge v-if="n.category" :text="n.category" :variant="getCategoryVariant(n.category)" size="xs" />
                  <StatusBadge :text="n.audience_type || 'All'" variant="neutral" size="xs" />
                </div>
              </div>
            </div>
            <div class="notice-right">
              <span class="expand-icon" :class="{ rotated: expanded === n.name }">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"></polyline></svg>
              </span>
            </div>
          </button>
          <div class="notice-body" v-if="expanded === n.name" v-html="n.body"></div>
        </div>
      </div>
      <EmptyState v-else title="No notices" description="There are no published notices at this time" icon="📢" size="lg" />
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { callAPI } from '../utils/api.js'
import PageHeader from '../components/PageHeader.vue'
import StatusBadge from '../components/StatusBadge.vue'
import EmptyState from '../components/EmptyState.vue'
import Skeleton from '../components/Skeleton.vue'

const notices = ref([])
const expanded = ref(null)
const loading = ref(true)

const metaItems = computed(() => [
  { label: 'Total', value: notices.value.length, icon: '📢' }
])

function toggle(name) {
  expanded.value = expanded.value === name ? null : name
}

function formatMonth(d) {
  return d ? new Date(d).toLocaleDateString('en-US', { month: 'short' }) : ''
}
function formatDay(d) {
  return d ? new Date(d).getDate() : ''
}

function getCategoryVariant(category) {
  const map = { 'Academic': 'info', 'Exam': 'warning', 'Fee': 'amber', 'Holiday': 'success', 'Event': 'purple', 'General': 'neutral' }
  return map[category] || 'neutral'
}

onMounted(async () => {
  try {
    const result = await callAPI('portal_get_notices')
    notices.value = result.notices || []
  } catch (e) {
    console.error('Failed to load notices:', e)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.notices-page { animation: fadeIn var(--transition-base); }
.page-loading { padding: var(--space-6); }
.notices-skeleton { display: flex; flex-direction: column; gap: var(--space-3); }

.notices-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.notice-card {
  border-radius: var(--radius-xl);
  border: 1px solid var(--color-border-light);
  overflow: hidden;
  transition: all var(--transition-base);
}
.notice-card:hover { box-shadow: var(--shadow-md); }
.notice-card.expanded { box-shadow: var(--shadow-lg); border-color: var(--color-accent-light); }

.notice-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  width: 100%;
  padding: var(--space-4) var(--space-5);
  border: none;
  background: none;
  cursor: pointer;
  text-align: left;
  gap: var(--space-4);
}

.notice-left { display: flex; align-items: flex-start; gap: var(--space-4); flex: 1; min-width: 0; }

.notice-date-badge {
  width: 56px;
  text-align: center;
  background: var(--gray-50);
  border-radius: var(--radius-lg);
  padding: var(--space-3) var(--space-2);
  flex-shrink: 0;
}
.date-month { display: block; font-size: 10px; font-weight: var(--font-weight-semibold); text-transform: uppercase; color: var(--color-accent); letter-spacing: 0.05em; }
.date-day { display: block; font-size: var(--text-2xl); font-weight: var(--font-weight-bold); color: var(--color-text); line-height: 1; margin-top: 2px; }

.notice-info { flex: 1; min-width: 0; }
.notice-title { font-size: var(--text-md); font-weight: var(--font-weight-semibold); color: var(--color-text); margin-bottom: var(--space-2); line-height: var(--leading-tight); }
.notice-badges { display: flex; flex-wrap: wrap; gap: var(--space-2); }

.notice-right { display: flex; align-items: center; flex-shrink: 0; }
.expand-icon { color: var(--color-text-muted); transition: transform var(--transition-fast); }
.expand-icon.rotated { transform: rotate(180deg); }

.notice-body {
  padding: 0 var(--space-5) var(--space-5) calc(56px + var(--space-4) + var(--space-5));
  border-top: 1px solid var(--color-border-light);
  padding-top: var(--space-4);
  font-size: var(--text-sm);
  line-height: var(--leading-relaxed);
  color: var(--color-text-secondary);
  animation: slideDown var(--transition-base);
}

@media (max-width: 640px) {
  .notice-date-badge { width: 48px; padding: var(--space-2); }
  .date-day { font-size: var(--text-xl); }
  .notice-body { padding-left: var(--space-5); padding-right: var(--space-5); }
  .notice-badges { gap: var(--space-1); }
}
</style>