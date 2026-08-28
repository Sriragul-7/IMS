<template>
  <div class="cockpit">
    <div v-if="loading" class="loading-overlay"><div class="spinner spinner-lg"></div></div>
    <template v-else>
      <div class="welcome-banner admissions-banner">
        <div>
          <h2>Welcome, {{ user?.user_name }}!</h2>
          <p>{{ greeting }} — Admissions Officer Dashboard</p>
        </div>
        <a href="/app" class="btn btn-glass" target="_blank">Open Full Admin &#8599;</a>
      </div>

      <div class="stats-grid">
        <StatCard :value="stats.total_inquiries" label="TOTAL INQUIRIES" color="#1e40af" icon="&#128221;" />
        <StatCard :value="stats.open_inquiries" label="OPEN INQUIRIES" color="#d97706" icon="&#9888;" />
        <StatCard :value="stats.under_review" label="UNDER REVIEW" color="#7c3aed" icon="&#128269;" />
        <StatCard :value="stats.approved" label="APPROVED" color="#059669" icon="&#10003;" />
      </div>

      <div class="dash-grid">
        <div class="card">
          <div class="card-header">
            <h3>Quick Actions</h3>
          </div>
          <div class="card-body">
            <div class="action-list">
              <a href="/app/admission-inquiry/new" class="action-item" target="_blank">
                <span class="action-icon" style="background:rgba(5,150,105,0.1);color:#059669">&#10010;</span>
                <div class="action-text">
                  <span class="action-label">New Inquiry</span>
                  <span class="action-desc">Create a new admission inquiry</span>
                </div>
              </a>
              <a href="/app/student/new" class="action-item" target="_blank">
                <span class="action-icon" style="background:rgba(30,64,175,0.1);color:#1e40af">&#128100;</span>
                <div class="action-text">
                  <span class="action-label">New Applicant</span>
                  <span class="action-desc">Register a new student applicant</span>
                </div>
              </a>
              <a href="/app/student?status=Applied" class="action-item" target="_blank">
                <span class="action-icon" style="background:rgba(124,58,237,0.1);color:#7c3aed">&#128203;</span>
                <div class="action-text">
                  <span class="action-label">Review Applicants</span>
                  <span class="action-desc">View applicants by status</span>
                </div>
              </a>
            </div>
          </div>
        </div>

        <div class="card pipeline-card">
          <div class="card-header">
            <h3>Admission Pipeline</h3>
          </div>
          <div class="card-body">
            <div class="pipeline-stages">
              <div class="pipeline-col">
                <div class="stage-header" style="border-top-color: #6b7280;">
                  <span class="stage-count">{{ pipeline.open }}</span>
                  <span class="stage-label">Open</span>
                </div>
              </div>
              <div class="pipeline-arrow">&#8594;</div>
              <div class="pipeline-col">
                <div class="stage-header" style="border-top-color: #d97706;">
                  <span class="stage-count">{{ pipeline.applied }}</span>
                  <span class="stage-label">Applied</span>
                </div>
              </div>
              <div class="pipeline-arrow">&#8594;</div>
              <div class="pipeline-col">
                <div class="stage-header" style="border-top-color: #7c3aed;">
                  <span class="stage-count">{{ pipeline.review }}</span>
                  <span class="stage-label">Review</span>
                </div>
              </div>
              <div class="pipeline-arrow">&#8594;</div>
              <div class="pipeline-col">
                <div class="stage-header" style="border-top-color: #059669;">
                  <span class="stage-count">{{ pipeline.approved }}</span>
                  <span class="stage-label">Approved</span>
                </div>
              </div>
              <div class="pipeline-arrow">&#8594;</div>
              <div class="pipeline-col">
                <div class="stage-header" style="border-top-color: #dc2626;">
                  <span class="stage-count">{{ pipeline.rejected }}</span>
                  <span class="stage-label">Rejected</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="card">
          <div class="card-header">
            <h3>Recent Inquiries</h3>
          </div>
          <div class="card-body" v-if="recentInquiries.length">
            <div v-for="inq in recentInquiries.slice(0, 5)" :key="inq.name" class="inquiry-row">
              <div class="inquiry-info">
                <span class="inquiry-name">{{ inq.inquiry_name || inq.name }}</span>
                <span class="inquiry-date">{{ formatDate(inq.creation) }}</span>
              </div>
              <StatusBadge :text="inq.status" :variant="statusVariant(inq.status)" />
            </div>
          </div>
          <div class="card-body" v-else>
            <EmptyState title="No inquiries" description="No admission inquiries found" icon="&#128221;" />
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
const stats = ref({ total_inquiries: 0, open_inquiries: 0, under_review: 0, approved: 0 })
const pipeline = ref({ open: 0, applied: 0, review: 0, approved: 0, rejected: 0 })
const recentInquiries = ref([])
const loading = ref(true)

const greeting = computed(() => {
  const h = new Date().getHours()
  if (h < 12) return 'Good morning'
  if (h < 17) return 'Good afternoon'
  return 'Good evening'
})

function formatDate(d) { return d ? new Date(d).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }) : '—' }
function statusVariant(status) {
  const map = { 'Open': 'info', 'Applied': 'warning', 'Under Review': 'purple', 'Approved': 'success', 'Rejected': 'danger' }
  return map[status] || 'neutral'
}

onMounted(async () => {
  user.value = getSessionUser()
  if (!user.value) return
  try {
    const [inqData, pipelineData] = await Promise.all([
      callAPI('portal_get_admission_inquiries').catch(() => []),
      callAPI('portal_get_admission_pipeline').catch(() => ({})),
    ])
    recentInquiries.value = Array.isArray(inqData) ? inqData : []
    pipeline.value = pipelineData || {}
    stats.value = {
      total_inquiries: recentInquiries.value.length,
      open_inquiries: pipeline.value.open || 0,
      under_review: pipeline.value.review || 0,
      approved: pipeline.value.approved || 0,
    }
  } catch (e) {
    console.error('Admissions Officer cockpit load error:', e)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.welcome-banner { background: linear-gradient(135deg, #1e40af 0%, #1e3a8a 100%); color: white; padding: var(--space-6) var(--space-8); border-radius: var(--radius-xl); margin-bottom: var(--space-6); display: flex; justify-content: space-between; align-items: center; }
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

.pipeline-stages { display: flex; align-items: center; justify-content: center; gap: var(--space-2); padding: var(--space-4) 0; }
.pipeline-col { flex: 1; text-align: center; }
.stage-header {
  border-top: 3px solid;
  padding-top: var(--space-3);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-1);
}
.stage-count { font-size: var(--text-2xl); font-weight: 700; color: var(--color-text); }
.stage-label { font-size: var(--text-xs); color: var(--color-text-muted); font-weight: 500; }
.pipeline-arrow { color: var(--gray-300); font-size: 18px; flex-shrink: 0; }

.inquiry-row { display: flex; align-items: center; justify-content: space-between; padding: var(--space-3) 0; border-bottom: 1px solid var(--color-border-light); }
.inquiry-row:last-child { border-bottom: none; }
.inquiry-info { flex: 1; min-width: 0; }
.inquiry-name { display: block; font-size: var(--text-sm); font-weight: 500; }
.inquiry-date { font-size: var(--text-xs); color: var(--color-text-muted); }

@media (max-width: 1024px) { .stats-grid { grid-template-columns: repeat(2, 1fr); } .dash-grid { grid-template-columns: 1fr; } }
@media (max-width: 640px) { .stats-grid { grid-template-columns: 1fr; } .welcome-banner { flex-direction: column; gap: var(--space-3); } .pipeline-stages { flex-wrap: wrap; } }
</style>
