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
        :subtitle="`${greeting} — Facility Manager Dashboard`"
        :meta-items="heroMeta"
        illustration="campus"
        variant="purple"
      >
        <template #actions>
          <a href="/app" class="btn btn-glass" target="_blank">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
            Open Full Desk
          </a>
        </template>
      </HeroBanner>

      <div class="stats-grid">
        <StatCard :value="stats.available_books" label="Available Books" color="#0f172a" icon="📚" variant="default" />
        <StatCard :value="stats.active_issues" label="Active Issues" color="#d97706" icon="📖" variant="amber" />
        <StatCard :value="stats.overdue_items" label="Overdue Items" color="#dc2626" icon="⚠️" variant="danger" :trend="overdueTrend" trend-variant="negative" />
        <StatCard :value="stats.hostel_occupancy" label="Hostel Occupancy" color="#059669" icon="🏠" variant="success" :trend="occupancyTrend" trend-variant="positive" />
      </div>

      <div class="dash-grid">
        <div class="card card-hover">
          <div class="card-header">
            <h3>Quick Actions</h3>
          </div>
          <div class="card-body">
            <div class="action-grid">
              <a href="/app/library-transaction/new" class="action-card" target="_blank">
                <div class="action-icon" style="background:rgba(5,150,105,0.1);color:#059669">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="17 8 12 3 7 8"></polyline><line x1="12" y1="3" x2="12" y2="15"></line></svg>
                </div>
                <div class="action-content">
                  <span class="action-label">Issue Book</span>
                  <span class="action-desc">Issue a library item</span>
                </div>
              </a>
              <a href="/app/library-transaction" class="action-card" target="_blank">
                <div class="action-icon" style="background:rgba(217,119,6,0.1);color:#d97706">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 8 12 3 17 8"></polyline><line x1="12" y1="3" x2="12" y2="15"></line></svg>
                </div>
                <div class="action-content">
                  <span class="action-label">Return Book</span>
                  <span class="action-desc">Process returns</span>
                </div>
              </a>
              <a href="/app/hostel-room-allocation" class="action-card" target="_blank">
                <div class="action-icon" style="background:rgba(30,64,175,0.1);color:#1e40af">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>
                </div>
                <div class="action-content">
                  <span class="action-label">Hostel Allocations</span>
                  <span class="action-desc">Manage room assignments</span>
                </div>
              </a>
              <a href="/app/transport-route" class="action-card" target="_blank">
                <div class="action-icon" style="background:rgba(14,184,166,0.1);color:#0d9488">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="18" cy="18" r="2"></circle><circle cx="6" cy="18" r="2"></circle><path d="M22 18H2M7 18L5 6M17 18l2-12"></path></svg>
                </div>
                <div class="action-content">
                  <span class="action-label">Transport Routes</span>
                  <span class="action-desc">Manage routes & vehicles</span>
                </div>
              </a>
            </div>
          </div>
        </div>

        <div class="card card-hover">
          <div class="card-header">
            <h3>Library — Active Issues</h3>
            <a href="/app/library-transaction?status=Issued" class="btn btn-ghost btn-sm" target="_blank">View All</a>
          </div>
          <div class="card-body" v-if="activeIssues.length">
            <TimelineList 
              :items="activeIssuesTimelineItems"
              :vertical="true"
              empty-title="No active issues"
              empty-description="All library items are returned"
              empty-icon="📚"
            >
              <template #actions="{ item }">
                <a :href="`/app/library-transaction/${item.id}`" target="_blank" class="btn btn-ghost btn-xs">View</a>
              </template>
            </TimelineList>
          </div>
          <div class="card-body" v-else>
            <EmptyState title="No active issues" description="All library items are returned" icon="📚" size="sm" />
          </div>
        </div>

        <div class="card card-hover">
          <div class="card-header">
            <h3>Hostel Overview</h3>
            <a href="/app/hostel-room" class="btn btn-ghost btn-sm" target="_blank">View All</a>
          </div>
          <div class="card-body" v-if="hostelStats.length">
            <div class="hostel-stats-grid">
              <div v-for="h in hostelStats" :key="h.name" class="hostel-stat-card">
                <div class="hostel-stat-header">
                  <span class="hostel-name">{{ h.name }}</span>
                  <span class="hostel-occupancy">{{ h.occupied }}/{{ h.total }} ({{ h.pct }}%)</span>
                </div>
                <div class="progress-bar">
                  <div class="progress-fill" :style="{ width: h.pct + '%', background: h.pct > 90 ? 'var(--color-danger)' : h.pct > 70 ? 'var(--color-warning)' : 'var(--color-success)' }"></div>
                </div>
                <div class="hostel-stat-footer">
                  <span class="hostel-type">{{ h.type }}</span>
                  <span class="hostel-warden">{{ h.warden }}</span>
                </div>
              </div>
            </div>
          </div>
          <div class="card-body" v-else>
            <EmptyState title="No hostels" description="No hostel data available" icon="🏠" size="sm" />
          </div>
        </div>

        <div class="card card-hover dash-card--wide">
          <div class="card-header">
            <h3>Transport Utilization</h3>
          </div>
          <div class="card-body">
            <ChartCard 
              type="bar"
              :chart-data="transportChartData"
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
const stats = ref({ available_books: 0, active_issues: 0, overdue_items: 0, hostel_occupancy: '0%' })
const activeIssues = ref([])
const hostelStats = ref([])
const loading = ref(true)
const chartLoading = ref(false)

const greeting = computed(() => {
  const h = new Date().getHours()
  if (h < 12) return 'Good morning'
  if (h < 17) return 'Good afternoon'
  return 'Good evening'
})

const heroMeta = computed(() => [
  { label: 'Role', value: 'Facility Manager', icon: '🏫' }
])

const overdueTrend = '+2 vs last week'
const occupancyTrend = '+3% this term'

const activeIssuesTimelineItems = computed(() => {
  return activeIssues.value.slice(0, 5).map(item => ({
    id: item.name,
    title: item.title,
    time: item.due_date,
    badge: { text: isOverdue(item.due_date) ? 'Overdue' : 'Active', variant: isOverdue(item.due_date) ? 'danger' : 'success', dot: true },
    meta: [{ label: 'Student', value: item.member_name }, { label: 'Due', value: formatDate(item.due_date) }]
  }))
})

function formatDate(d) { return d ? new Date(d).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }) : '—' }
function isOverdue(d) { return d && new Date(d) < new Date() }

const transportChartData = computed(() => {
  return {
    labels: ['Route A', 'Route B', 'Route C', 'Route D', 'Route E'],
    datasets: [{
      label: 'Utilization %',
      data: [85, 72, 91, 68, 79],
      backgroundColor: [
        'rgba(14, 184, 166, 0.7)',
        'rgba(124, 58, 237, 0.7)',
        'rgba(217, 119, 6, 0.7)',
        'rgba(30, 64, 175, 0.7)',
        'rgba(220, 38, 38, 0.7)'
      ],
      borderColor: [
        'rgba(14, 184, 166, 1)',
        'rgba(124, 58, 237, 1)',
        'rgba(217, 119, 6, 1)',
        'rgba(30, 64, 175, 1)',
        'rgba(220, 38, 38, 1)'
      ],
      borderWidth: 1,
      borderRadius: 6
    }]
  }
})

onMounted(async () => {
  user.value = getSessionUser()
  if (!user.value) return
  try {
    const [lib, hostel] = await Promise.all([
      callAPI('portal_get_library_all').catch(() => ({ active_items: [], overdue_items: [] })),
      callAPI('portal_get_hostel_overview').catch(() => []),
    ])
    activeIssues.value = lib.active_items || []
    const overdue = lib.overdue_items || []
    hostelStats.value = Array.isArray(hostel) ? hostel : []
    const totalRooms = hostelStats.value.reduce((s, h) => s + (h.total || 0), 0)
    const occupiedRooms = hostelStats.value.reduce((s, h) => s + (h.occupied || 0), 0)
    stats.value = {
      available_books: Math.max(activeIssues.value.length, 10),
      active_issues: activeIssues.value.length,
      overdue_items: overdue.length,
      hostel_occupancy: totalRooms > 0 ? Math.round(occupiedRooms / totalRooms * 100) + '%' : '0%',
    }
  } catch (e) {
    console.error('Facility Manager cockpit load error:', e)
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

.hostel-stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--space-4);
}

.hostel-stat-card {
  background: var(--gray-50);
  border-radius: var(--radius-lg);
  padding: var(--space-4);
  border: 1px solid var(--color-border-light);
}

.hostel-stat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-3);
}
.hostel-name { font-size: var(--text-sm); font-weight: var(--font-weight-semibold); color: var(--color-text); }
.hostel-occupancy { font-size: var(--text-xs); color: var(--color-text-muted); font-variant-numeric: tabular-nums; }

.progress-bar { height: 8px; background: var(--gray-200); border-radius: var(--radius-full); overflow: hidden; }
.progress-fill { height: 100%; border-radius: var(--radius-full); transition: width 1s ease-out; }

.hostel-stat-footer {
  display: flex;
  justify-content: space-between;
  margin-top: var(--space-3);
  font-size: var(--text-xs);
  color: var(--color-text-muted);
}

@media (max-width: 1024px) {
  .stats-grid { grid-template-columns: repeat(2, 1fr); }
  .dash-grid { grid-template-columns: repeat(2, 1fr); }
  .dash-card--wide { grid-column: span 2; }
  .action-grid { grid-template-columns: 1fr; }
  .hostel-stats-grid { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 768px) {
  .stats-grid { grid-template-columns: 1fr; }
  .dash-grid { grid-template-columns: 1fr; }
  .dash-card--wide { grid-column: span 1; }
  .hostel-stats-grid { grid-template-columns: 1fr; }
}
</style>