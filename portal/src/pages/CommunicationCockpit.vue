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
        :subtitle="`${greeting} — Communication Officer Dashboard`"
        :meta-items="heroMeta"
        illustration="abstract"
        variant="info"
      >
        <template #actions>
          <a href="/app" class="btn btn-glass" target="_blank">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
            Open Full Desk
          </a>
        </template>
      </HeroBanner>

      <div class="stats-grid">
        <StatCard :value="stats.total_notices" label="Total Notices" color="#0f172a" icon="📢" variant="default" />
        <StatCard :value="stats.published_notices" label="Published" color="#059669" icon="✅" variant="success" />
        <StatCard :value="stats.pending_feedback" label="Feedback Queue" color="#d97706" icon="💬" variant="amber" :trend="feedbackTrend" trend-variant="negative" />
        <StatCard :value="stats.open_logs" label="Communication Logs" color="#7c3aed" icon="📋" variant="purple" />
      </div>

      <div class="dash-grid">
        <div class="card card-hover">
          <div class="card-header">
            <h3>Quick Actions</h3>
          </div>
          <div class="card-body">
            <div class="action-grid">
              <a href="/app/notice/new" class="action-card" target="_blank">
                <div class="action-icon" style="background:rgba(5,150,105,0.1);color:#059669">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
                </div>
                <div class="action-content">
                  <span class="action-label">Create Notice</span>
                  <span class="action-desc">Compose and publish</span>
                </div>
              </a>
              <a href="/app/notice" class="action-card" target="_blank">
                <div class="action-icon" style="background:rgba(30,64,175,0.1);color:#1e40af">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline></svg>
                </div>
                <div class="action-content">
                  <span class="action-label">All Notices</span>
                  <span class="action-desc">View and manage notices</span>
                </div>
              </a>
              <a href="/app/communication-log" class="action-card" target="_blank">
                <div class="action-icon" style="background:rgba(124,58,237,0.1);color:#7c3aed">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path><polyline points="22 6 12 13 9 13"></polyline></svg>
                </div>
                <div class="action-content">
                  <span class="action-label">Communication Logs</span>
                  <span class="action-desc">View history</span>
                </div>
              </a>
              <a href="/app/feedback" class="action-card" target="_blank">
                <div class="action-icon" style="background:rgba(236,72,153,0.1);color:#ec4899">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>
                </div>
                <div class="action-content">
                  <span class="action-label">Feedback</span>
                  <span class="action-desc">Review feedback items</span>
                </div>
              </a>
            </div>
          </div>
        </div>

        <div class="card card-hover dash-card--wide">
          <div class="card-header">
            <h3>Recent Notices</h3>
            <a href="/app/notice" class="btn btn-ghost btn-sm" target="_blank">View All</a>
          </div>
          <div class="card-body" v-if="notices.length">
            <TimelineList 
              :items="noticesTimelineItems"
              :vertical="true"
              empty-title="No notices"
              empty-description="No notices found"
              empty-icon="📢"
            >
              <template #actions="{ item }">
                <a :href="`/app/notice/${item.id}`" target="_blank" class="btn btn-ghost btn-xs">Edit</a>
              </template>
            </TimelineList>
          </div>
          <div class="card-body" v-else>
            <EmptyState title="No notices" description="No notices found" icon="📢" size="sm" />
          </div>
        </div>

        <div class="card card-hover dash-card--wide">
          <div class="card-header">
            <h3>Open Feedback</h3>
            <a href="/app/feedback?status=Open" class="btn btn-ghost btn-sm" target="_blank">View All</a>
          </div>
          <div class="card-body" v-if="feedback.length">
            <TimelineList 
              :items="feedbackTimelineItems"
              :vertical="true"
              empty-title="All clear"
              empty-description="No pending feedback"
              empty-icon="✅"
            >
              <template #actions="{ item }">
                <a :href="`/app/feedback/${item.id}`" target="_blank" class="btn btn-accent btn-sm">Review</a>
              </template>
            </TimelineList>
          </div>
          <div class="card-body" v-else>
            <EmptyState title="All clear" description="No pending feedback" icon="✅" size="sm" />
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
const stats = ref({ total_notices: 0, published_notices: 0, pending_feedback: 0, open_logs: 0 })
const notices = ref([])
const feedback = ref([])
const loading = ref(true)

const greeting = computed(() => {
  const h = new Date().getHours()
  if (h < 12) return 'Good morning'
  if (h < 17) return 'Good afternoon'
  return 'Good evening'
})

const heroMeta = computed(() => [
  { label: 'Role', value: 'Communication Officer', icon: '📢' }
])

const feedbackTrend = '+3 new today'

const noticesTimelineItems = computed(() => {
  return notices.value.slice(0, 5).map(n => ({
    id: n.name,
    title: n.title,
    time: n.publish_date || n.creation,
    badge: { text: n.status, variant: n.status === 'Published' ? 'success' : 'neutral', dot: true },
    meta: [{ label: 'Audience', value: n.audience_type || 'All' }]
  }))
})

const feedbackTimelineItems = computed(() => {
  return feedback.value.slice(0, 5).map(f => ({
    id: f.name,
    title: f.subject,
    time: f.creation,
    badge: { text: f.status, variant: fbVariant(f.status), dot: true },
    meta: [{ label: 'Type', value: f.feedback_type }, { label: 'From', value: f.student_name || f.student }]
  }))
})

function fbVariant(status) {
  const map = { Open: 'warning', 'In Progress': 'info', Resolved: 'success', Closed: 'neutral' }
  return map[status] || 'neutral'
}

onMounted(async () => {
  user.value = getSessionUser()
  if (!user.value) return
  try {
    const [noticeData, feedbackData] = await Promise.all([
      callAPI('portal_get_notices').catch(() => ({ notices: [] })),
      callAPI('portal_get_feedback_queue').catch(() => []),
    ])
    notices.value = noticeData.notices || []
    feedback.value = Array.isArray(feedbackData) ? feedbackData : []
    stats.value = {
      total_notices: notices.value.length,
      published_notices: notices.value.filter(n => n.status === 'Published').length,
      pending_feedback: feedback.value.length,
      open_logs: 0,
    }
  } catch (e) {
    console.error('Communication Officer cockpit load error:', e)
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