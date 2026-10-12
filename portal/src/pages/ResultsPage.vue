<template>
  <div class="results-page">
    <PageHeader 
      title="Results" 
      subtitle="Assessment results and grades"
      :meta-items="metaItems"
    />

    <div v-if="loading" class="page-loading">
      <div class="stats-skeleton" style="margin-bottom: var(--space-6);">
        <Skeleton type="stat" v-for="i in 3" :key="i" />
      </div>
      <div class="results-skeleton">
        <Skeleton type="card" v-for="i in 4" :key="i" />
      </div>
    </div>

    <template v-else>
      <!-- Results Not Published Banner -->
      <div v-if="!hasPublishedResults && unpublishedCount > 0" class="publish-banner card card-gradient-info card-padded">
        <div class="banner-content">
          <div class="banner-icon">📋</div>
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
        <StatCard :value="stats.total" label="Total Assessments" color="#0f172a" icon="📋" variant="default" />
        <StatCard :value="stats.published" label="Published" color="#059669" icon="✅" variant="success" />
        <StatCard :value="stats.pending" label="Pending" color="#d97706" icon="⏳" variant="amber" />
      </div>

      <!-- Results Grid -->
      <div v-if="records.length" class="results-grid">
        <div v-for="r in records" :key="r.name" class="result-card card card-hover">
          <div class="result-header">
            <span class="result-type-badge">{{ r.assessment_type }}</span>
            <StatusBadge :text="r.status" :variant="r.status === 'Pass' ? 'success' : 'danger'" size="sm" />
          </div>
          <div class="result-course">{{ r.course_name || r.course }}</div>
          <div class="result-marks">
            <span class="marks-big">{{ r.marks_obtained }}</span>
            <span class="marks-sep">/</span>
            <span class="marks-total">{{ r.max_marks }}</span>
          </div>
          <div class="result-progress" v-if="r.max_marks > 0">
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: progressPercent(r) + '%', background: progressColor(r) }"></div>
            </div>
            <span class="progress-percent">{{ progressPercent(r) }}%</span>
          </div>
          <div class="result-meta">
            <span v-if="r.grade" class="grade-badge">{{ r.grade }}</span>
            <span v-if="r.passing_marks" class="passing-info">Pass: {{ r.passing_marks }}</span>
            <span v-if="r.assessment_date" class="assessment-date">📅 {{ formatDate(r.assessment_date) }}</span>
          </div>
        </div>
      </div>

      <!-- Empty States -->
      <div v-else-if="loaded && !hasPublishedResults" class="empty-results">
        <EmptyState 
          title="No Published Results" 
          description="Your assessment results will appear here once published by instructors."
          icon="📋"
          size="lg"
        />
      </div>
      <div v-else-if="loaded && hasPublishedResults" class="empty-results">
        <EmptyState 
          title="No Results Available" 
          description="No assessment records found for the current term."
          icon="📊"
          size="lg"
        />
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
const loaded = ref(false)
const loading = ref(true)
const stats = ref({ total: 0, published: 0, pending: 0 })

const hasPublishedResults = computed(() => records.value.length > 0)
const unpublishedCount = computed(() => unpublishedRecords.value.length)
const unpublishedRecords = computed(() => allRecords.value.filter(r => !r.published))
const allRecords = ref([])

const metaItems = computed(() => [
  { label: 'Term', value: currentTerm.value || 'Current', icon: '📅' }
])

const currentTerm = ref('Term 1 2026-27')

function formatDate(d) {
  return d ? new Date(d).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }) : ''
}

function progressPercent(r) {
  if (!r.max_marks) return 0
  return Math.round((r.marks_obtained / r.max_marks) * 100)
}

function progressColor(r) {
  const pct = progressPercent(r)
  if (pct >= 80) return 'var(--color-success)'
  if (pct >= 60) return 'var(--color-warning)'
  return 'var(--color-danger)'
}

async function load() {
  loading.value = true
  loaded.value = false
  const user = getSessionUser()
  if (!user) { loading.value = false; return }
  const student = user.role === 'Guardian' ? (props.selectedChild || undefined) : undefined
  try {
    const result = await callAPI('portal_get_results', { student })
    allRecords.value = result.records || []
    records.value = allRecords.value.filter(r => r.published)
    
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
.stats-skeleton { display: grid; grid-template-columns: repeat(3, 1fr); gap: var(--space-4); }
.results-skeleton { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: var(--space-4); }

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

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-4);
  margin-bottom: var(--space-6);
}

.results-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: var(--space-4);
}

.result-card {
  padding: var(--space-5);
  border: 1px solid var(--color-border-light);
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

.result-progress { margin-bottom: var(--space-3); }
.progress-bar { height: 6px; background: var(--gray-200); border-radius: var(--radius-full); overflow: hidden; }
.progress-fill { height: 100%; border-radius: var(--radius-full); transition: width 1s ease-out; }
.progress-percent { font-size: var(--text-xs); color: var(--color-text-muted); font-variant-numeric: tabular-nums; }

.result-meta {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: var(--space-3);
  padding-top: var(--space-3);
  border-top: 1px solid var(--color-border-light);
}

.grade-badge {
  display: inline-flex;
  align-items: center;
  padding: var(--space-1) var(--space-3);
  border-radius: var(--radius-md);
  background: var(--color-primary-100);
  color: var(--color-primary);
  font-size: var(--text-sm);
  font-weight: var(--font-weight-bold);
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