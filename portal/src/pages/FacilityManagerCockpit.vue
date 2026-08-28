<template>
  <div class="cockpit">
    <div v-if="loading" class="loading-overlay"><div class="spinner spinner-lg"></div></div>
    <template v-else>
      <div class="welcome-banner facility-banner">
        <div>
          <h2>Welcome, {{ user?.user_name }}!</h2>
          <p>{{ greeting }} — Facility Manager Dashboard</p>
        </div>
        <a href="/app" class="btn btn-glass" target="_blank">Open Full Admin &#8599;</a>
      </div>

      <div class="stats-grid">
        <StatCard :value="stats.available_books" label="AVAILABLE BOOKS" color="#1e40af" icon="&#128218;" />
        <StatCard :value="stats.active_issues" label="ACTIVE ISSUES" color="#d97706" icon="&#128203;" />
        <StatCard :value="stats.overdue_items" label="OVERDUE ITEMS" color="#dc2626" icon="&#9888;" />
        <StatCard :value="stats.hostel_occupancy" label="HOSTEL OCCUPANCY" color="#059669" icon="&#127968;" />
      </div>

      <div class="dash-grid">
        <div class="card">
          <div class="card-header">
            <h3>Quick Actions</h3>
          </div>
          <div class="card-body">
            <div class="action-list">
              <a href="/app/library-transaction/new" class="action-item" target="_blank">
                <span class="action-icon" style="background:rgba(5,150,105,0.1);color:#059669">&#128214;</span>
                <div class="action-text">
                  <span class="action-label">Issue Book</span>
                  <span class="action-desc">Issue a library item to a student</span>
                </div>
              </a>
              <a href="/app/library-transaction" class="action-item" target="_blank">
                <span class="action-icon" style="background:rgba(217,119,6,0.1);color:#d97706">&#128215;</span>
                <div class="action-text">
                  <span class="action-label">Return Book</span>
                  <span class="action-desc">Process library item returns</span>
                </div>
              </a>
              <a href="/app/hostel-room-allocation" class="action-item" target="_blank">
                <span class="action-icon" style="background:rgba(30,64,175,0.1);color:#1e40af">&#127968;</span>
                <div class="action-text">
                  <span class="action-label">Hostel Allocations</span>
                  <span class="action-desc">Manage room assignments</span>
                </div>
              </a>
            </div>
          </div>
        </div>

        <div class="card">
          <div class="card-header">
            <h3>Library — Active Issues</h3>
            <a href="/app/library-transaction?status=Issued" class="btn btn-ghost btn-sm" target="_blank">View All</a>
          </div>
          <div class="card-body" v-if="activeIssues.length">
            <div v-for="item in activeIssues.slice(0, 5)" :key="item.name" class="issue-row">
              <div class="issue-info">
                <span class="issue-book">{{ item.title }}</span>
                <span class="issue-member">{{ item.member_name }} — {{ item.member }}</span>
              </div>
              <div class="issue-right">
                <span class="issue-date" :class="{ overdue: isOverdue(item.due_date) }">
                  Due: {{ formatDate(item.due_date) }}
                </span>
              </div>
            </div>
          </div>
          <div class="card-body" v-else>
            <EmptyState title="No active issues" description="All library items are returned" icon="&#128218;" />
          </div>
        </div>

        <div class="card">
          <div class="card-header">
            <h3>Hostel Overview</h3>
            <a href="/app/hostel-room" class="btn btn-ghost btn-sm" target="_blank">View All</a>
          </div>
          <div class="card-body" v-if="hostelStats.length">
            <div v-for="h in hostelStats" :key="h.name" class="hostel-row">
              <div class="hostel-info">
                <span class="hostel-name">{{ h.name }}</span>
                <span class="hostel-detail">{{ h.occupied }}/{{ h.total }} rooms occupied</span>
              </div>
              <div class="hostel-bar">
                <div class="hostel-bar-fill" :style="{ width: h.pct + '%' }"></div>
              </div>
            </div>
          </div>
          <div class="card-body" v-else>
            <EmptyState title="No hostels" description="No hostel data available" icon="&#127968;" />
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
import EmptyState from '../components/EmptyState.vue'

const user = ref(null)
const stats = ref({ available_books: 0, active_issues: 0, overdue_items: 0, hostel_occupancy: '0%' })
const activeIssues = ref([])
const hostelStats = ref([])
const loading = ref(true)

const greeting = computed(() => {
  const h = new Date().getHours()
  if (h < 12) return 'Good morning'
  if (h < 17) return 'Good afternoon'
  return 'Good evening'
})

function formatDate(d) { return d ? new Date(d).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }) : '—' }
function isOverdue(d) { return d && new Date(d) < new Date() }

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
      available_books: activeIssues.value.length > 0 ? Math.max(activeIssues.value.length, 10) : 0,
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
.welcome-banner { background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%); color: white; padding: var(--space-6) var(--space-8); border-radius: var(--radius-xl); margin-bottom: var(--space-6); display: flex; justify-content: space-between; align-items: center; }
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

.issue-row { display: flex; align-items: center; justify-content: space-between; padding: var(--space-3) 0; border-bottom: 1px solid var(--color-border-light); }
.issue-row:last-child { border-bottom: none; }
.issue-info { flex: 1; min-width: 0; }
.issue-book { display: block; font-size: var(--text-sm); font-weight: 500; }
.issue-member { font-size: var(--text-xs); color: var(--color-text-muted); }
.issue-date { font-size: var(--text-xs); color: var(--color-text-muted); white-space: nowrap; }
.issue-date.overdue { color: var(--color-danger); font-weight: 600; }

.hostel-row { padding: var(--space-3) 0; border-bottom: 1px solid var(--color-border-light); }
.hostel-row:last-child { border-bottom: none; }
.hostel-info { display: flex; justify-content: space-between; align-items: center; margin-bottom: var(--space-2); }
.hostel-name { font-size: var(--text-sm); font-weight: 600; }
.hostel-detail { font-size: var(--text-xs); color: var(--color-text-muted); }
.hostel-bar { height: 6px; background: var(--gray-200); border-radius: var(--radius-full); overflow: hidden; }
.hostel-bar-fill { height: 100%; background: var(--color-primary); border-radius: var(--radius-full); transition: width 0.3s ease; }

@media (max-width: 1024px) { .stats-grid { grid-template-columns: repeat(2, 1fr); } .dash-grid { grid-template-columns: 1fr; } }
@media (max-width: 640px) { .stats-grid { grid-template-columns: 1fr; } .welcome-banner { flex-direction: column; gap: var(--space-3); } }
</style>
