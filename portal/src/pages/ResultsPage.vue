<template>
  <div class="results-page">
    <PageHeader title="Results" subtitle="Assessment results and grades" />

    <div v-if="!loaded" class="loading-overlay"><div class="spinner spinner-lg"></div></div>

    <template v-else>
      <div v-if="!hasPublishedResults" class="publish-banner">
        <div class="banner-icon">&#9432;</div>
        <div>
          <h3>Results Not Yet Published</h3>
          <p>Assessment results for this term have not been published yet. Please check back later.</p>
        </div>
      </div>

      <div v-if="records.length" class="results-grid">
        <div v-for="r in records" :key="r.name" class="result-card">
          <div class="result-top">
            <span class="result-type-badge">{{ r.assessment_type }}</span>
            <StatusBadge :text="r.status" :variant="r.status === 'Pass' ? 'success' : 'danger'" />
          </div>
          <div class="result-course">{{ r.course_name || r.course }}</div>
          <div class="result-marks">
            <span class="marks-big">{{ r.marks_obtained }}</span>
            <span class="marks-sep">/</span>
            <span class="marks-total">{{ r.max_marks }}</span>
          </div>
          <div class="result-meta">
            <span v-if="r.grade" class="grade-badge">{{ r.grade }}</span>
            <span v-if="r.passing_marks" class="passing-info">Pass: {{ r.passing_marks }}</span>
          </div>
        </div>
      </div>

      <EmptyState v-else-if="loaded && !hasPublishedResults"
        title="No results available"
        description="Your assessment results will appear here once published"
        icon="&#9733;"
      />
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import { getSessionUser, callAPI } from '../utils/api.js'
import PageHeader from '../components/PageHeader.vue'
import StatusBadge from '../components/StatusBadge.vue'
import EmptyState from '../components/EmptyState.vue'

const props = defineProps({ selectedChild: String })
const records = ref([])
const loaded = ref(false)
const hasPublishedResults = computed(() => records.value.length > 0)

async function load() {
  const user = getSessionUser()
  if (!user) return
  const student = user.role === 'Guardian' ? (props.selectedChild || undefined) : undefined
  const result = await callAPI('portal_get_results', { student })
  records.value = result.records || []
  loaded.value = true
}

onMounted(load)
watch(() => props.selectedChild, load)
</script>

<style scoped>
.publish-banner {
  display: flex;
  align-items: flex-start;
  gap: var(--space-4);
  background: var(--color-info-light);
  border: 1px solid #93c5fd;
  border-radius: var(--radius-lg);
  padding: var(--space-5) var(--space-6);
  margin-bottom: var(--space-6);
}
.banner-icon { font-size: 1.25rem; color: var(--color-info); flex-shrink: 0; margin-top: 2px; }
.publish-banner h3 { font-size: var(--text-md); font-weight: 600; color: #1e40af; }
.publish-banner p { font-size: var(--text-sm); color: var(--color-info); margin-top: var(--space-1); }

.results-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: var(--space-4);
}

.result-card {
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  padding: var(--space-5);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--color-border-light);
  transition: box-shadow var(--transition-base);
}
.result-card:hover { box-shadow: var(--shadow-md); }

.result-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-3);
}

.result-type-badge {
  font-size: 10px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--color-text-muted);
}

.result-course {
  font-size: var(--text-md);
  font-weight: 600;
  color: var(--color-text);
  margin-bottom: var(--space-3);
}

.result-marks {
  display: flex;
  align-items: baseline;
  gap: 2px;
  margin-bottom: var(--space-3);
}
.marks-big { font-size: var(--text-3xl); font-weight: 700; color: var(--color-text); }
.marks-sep { font-size: var(--text-lg); color: var(--gray-300); }
.marks-total { font-size: var(--text-lg); color: var(--color-text-muted); }

.result-meta {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding-top: var(--space-3);
  border-top: 1px solid var(--color-border-light);
}

.grade-badge {
  display: inline-flex;
  align-items: center;
  padding: var(--space-1) var(--space-2-5);
  border-radius: var(--radius-sm);
  background: var(--color-primary-100);
  color: var(--color-primary);
  font-size: var(--text-xs);
  font-weight: 600;
}

.passing-info {
  font-size: var(--text-xs);
  color: var(--color-text-muted);
}
</style>
