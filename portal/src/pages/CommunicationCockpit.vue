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
            <span class="icon-svg" v-html="icons.layers"></span>
            Open Full Desk
          </a>
        </template>
      </HeroBanner>

      <div class="stats-grid">
        <StatCard :value="stats.total_notices" label="Total Notices" color="#0f172a" :icon="icons.bell" variant="default" />
        <StatCard :value="stats.published_notices" label="Published" color="#059669" :icon="icons.checkCircle" variant="success" />
        <StatCard :value="stats.pending_feedback" label="Feedback Queue" color="#d97706" :icon="icons.message" variant="amber" :trend="feedbackTrend" trend-variant="negative" />
        <StatCard :value="stats.open_logs" label="Communication Logs" color="#0d9488" :icon="icons.clipboard" variant="default" />
      </div>

      <div class="dash-grid">
        <div class="card card-hover">
          <div class="card-header">
            <h3>Quick Actions</h3>
          </div>
          <div class="card-body">
            <div class="action-grid">
              <a href="/app/notice/new" class="action-card" target="_blank">
                <div class="action-card__icon" style="background:rgba(5,150,105,0.1);color:#059669" v-html="icons.document"></div>
                <span class="action-card__title">Create Notice</span>
                <span class="action-card__desc">Compose and publish</span>
              </a>
              <a href="/app/notice" class="action-card" target="_blank">
                <div class="action-card__icon" style="background:rgba(15,23,42,0.08);color:#0f172a" v-html="icons.bell"></div>
                <span class="action-card__title">All Notices</span>
                <span class="action-card__desc">View and manage notices</span>
              </a>
              <a href="/app/communication-log" class="action-card" target="_blank">
                <div class="action-card__icon" style="background:rgba(13,148,136,0.1);color:#0d9488" v-html="icons.inbox"></div>
                <span class="action-card__title">Communication Logs</span>
                <span class="action-card__desc">View history</span>
              </a>
              <a href="/app/feedback" class="action-card" target="_blank">
                <div class="action-card__icon" style="background:rgba(217,119,6,0.1);color:#d97706" v-html="icons.message"></div>
                <span class="action-card__title">Feedback</span>
                <span class="action-card__desc">Review feedback items</span>
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
              :empty-icon="icons.bell"
            >
              <template #actions="{ item }">
                <a :href="`/app/notice/${item.id}`" target="_blank" class="btn btn-ghost btn-xs">Edit</a>
              </template>
            </TimelineList>
          </div>
          <div class="card-body" v-else>
            <EmptyState title="No notices" description="No notices found" :icon="icons.bell" size="sm" />
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
              :empty-icon="icons.checkCircle"
            >
              <template #actions="{ item }">
                <a :href="`/app/feedback/${item.id}`" target="_blank" class="btn btn-accent btn-sm">Review</a>
              </template>
            </TimelineList>
          </div>
          <div class="card-body" v-else>
            <EmptyState title="All clear" description="No pending feedback" :icon="icons.checkCircle" size="sm" />
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
  { label: 'Role', value: 'Communication Officer', icon: icons.bell }
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
