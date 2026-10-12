<template>
  <div class="results-page">
    <PageHeader
      title="Results and Fees"
      subtitle="Semester 4 results (published) and current fee statement"
      :meta-items="metaItems"
    />

    <div v-if="loading" class="page-loading">
      <div class="stats-grid">
        <Skeleton type="stat" v-for="i in 3" :key="i" />
      </div>
      <div class="results-grid">
        <Skeleton type="card" v-for="i in 6" :key="i" />
      </div>
      <div class="card card-hover" style="margin-top: var(--space-6)">
        <Skeleton type="card" style="height: 300px;" />
      </div>
    </div>

    <template v-else>
      <!-- Results Not Published Banner -->
      <div v-if="!hasPublishedResults && unpublishedCount > 0" class="publish-banner card card-gradient-info card-padded">
        <div class="banner-content">
          <div class="banner-icon">RS</div>
          <div class="banner-text">
            <h3>Results Not Yet Published</h3>
            <p>{{ unpublishedCount }} assessment{{ unpublishedCount > 1 ? 's' : '' }} pending publication. Results will appear here once published by your instructors.</p>
          </div>
        </div>
        <div class="banner-action">
          <span class="banner-note">Check back after exams</span>
        </div>
      </div>

      <!-- Results Summary Stats -->
      <div class="stats-grid" v-if="stats">
        <StatCard :value="stats.total" label="Total Assessments" color="#0f172a" icon="AS" variant="primary" />
        <StatCard :value="stats.published" label="Published" color="#059669" icon="PU" variant="primary" />
        <StatCard :value="stats.pending" label="Pending" color="#d97706" icon="PE" variant="primary" />
      </div>

      <!-- Results Grid -->
      <div v-if="records.length" class="results-grid">
        <div v-for="r in records" :key="r.name" class="result-card card card-hover">
          <div class="result-header">
            <span class="result-type-badge">{{ r.assessment_type }}</span>
            <StatusBadge :text="r.status" :variant="r.status === 'Pass' ? 'success' : 'danger'" size="sm" />
          </div>
          <div class="result-course">{{ r.course_name || r.course }}</div>
          <div class="result-course-code">{{ r.course_code || '' }}</div>
          <div class="result-marks">
            <span class="marks-big">{{ r.marks_obtained }}</span>
            <span class="marks-sep">/</span>
            <span class="marks-total">{{ r.max_marks }}</span>
          </div>
          <div class="result-grade-badge" :style="{ background: gradeBadgeBg(r.grade), color: gradeBadgeText(r.grade) }">
            {{ r.grade }}
          </div>
          <div class="result-meta">
            <span class="grade-text">{{ gradeLabel(r.grade) }}</span>
            <span v-if="r.passing_marks" class="passing-info">Pass: {{ r.passing_marks }}</span>
            <span v-if="r.assessment_date" class="assessment-date">{{ formatDate(r.assessment_date) }}</span>
          </div>
        </div>
      </div>

      <!-- Empty States -->
      <div v-else-if="loaded && !hasPublishedResults" class="empty-results">
        <EmptyState title="No Published Results" description="Your assessment results will appear here once published by instructors." icon="RS" size="lg" />
      </div>
      <div v-else-if="loaded && hasPublishedResults" class="empty-results">
        <EmptyState title="No Results Available" description="No assessment records found for the current term." icon="NR" size="lg" />
      </div>

      <!-- Fee Statement Table -->
      <div v-if="fees.length" class="card card-hover" style="margin-top: var(--space-6)">
        <div class="card-header">
          <h3>Fee statement · 2026-27</h3>
          <a href="#" class="btn btn-outline btn-sm">Download receipt</a>
        </div>
        <div class="card-body">
          <div class="table-wrapper">
            <table class="data-table">
              <thead>
                <tr>
                  <th>Fee category</th>
                  <th class="text-right">Total</th>
                  <th class="text-right">Paid</th>
                  <th class="text-right">Discount</th>
                  <th class="text-right">Outstanding</th>
                  <th>Due date</th>
                  <th class="text-right">Status</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="f in fees" :key="f.name">
                  <td class="font-medium">{{ f.fee_schedule || f.name }}</td>
                  <td class="text-right font-mono">{{ formatCurrency(f.total_amount) }}</td>
                  <td class="text-right font-mono">{{ formatCurrency(f.paid_amount) }}</td>
                  <td class="text-right font-mono">{{ formatCurrency(f.discount_amount || 0) }}</td>
                  <td class="text-right font-mono">{{ formatCurrency(f.outstanding_amount) }}</td>
                  <td>{{ formatDate(f.due_date) }}</td>
                  <td class="text-right">
                    <StatusBadge :text="f.status" :variant="feeStatusVariant(f.status)" size="sm" />
                  </td>
                </tr>
              </tbody>
              <tfoot>
                <tr>
                  <td class="font-semibold">Total outstanding</td>
                  <td class="text-right" colspan="5"></td>
                  <td class="text-right font-semibold font-mono">{{ formatCurrency(totalOutstanding) }}</td>
                </tr>
              </tfoot>
            </table>
          </div>
        </div>
      </div>

      <div v-else class="card card-hover" style="margin-top: var(--space-6)">
        <div class="card-body card-padded">
          <EmptyState title="No fees" description="No fee records found for the current term" icon="FE" size="md" />
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { getSessionUser, callAPI } from '../utils/api.js'
import PageHeader from '../components/PageHeader.vue'
import StatCard from '../components/StatCard.vue'
import StatusBadge from '../components/StatusBadge.vue'
import EmptyState from '../components/EmptyState.vue'
import Skeleton from '../components/Skeleton.vue'

const props = defineProps({ selectedChild: String })
const records = ref([])
const allRecords = ref([])
const fees = ref([])
const loading = ref(true)
const loaded = ref(false)
const stats = ref({ total: 0, published: 0, pending: 0 })

const hasPublishedResults = computed(() => records.value.length > 0)
const unpublishedCount = computed(() => unpublishedRecords.value.length)
const unpublishedRecords = computed(() => allRecords.value.filter(r => !r.published))

const metaItems = computed(() => [
  { label: 'CGPA', value: '8.65', icon: 'CG' },
  { label: 'Semester', value: '4', icon: 'SM' }
])

function formatDate(d) {
  return d ? new Date(d).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }) : ''
}

function formatCurrency(v) {
  return '₹' + Number(v || 0).toLocaleString('en-IN', { minimumFractionDigits: 0 })
}

function gradeBadgeBg(grade) {
  const map = {
    'O': '#059669',
    'A+': '#059669',
    'A': '#2563eb',
    'B+': '#7c3aed',
    'B': '#d97706',
    'C': '#dc2626',
    'D': '#dc2626',
    'F': '#dc2626',
  }
  return map[grade] || '#0f172a'
}

function gradeBadgeText(grade) {
  return '#ffffff'
}

function gradeLabel(grade) {
  const map = {
    'O': 'Outstanding',
    'A+': 'Excellent',
    'A': 'Very Good',
    'B+': 'Good',
    'B': 'Average',
    'C': 'Below Average',
    'D': 'Poor',
    'F': 'Fail',
  }
  return map[grade] || grade
}

function feeStatusVariant(status) {
  const map = { Paid: 'success', Partial: 'warning', Unpaid: 'danger', Overdue: 'danger' }
  return map[status] || 'neutral'
}

const totalOutstanding = computed(() =>
  fees.value.reduce((s, f) => s + (f.outstanding_amount || 0), 0)
)

async function load() {
  loading.value = true
  loaded.value = false
  const user = getSessionUser()
  if (!user) { loading.value = false; return }
  const student = user.role === 'Guardian' ? (props.selectedChild || undefined) : undefined
  try {
    const [resResult, feeResult] = await Promise.all([
      callAPI('portal_get_results', { student }),
      callAPI('portal_get_fees', { student }),
    ])
    allRecords.value = resResult.records || []
    records.value = allRecords.value.filter(r => r.published)
    fees.value = feeResult.fees || []

    stats.value = {
      total: allRecords.value.length,
      published: records.value.length,
      pending: unpublishedRecords.value.length
    }
  } catch (e) {
    console.error('Results load error:', e)
  } finally {
    loaded.value = true
    loading.value = false
  }
}

onMounted(load)
watch(() => props.selectedChild, load)
</script>

<style scoped>
.results-page { animation: fadeIn var(--transition-base); }
.page-loading { padding: var(--space-6); }
.stats-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: var(--space-4); margin-bottom: var(--space-6); }
.results-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: var(--space-4); }

.publish-banner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-4);
  margin-bottom: var(--space-6);
  border-radius: var(--radius-xl);
  border: none;
}
.banner-content { display: flex; align-items: flex-start; gap: var(--space-4); }
.banner-icon { font-size: 2rem; flex-shrink: 0; }
.banner-text h3 { font-size: var(--text-lg); font-weight: var(--font-weight-bold); color: white; margin-bottom: var(--space-1); }
.banner-text p { font-size: var(--text-sm); color: rgba(255,255,255,0.9); }
.banner-action { flex-shrink: 0; }
.banner-note { font-size: var(--text-sm); color: rgba(255,255,255,0.8); padding: var(--space-2) var(--space-4); background: rgba(255,255,255,0.15); border-radius: var(--radius-full); }

.result-card {
  padding: var(--space-5);
  border: 1px solid var(--color-border-light);
  background: var(--color-surface);
}
.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-3);
}
.result-type-badge {
  font-size: 10px;
  font-weight: var(--font-weight-semibold);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--color-text-muted);
}
.result-course {
  font-size: var(--text-md);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text);
  margin-bottom: var(--space-1);
}
.result-course-code {
  font-size: var(--text-xs);
  color: var(--color-text-muted);
  margin-bottom: var(--space-3);
}
.result-marks {
  display: flex;
  align-items: baseline;
  gap: 2px;
  margin-bottom: var(--space-3);
}
.marks-big { font-size: var(--text-4xl); font-weight: var(--font-weight-bold); color: var(--color-text); font-variant-numeric: tabular-nums; }
.marks-sep { font-size: var(--text-xl); color: var(--gray-300); }
.marks-total { font-size: var(--text-xl); color: var(--color-text-muted); }

.result-grade-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: var(--radius-md);
  font-size: var(--text-lg);
  font-weight: var(--font-weight-bold);
  margin-bottom: var(--space-3);
}
.result-meta {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: var(--space-3);
  padding-top: var(--space-3);
  border-top: 1px solid var(--color-border-light);
}
.grade-text {
  font-size: var(--text-sm);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-secondary);
}
.passing-info { font-size: var(--text-xs); color: var(--color-text-muted); }
.assessment-date { font-size: var(--text-xs); color: var(--color-text-muted); }

.empty-results { padding: var(--space-8); }

@media (max-width: 768px) {
  .stats-grid { grid-template-columns: 1fr; }
  .results-grid { grid-template-columns: 1fr; }
  .publish-banner { flex-direction: column; text-align: center; }
  .banner-action { margin-top: var(--space-3); }
}
</style>