<template>
  <div class="dashboard-page">
    <div v-if="loading" class="page-loading">
      <div class="skeleton skeleton--heading" style="width: 40%;"></div>
      <div class="skeleton skeleton--text" style="width: 60%; margin-top: var(--space-2);"></div>
      <div class="stats-skeleton" style="margin-top: var(--space-6);">
        <Skeleton type="stat" v-for="i in 4" :key="i" />
      </div>
      <div class="dash-skeleton" style="margin-top: var(--space-6);">
        <Skeleton type="card" v-for="i in 3" :key="i" />
      </div>
    </div>

    <template v-else>
      <!-- Hero Banner -->
      <HeroBanner 
        :title="`Welcome, ${user?.user_name}!`"
        :subtitle="greeting"
        :meta-items="heroMeta"
        illustration="campus"
        variant="primary"
      >
        <template #actions>
          <router-link to="/fees" v-if="stats?.outstanding > 0" class="btn btn-accent btn-sm">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="1" x2="12" y2="23"></line><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path></svg>
            Pay Fees
          </router-link>
          <router-link to="/results" class="btn btn-secondary btn-sm">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
            View Results
          </router-link>
        </template>
      </HeroBanner>

      <!-- Stat Cards -->
      <div class="stats-grid" v-if="stats">
        <StatCard 
          :value="stats.attendance_pct" 
          label="Attendance Rate" 
          format="percent"
          color="#059669" 
          icon="&#9776;" 
          :trend="attendanceTrend"
          trend-variant="positive"
          variant="success"
        />
        <StatCard 
          :value="stats.cgpa" 
          label="CGPA / Average" 
          format="number"
          color="#7c3aed" 
          icon="&#9733;" 
          :trend="cgpaTrend"
          trend-variant="positive"
          variant="purple"
        />
        <StatCard 
          :value="stats.outstanding" 
          label="Fee Outstanding" 
          format="currency"
          color="#d97706" 
          icon="&#9888;" 
          variant="amber"
        />
        <StatCard 
          :value="stats.active_books" 
          label="Library Books" 
          format="number"
          color="#2563eb" 
          icon="&#128218;" 
          variant="info"
        />
      </div>

      <!-- Main Grid -->
      <div class="dash-grid">
        <!-- Attendance Donut + Upcoming Classes -->
        <div class="card card-hover dash-card--wide">
          <div class="card-header">
            <h3>Attendance Overview</h3>
            <router-link to="/attendance" class="btn btn-ghost btn-sm">View Details</router-link>
          </div>
          <div class="card-body" v-if="attendance">
            <div class="attendance-overview">
              <div class="attendance-ring-wrapper">
                <ProgressRing 
                  :value="attendance.percentage" 
                  :size="120" 
                  :stroke-width="8"
                  stroke-color="#059669"
                  label="Attendance"
                  unit="%"
                />
              </div>
              <div class="attendance-breakdown">
                <div class="att-stat-row" v-for="item in attendanceItems" :key="item.label">
                  <span class="att-dot" :style="{ background: item.color }"></span>
                  <span class="att-label">{{ item.label }}</span>
                  <strong class="att-value">{{ item.value }}</strong>
                </div>
              </div>
            </div>
            
            <div class="section-divider"></div>
            
            <h4 class="section-subtitle">Upcoming Classes Today</h4>
            <TimelineList 
              :items="todayClasses" 
              :loading="false"
              :vertical="true"
              empty-title="No classes today"
              empty-description="Enjoy your free day!"
              empty-icon="🎉"
            >
              <template #actions="{ item }">
                <router-link :to="`/attendance?group=${item.groupId}`" class="btn btn-ghost btn-xs">View</router-link>
              </template>
            </TimelineList>
          </div>
          <div class="card-body" v-else>
            <EmptyState title="Loading attendance..." description="Please wait" icon="⏳" size="sm" />
          </div>
        </div>

        <!-- Latest Notices -->
        <div class="card card-hover">
          <div class="card-header">
            <h3>Latest Notices</h3>
            <router-link to="/notices" class="btn btn-ghost btn-sm">View All</router-link>
          </div>
          <div class="card-body" v-if="notices.length">
            <TimelineList 
              :items="noticeTimelineItems" 
              :loading="false"
              :vertical="true"
              empty-title="No notices"
              empty-description="No recent notices to display"
              empty-icon="📢"
            />
          </div>
          <div class="card-body" v-else>
            <EmptyState title="No notices" description="No recent notices to display" icon="📢" size="sm" />
          </div>
        </div>

        <!-- Fee Status Summary -->
        <div class="card card-hover">
          <div class="card-header">
            <h3>Fee Status</h3>
            <router-link to="/fees" class="btn btn-ghost btn-sm">View All</router-link>
          </div>
          <div class="card-body" v-if="feeSummary">
            <div class="fee-summary-grid">
              <div class="fee-summary-item" :class="`fee-summary--${item.variant}`" v-for="item in feeSummaryItems" :key="item.label">
                <div class="fee-summary-icon" :style="{ background: item.color + '15', color: item.color }">
                  <span v-html="item.icon"></span>
                </div>
                <div class="fee-summary-content">
                  <span class="fee-summary-value">{{ item.value }}</span>
                  <span class="fee-summary-label">{{ item.label }}</span>
                </div>
              </div>
            </div>
            
            <div class="section-divider"></div>
            
            <div class="recent-fee-list" v-if="recentFees.length">
              <div v-for="f in recentFees.slice(0, 3)" :key="f.name" class="fee-list-item">
                <div class="fee-list-info">
                  <span class="fee-list-name">{{ f.fee_schedule || f.name }}</span>
                  <span class="fee-list-year">{{ f.academic_year }}</span>
                </div>
                <div class="fee-list-right">
                  <span class="fee-list-amount">{{ formatCurrency(f.total_amount) }}</span>
                  <StatusBadge :text="f.status" :variant="feeStatusVariant(f.status)" size="sm" />
                </div>
              </div>
            </div>
            <div v-else class="text-center text-muted text-sm" style="padding: var(--space-4);">No fee records</div>
          </div>
          <div class="card-body" v-else>
            <EmptyState title="Loading fees..." description="Please wait" icon="⏳" size="sm" />
          </div>
        </div>

        <!-- Quick Links -->
        <div class="card card-hover">
          <div class="card-header">
            <h3>Quick Links</h3>
          </div>
          <div class="card-body">
            <div class="quick-links-grid">
              <router-link v-for="link in quickLinks" :key="link.to" :to="link.to" class="quick-link">
                <div class="quick-link-icon" :style="{ background: link.color + '15', color: link.color }">
                  <span v-html="link.icon"></span>
                </div>
                <span class="quick-link-label">{{ link.label }}</span>
              </router-link>
            </div>
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
import ProgressRing from '../components/ProgressRing.vue'
import TimelineList from '../components/TimelineList.vue'
import Skeleton from '../components/Skeleton.vue'

const user = ref(null)
const stats = ref(null)
const attendance = ref(null)
const notices = ref([])
const recentFees = ref([])
const feeSummary = ref(null)
const todayClasses = ref([])
const loading = ref(true)

const greeting = computed(() => {
  const h = new Date().getHours()
  if (h < 12) return 'Good morning! Here\'s your overview for today.'
  if (h < 17) return 'Good afternoon! Here\'s your overview for today.'
  return 'Good evening! Here\'s your overview for today.'
})

const heroMeta = computed(() => [
  { label: 'Program', value: user.value?.program || '—', icon: '🎓' },
  { label: 'Academic Year', value: user.value?.academic_year || '—', icon: '📅' },
  { label: 'Semester', value: user.value?.semester || '—', icon: '📚' }
])

const attendanceTrend = '+2.1% this month'
const cgpaTrend = '+0.15 this semester'

const attendanceItems = computed(() => {
  if (!attendance.value?.summary) return []
  return [
    { label: 'Present', value: attendance.value.summary.Present || 0, color: '#059669' },
    { label: 'Absent', value: attendance.value.summary.Absent || 0, color: '#dc2626' },
    { label: 'Late', value: attendance.value.summary.Late || 0, color: '#d97706' },
    { label: 'Excused', value: attendance.value.summary.Excused || 0, color: '#7c3aed' }
  ]
})

const noticeTimelineItems = computed(() => {
  return notices.value.slice(0, 5).map(n => ({
    id: n.name,
    title: n.title,
    time: n.publish_date,
    badge: { text: n.category || 'General', variant: getCategoryVariant(n.category) },
    body: n.body ? n.body.substring(0, 150) + (n.body.length > 150 ? '...' : '') : ''
  }))
})

function getCategoryVariant(category) {
  const map = { 'Academic': 'info', 'Exam': 'warning', 'Fee': 'amber', 'Holiday': 'success', 'Event': 'purple', 'General': 'neutral' }
  return map[category] || 'neutral'
}

const feeSummaryItems = computed(() => {
  if (!feeSummary.value) return []
  return [
    { label: 'Total Fees', value: formatCurrency(feeSummary.value.total), icon: '💰', color: '#0f172a', variant: 'primary' },
    { label: 'Paid', value: formatCurrency(feeSummary.value.paid), icon: '✅', color: '#059669', variant: 'success' },
    { label: 'Outstanding', value: formatCurrency(feeSummary.value.outstanding), icon: '⚠️', color: '#d97706', variant: 'amber' }
  ]
})

const quickLinks = [
  { to: '/attendance', label: 'Attendance', icon: '📅', color: '#059669' },
  { to: '/results', label: 'Results', icon: '📊', color: '#7c3aed' },
  { to: '/fees', label: 'Fees', icon: '💰', color: '#d97706' },
  { to: '/library', label: 'Library', icon: '📚', color: '#2563eb' },
  { to: '/notices', label: 'Notices', icon: '📢', color: '#ec4899' },
  { to: '/feedback', label: 'Feedback', icon: '💬', color: '#0d9488' }
]

function formatCurrency(v) {
  return '₹' + Number(v || 0).toLocaleString('en-IN', { minimumFractionDigits: 0 })
}

function feeStatusVariant(status) {
  const map = { Paid: 'success', Partial: 'warning', Unpaid: 'danger', Overdue: 'danger' }
  return map[status] || 'neutral'
}

onMounted(async () => {
  user.value = getSessionUser()
  if (!user.value) return

  try {
    const [att, fees, lib, notif] = await Promise.all([
      callAPI('portal_get_attendance', { student: user.value.record_name }),
      callAPI('portal_get_fees', { student: user.value.record_name }),
      callAPI('portal_get_library', { student: user.value.record_name }),
      callAPI('portal_get_notices')
    ])
    
    attendance.value = att
    recentFees.value = fees.fees || []
    notices.value = notif.notices || []
    
    const totalFees = fees.fees?.reduce((s, f) => s + (f.total_amount || 0), 0) || 0
    const totalPaid = fees.fees?.reduce((s, f) => s + (f.paid_amount || 0), 0) || 0
    const totalOutstanding = fees.fees?.reduce((s, f) => s + (f.outstanding_amount || 0), 0) || 0
    
    feeSummary.value = { total: totalFees, paid: totalPaid, outstanding: totalOutstanding }
    
    stats.value = {
      attendance_pct: att.percentage || 0,
      cgpa: att.cgpa || 8.5,
      outstanding: totalOutstanding,
      active_books: lib.active_items?.length || 0
    }
    
    // Load today's classes
    try {
      const classes = await callAPI('portal_get_today_classes', { student: user.value.record_name })
      todayClasses.value = (classes.today_classes || []).map(c => ({
        id: c.name,
        title: `${c.course} (${c.course_code})`,
        time: c.time_slot,
        groupId: c.student_group,
        badge: { text: c.status, variant: c.status === 'Ongoing' ? 'success' : c.status === 'Upcoming' ? 'info' : 'neutral' }
      }))
    } catch (e) {
      todayClasses.value = []
    }
    
  } catch (e) {
    console.error('Dashboard load error:', e)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.dashboard-page { animation: fadeIn var(--transition-base); }

.page-loading { padding: var(--space-6); }
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

.attendance-overview {
  display: flex;
  align-items: center;
  gap: var(--space-8);
  margin-bottom: var(--space-4);
}
.attendance-ring-wrapper { flex-shrink: 0; }
.attendance-breakdown { flex: 1; }
.att-stat-row {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-2) 0;
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
}
.att-dot { width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; }
.att-label { flex: 1; font-weight: var(--font-weight-medium); }
.att-value { font-variant-numeric: tabular-nums; color: var(--color-text); }

.section-divider { height: 1px; background: var(--color-border-light); margin: var(--space-4) 0; }
.section-subtitle { font-size: var(--text-sm); font-weight: var(--font-weight-semibold); color: var(--color-text-secondary); margin-bottom: var(--space-3); }

.fee-summary-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: var(--space-3); }
.fee-summary-item {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-4);
  border-radius: var(--radius-lg);
  background: var(--gray-50);
  border: 1px solid var(--color-border-light);
}
.fee-summary-icon { width: 36px; height: 36px; border-radius: var(--radius-md); display: flex; align-items: center; justify-content: center; font-size: 1rem; flex-shrink: 0; }
.fee-summary-content { display: flex; flex-direction: column; gap: 2px; }
.fee-summary-value { font-size: var(--text-lg); font-weight: var(--font-weight-bold); color: var(--color-text); font-variant-numeric: tabular-nums; }
.fee-summary-label { font-size: var(--text-xs); color: var(--color-text-muted); }

.recent-fee-list { display: flex; flex-direction: column; gap: var(--space-2); }
.fee-list-item { display: flex; align-items: center; justify-content: space-between; padding: var(--space-2) 0; border-bottom: 1px solid var(--color-border-light); }
.fee-list-item:last-child { border-bottom: none; }
.fee-list-info { flex: 1; min-width: 0; }
.fee-list-name { display: block; font-size: var(--text-sm); font-weight: var(--font-weight-medium); color: var(--color-text); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.fee-list-year { font-size: var(--text-xs); color: var(--color-text-muted); }
.fee-list-right { display: flex; align-items: center; gap: var(--space-2); }
.fee-list-amount { font-size: var(--text-sm); font-weight: var(--font-weight-semibold); color: var(--color-text); white-space: nowrap; font-variant-numeric: tabular-nums; }

.quick-links-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: var(--space-2); }
.quick-link {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-4) var(--space-2);
  border-radius: var(--radius-md);
  border: 1px solid var(--color-border-light);
  text-decoration: none;
  transition: all var(--transition-fast);
  text-align: center;
}
.quick-link:hover { border-color: var(--color-accent-light); background: var(--color-accent-50); transform: translateY(-1px); box-shadow: var(--shadow-sm); }
.quick-link-icon { width: 40px; height: 40px; border-radius: var(--radius-md); display: flex; align-items: center; justify-content: center; font-size: 1.25rem; }
.quick-link-label { font-size: var(--text-xs); font-weight: var(--font-weight-medium); color: var(--color-text); }

@media (max-width: 1024px) {
  .stats-grid { grid-template-columns: repeat(2, 1fr); }
  .dash-grid { grid-template-columns: repeat(2, 1fr); }
  .dash-card--wide { grid-column: span 2; }
  .quick-links-grid { grid-template-columns: repeat(3, 1fr); }
}
@media (max-width: 768px) {
  .stats-grid { grid-template-columns: 1fr; }
  .dash-grid { grid-template-columns: 1fr; }
  .dash-card--wide { grid-column: span 1; }
  .attendance-overview { flex-direction: column; text-align: center; gap: var(--space-4); }
  .att-stat-row { justify-content: center; }
  .quick-links-grid { grid-template-columns: repeat(2, 1fr); }
  .fee-summary-grid { grid-template-columns: 1fr; }
}
</style>