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
        :subtitle="`${greeting} — Admissions Officer Dashboard`"
        :meta-items="heroMeta"
        illustration="graduation"
        variant="primary"
      >
        <template #actions>
          <a href="/app" class="btn btn-glass" target="_blank">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
            Open Full Desk
          </a>
        </template>
      </HeroBanner>

      <div class="stats-grid">
        <StatCard :value="stats.total_inquiries" label="Total Inquiries" color="#0f172a" icon="📋" variant="default" />
        <StatCard :value="stats.open_inquiries" label="Open Inquiries" color="#d97706" icon="📥" variant="amber" :trend="openTrend" trend-variant="negative" />
        <StatCard :value="stats.under_review" label="Under Review" color="#7c3aed" icon="🔍" variant="purple" />
        <StatCard :value="stats.approved" label="Approved" color="#059669" icon="✅" variant="success" :trend="approvedTrend" trend-variant="positive" />
      </div>

      <div class="dash-grid">
        <div class="card card-hover">
          <div class="card-header">
            <h3>Quick Actions</h3>
          </div>
          <div class="card-body">
            <div class="action-grid">
              <a href="/app/admission-inquiry/new" class="action-card" target="_blank">
                <div class="action-icon" style="background:rgba(5,150,105,0.1);color:#059669">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="12" y1="18" x2="12" y2="12"></line><line x1="9" y1="15" x2="15" y2="15"></line></svg>
                </div>
                <div class="action-content">
                  <span class="action-label">New Inquiry</span>
                  <span class="action-desc">Create admission inquiry</span>
                </div>
              </a>
              <a href="/app/student/new" class="action-card" target="_blank">
                <div class="action-icon" style="background:rgba(30,64,175,0.1);color:#1e40af">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="8.5" cy="7" r="4"></circle><line x1="18" y1="8" x2="18" y2="14"></line><line x1="22" y1="8" x2="22" y2="14"></line></svg>
                </div>
                <div class="action-content">
                  <span class="action-label">New Applicant</span>
                  <span class="action-desc">Register student applicant</span>
                </div>
              </a>
              <a href="/app/student?status=Applied" class="action-card" target="_blank">
                <div class="action-icon" style="background:rgba(124,58,237,0.1);color:#7c3aed">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline></svg>
                </div>
                <div class="action-content">
                  <span class="action-label">Review Applicants</span>
                  <span class="action-desc">View by status</span>
                </div>
              </a>
              <a href="/app/student?status=Approved" class="action-card" target="_blank">
                <div class="action-icon" style="background:rgba(5,150,105,0.1);color:#059669">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
                </div>
                <div class="action-content">
                  <span class="action-label">Approved List</span>
                  <span class="action-desc">View approved applicants</span>
                </div>
              </a>
            </div>
          </div>
        </div>

        <div class="card card-hover dash-card--wide">
          <div class="card-header">
            <h3>Admission Pipeline</h3>
          </div>
          <div class="card-body">
            <div class="pipeline-visual">
              <div class="pipeline-stage" v-for="stage in pipelineStages" :key="stage.key">
                <div class="stage-header" :style="{ borderTopColor: stage.color }">
                  <span class="stage-count">{{ pipeline[stage.key] || 0 }}</span>
                  <span class="stage-label">{{ stage.label }}</span>
                </div>
                <div class="stage-bar" v-if="stage.key !== 'rejected'">
                  <div class="stage-fill" :style="{ width: stageWidth(stage.key) + '%', background: stage.color }"></div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="card card-hover">
          <div class="card-header">
            <h3>Recent Inquiries</h3>
          </div>
          <div class="card-body" v-if="recentInquiries.length">
            <TimelineList 
              :items="inquiryTimelineItems"
              :vertical="true"
              empty-title="No inquiries"
              empty-description="No admission inquiries found"
              empty-icon="📋"
            >
              <template #actions="{ item }">
                <a :href="`/app/admission-inquiry/${item.id}`" target="_blank" class="btn btn-ghost btn-xs">View</a>
              </template>
            </TimelineList>
          </div>
          <div class="card-body" v-else>
            <EmptyState title="No inquiries" description="No admission inquiries found" icon="📋" size="sm" />
          </div>
        </div>

        <div class="card card-hover dash-card--wide">
          <div class="card-header">
            <h3>Inquiry Trend (6 Months)</h3>
          </div>
          <div class="card-body">
            <ChartCard 
              type="line"
              :chart-data="inquiryChartData"
              :height="280"
              :loading="chartLoading"
            />
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
const stats = ref({ total_inquiries: 0, open_inquiries: 0, under_review: 0, approved: 0 })
const pipeline = ref({ open: 0, applied: 0, review: 0, approved: 0, rejected: 0 })
const recentInquiries = ref([])
const loading = ref(true)
const chartLoading = ref(false)

const greeting = computed(() => {
  const h = new Date().getHours()
  if (h < 12) return 'Good morning'
  if (h < 17) return 'Good afternoon'
  return 'Good evening'
})

const heroMeta = computed(() => [
  { label: 'Role', value: 'Admissions Officer', icon: '📋' }
])

const openTrend = '+5 this week'
const approvedTrend = '+12 this month'

const pipelineStages = [
  { key: 'open', label: 'Open', color: '#6b7280' },
  { key: 'applied', label: 'Applied', color: '#d97706' },
  { key: 'review', label: 'Review', color: '#7c3aed' },
  { key: 'approved', label: 'Approved', color: '#059669' },
  { key: 'rejected', label: 'Rejected', color: '#dc2626' }
]

function stageWidth(key) {
  const total = Object.values(pipeline.value).reduce((a, b) => a + b, 0)
  if (total === 0) return 0
  return Math.round((pipeline.value[key] / total) * 100)
}

const inquiryTimelineItems = computed(() => {
  return recentInquiries.value.slice(0, 5).map(inq => ({
    id: inq.name,
    title: inq.inquiry_name || inq.name,
    time: inq.creation,
    badge: { text: inq.status, variant: statusVariant(inq.status), dot: true },
    meta: [{ label: 'Program', value: inq.program || '—' }]
  }))
})

function statusVariant(status) {
  const map = { 'Open': 'info', 'Applied': 'warning', 'Under Review': 'purple', 'Approved': 'success', 'Rejected': 'danger' }
  return map[status] || 'neutral'
}

const inquiryChartData = computed(() => {
  return {
    labels: ['Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    datasets: [
      {
        label: 'Inquiries',
        data: [45, 52, 48, 61, 55, 67],
        borderColor: 'rgba(14, 184, 166, 1)',
        backgroundColor: 'rgba(14, 184, 166, 0.1)',
        fill: true,
        tension: 0.3,
        pointBackgroundColor: 'rgba(14, 184, 166, 1)',
        pointBorderColor: '#fff',
        pointBorderWidth: 2,
        pointRadius: 5
      },
      {
        label: 'Approved',
        data: [12, 18, 15, 22, 19, 25],
        borderColor: 'rgba(5, 150, 105, 1)',
        backgroundColor: 'rgba(5, 150, 105, 0.1)',
        fill: true,
        tension: 0.3,
        pointBackgroundColor: 'rgba(5, 150, 105, 1)',
        pointBorderColor: '#fff',
        pointBorderWidth: 2,
        pointRadius: 5
      }
    ]
  }
})

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
.action-icon { width: 44px; height: 44px; border-radius: var(--radius-lg); display: flex; align-items: center; justify_content: center; flex-shrink: 0; }
.action-content { display: flex; flex-direction: column; gap: 2px; }
.action-label { font-size: var(--text-sm); font-weight: var(--font-weight-semibold); color: var(--color-text); }
.action-desc { font-size: var(--text-xs); color: var(--color-text-muted); }

.pipeline-visual {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);
  padding: var(--space-4) 0;
}
.pipeline-stage { flex: 1; text-align: center; display: flex; flex-direction: column; align-items: center; gap: var(--space-2); }
.stage-header {
  border-top: 3px solid;
  padding-top: var(--space-3);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-1);
  min-width: 120px;
}
.stage-count { font-size: var(--text-2xl); font-weight: var(--font-weight-bold); color: var(--color-text); }
.stage-label { font-size: var(--text-xs); color: var(--color-text-muted); font-weight: var(--font-weight-medium); }
.stage-bar { width: 100%; height: 6px; background: var(--gray-200); border-radius: var(--radius-full); overflow: hidden; }
.stage-fill { height: 100%; border-radius: var(--radius-full); transition: width 1s ease-out; }

@media (max-width: 1024px) {
  .stats-grid { grid-template-columns: repeat(2, 1fr); }
  .dash-grid { grid-template-columns: repeat(2, 1fr); }
  .dash-card--wide { grid-column: span 2; }
  .action-grid { grid-template-columns: 1fr; }
  .pipeline-visual { flex-wrap: wrap; }
  .stage-header { min-width: 100px; }
}
@media (max-width: 768px) {
  .stats-grid { grid-template-columns: 1fr; }
  .dash-grid { grid-template-columns: 1fr; }
  .dash-card--wide { grid-column: span 1; }
  .pipeline-visual { flex-direction: column; gap: var(--space-4); }
  .stage-bar { width: 100%; }
}
</style>