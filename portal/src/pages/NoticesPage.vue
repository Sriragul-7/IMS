<template>
  <div class="notices-page">
    <PageHeader title="Notices" subtitle="Institution announcements and updates" />

    <div v-if="!loaded" class="loading-overlay"><div class="spinner spinner-lg"></div></div>

    <template v-else>
      <div v-if="notices.length" class="notices-list">
        <div v-for="n in notices" :key="n.name" class="notice-card" :class="{ expanded: expanded === n.name }">
          <button class="notice-header" @click="toggle(n.name)">
            <div class="notice-left">
              <div class="notice-date-badge">
                <span class="date-month">{{ formatMonth(n.publish_date) }}</span>
                <span class="date-day">{{ formatDay(n.publish_date) }}</span>
              </div>
              <div class="notice-info">
                <h4 class="notice-title">{{ n.title }}</h4>
                <span class="notice-audience">{{ n.audience_type }}</span>
              </div>
            </div>
            <span class="expand-icon" :class="{ rotated: expanded === n.name }">&#9662;</span>
          </button>
          <div class="notice-body" v-if="expanded === n.name">
            <div v-html="n.body"></div>
          </div>
        </div>
      </div>
      <EmptyState v-else title="No notices" description="There are no published notices at this time" icon="&#9998;" />
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { callAPI } from '../utils/api.js'
import PageHeader from '../components/PageHeader.vue'
import EmptyState from '../components/EmptyState.vue'

const notices = ref([])
const expanded = ref(null)
const loaded = ref(false)

function toggle(name) {
  expanded.value = expanded.value === name ? null : name
}

function formatMonth(d) {
  return d ? new Date(d).toLocaleDateString('en-US', { month: 'short' }) : ''
}
function formatDay(d) {
  return d ? new Date(d).getDate() : ''
}

onMounted(async () => {
  try {
    const result = await callAPI('portal_get_notices')
    notices.value = result.notices || []
  } catch (e) {
    console.error('Failed to load notices:', e)
  } finally {
    loaded.value = true
  }
})
</script>

<style scoped>
.notices-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.notice-card {
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--color-border-light);
  overflow: hidden;
  transition: box-shadow var(--transition-base);
}
.notice-card:hover { box-shadow: var(--shadow-md); }
.notice-card.expanded { box-shadow: var(--shadow-md); }

.notice-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  padding: var(--space-4) var(--space-5);
  border: none;
  background: none;
  cursor: pointer;
  text-align: left;
}

.notice-left {
  display: flex;
  align-items: center;
  gap: var(--space-4);
}

.notice-date-badge {
  width: 48px;
  text-align: center;
  background: var(--gray-50);
  border-radius: var(--radius-md);
  padding: var(--space-2);
  flex-shrink: 0;
}
.date-month { display: block; font-size: 10px; font-weight: 600; text-transform: uppercase; color: var(--color-primary); }
.date-day { display: block; font-size: var(--text-xl); font-weight: 700; color: var(--color-text); line-height: 1; margin-top: 2px; }

.notice-info { flex: 1; min-width: 0; }
.notice-title { font-size: var(--text-md); font-weight: 600; color: var(--color-text); margin-bottom: var(--space-1); }
.notice-audience {
  font-size: 10px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--color-purple);
  background: var(--color-purple-light);
  padding: 2px var(--space-2);
  border-radius: var(--radius-full);
}

.expand-icon {
  font-size: 12px;
  color: var(--color-text-muted);
  transition: transform var(--transition-fast);
}
.expand-icon.rotated { transform: rotate(180deg); }

.notice-body {
  padding: 0 var(--space-5) var(--space-5) calc(48px + var(--space-4) + var(--space-5));
  border-top: 1px solid var(--color-border-light);
  padding-top: var(--space-4);
  font-size: var(--text-sm);
  line-height: var(--leading-relaxed);
  color: var(--color-text-secondary);
}
</style>
