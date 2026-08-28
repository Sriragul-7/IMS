<template>
  <div class="cockpit">
    <div v-if="loading" class="loading-overlay"><div class="spinner spinner-lg"></div></div>
    <template v-else>
      <div class="welcome-banner comms-banner">
        <div>
          <h2>Welcome, {{ user?.user_name }}!</h2>
          <p>{{ greeting }} — Communication Officer Dashboard</p>
        </div>
        <a href="/app" class="btn btn-glass" target="_blank">Open Full Admin &#8599;</a>
      </div>

      <div class="stats-grid">
        <StatCard :value="stats.total_notices" label="TOTAL NOTICES" color="#1e40af" icon="&#9998;" />
        <StatCard :value="stats.published_notices" label="PUBLISHED" color="#059669" icon="&#10003;" />
        <StatCard :value="stats.pending_feedback" label="FEEDBACK QUEUE" color="#d97706" icon="&#10084;" />
        <StatCard :value="stats.open_logs" label="COMMUNICATION LOGS" color="#7c3aed" icon="&#128172;" />
      </div>

      <div class="dash-grid">
        <div class="card">
          <div class="card-header">
            <h3>Quick Actions</h3>
          </div>
          <div class="card-body">
            <div class="action-list">
              <a href="/app/notice/new" class="action-item" target="_blank">
                <span class="action-icon" style="background:rgba(5,150,105,0.1);color:#059669">&#9998;</span>
                <div class="action-text">
                  <span class="action-label">Create Notice</span>
                  <span class="action-desc">Compose and publish a new notice</span>
                </div>
              </a>
              <a href="/app/notice" class="action-item" target="_blank">
                <span class="action-icon" style="background:rgba(30,64,175,0.1);color:#1e40af">&#128203;</span>
                <div class="action-text">
                  <span class="action-label">All Notices</span>
                  <span class="action-desc">View and manage notices</span>
                </div>
              </a>
              <a href="/app/communication-log" class="action-item" target="_blank">
                <span class="action-icon" style="background:rgba(124,58,237,0.1);color:#7c3aed">&#128172;</span>
                <div class="action-text">
                  <span class="action-label">Communication Logs</span>
                  <span class="action-desc">View communication history</span>
                </div>
              </a>
            </div>
          </div>
        </div>

        <div class="card">
          <div class="card-header">
            <h3>Recent Notices</h3>
            <a href="/app/notice" class="btn btn-ghost btn-sm" target="_blank">View All</a>
          </div>
          <div class="card-body" v-if="notices.length">
            <div v-for="n in notices.slice(0, 5)" :key="n.name" class="notice-row">
              <div class="notice-dot" :class="{ published: n.status === 'Published' }"></div>
              <div class="notice-content">
                <span class="notice-title">{{ n.title }}</span>
                <span class="notice-date">{{ formatDate(n.publish_date || n.creation) }}</span>
              </div>
              <StatusBadge :text="n.status" :variant="n.status === 'Published' ? 'success' : 'neutral'" />
            </div>
          </div>
          <div class="card-body" v-else>
            <EmptyState title="No notices" description="No notices found" icon="&#9998;" />
          </div>
        </div>

        <div class="card">
          <div class="card-header">
            <h3>Open Feedback</h3>
            <a href="/app/feedback?status=Open" class="btn btn-ghost btn-sm" target="_blank">View All</a>
          </div>
          <div class="card-body" v-if="feedback.length">
            <div v-for="f in feedback.slice(0, 5)" :key="f.name" class="feedback-row">
              <div class="feedback-info">
                <span class="feedback-type">{{ f.feedback_type }}</span>
                <span class="feedback-date">{{ formatDate(f.creation) }}</span>
              </div>
              <a :href="`/app/feedback/${f.name}`" class="btn btn-sm btn-outline" target="_blank">Review</a>
            </div>
          </div>
          <div class="card-body" v-else>
            <EmptyState title="All clear" description="No pending feedback" icon="&#10003;" />
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

function formatDate(d) { return d ? new Date(d).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }) : '—' }

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
.welcome-banner { background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%); color: white; padding: var(--space-6) var(--space-8); border-radius: var(--radius-xl); margin-bottom: var(--space-6); display: flex; justify-content: space-between; align-items: center; }
.welcome-banner h2 { font-size: var(--text-2xl); font-weight: 700; margin-bottom: var(--space-1); }
.welcome-banner p { font-size: var(--text-sm); opacity: 0.85; }
.btn-glass { padding: var(--space-2) var(--space-4); border-radius: var(--radius-md); background: rgba(255,255,255,0.15); color: white; font-size: var(--text-sm); font-weight: 600; text-decoration: none; transition: all var(--transition-fast); white-space: nowrap; }
.btn-glass:hover { background: rgba(255,255,255,0.25); }
.stats-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: var(--space-4); margin-bottom: var(--space-6); }
.dash-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: var(--space-4); }

.action-list { display: flex; flex-direction: column; gap: var(--space-2); }
.action-item { display: flex; align-items: center; gap: var(--space-3); padding: var(--space-3); border-radius: var(--radius-md); border: 1px solid var(--color-border-light); text-decoration: none; transition: all var(--transition-fast); }
.action-item:hover { border-color: var(--color-primary-light); background: var(--color-primary-50); }
.action-icon { width: 36px; height: 36px; border-radius: var(--radius-md); display: flex; align-items: center; justify-content: center; font-size: 16px; flex-shrink: 0; }
.action-text { flex: 1; }
.action-label { display: block; font-size: var(--text-sm); font-weight: 600; color: var(--color-text); }
.action-desc { font-size: var(--text-xs); color: var(--color-text-muted); }

.notice-row { display: flex; align-items: center; gap: var(--space-3); padding: var(--space-3) 0; border-bottom: 1px solid var(--color-border-light); }
.notice-row:last-child { border-bottom: none; }
.notice-dot { width: 8px; height: 8px; border-radius: 50%; background: var(--gray-300); flex-shrink: 0; }
.notice-dot.published { background: var(--color-success); }
.notice-content { flex: 1; min-width: 0; }
.notice-title { display: block; font-size: var(--text-sm); font-weight: 500; }
.notice-date { font-size: var(--text-xs); color: var(--color-text-muted); }

.feedback-row { display: flex; align-items: center; justify-content: space-between; padding: var(--space-3) 0; border-bottom: 1px solid var(--color-border-light); }
.feedback-row:last-child { border-bottom: none; }
.feedback-info { flex: 1; min-width: 0; }
.feedback-type { display: block; font-size: var(--text-sm); font-weight: 500; }
.feedback-date { font-size: var(--text-xs); color: var(--color-text-muted); }

.btn-outline { padding: var(--space-1) var(--space-3); border: 1px solid var(--color-border); border-radius: var(--radius-sm); background: transparent; color: var(--color-primary); font-size: var(--text-xs); font-weight: 600; text-decoration: none; cursor: pointer; }
.btn-outline:hover { background: var(--color-primary-50); }

@media (max-width: 1024px) { .stats-grid { grid-template-columns: repeat(2, 1fr); } .dash-grid { grid-template-columns: 1fr; } }
@media (max-width: 640px) { .stats-grid { grid-template-columns: 1fr; } .welcome-banner { flex-direction: column; gap: var(--space-3); } }
</style>
