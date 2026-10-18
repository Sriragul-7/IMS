<template>
  <div class="cockpit-page">
    <div v-if="loading" class="cockpit-loading">
      <div class="skeleton skeleton--heading" style="width: 30%;"></div>
      <div class="skeleton skeleton--text" style="width: 50%; margin-top: var(--space-2);"></div>
      <div class="stats-skeleton" style="margin-top: var(--space-6);">
        <Skeleton type="stat" v-for="i in 4" :key="i" />
      </div>
    </div>

    <template v-else>
      <!-- Hero Banner - Amber for admissions -->
      <HeroBanner 
        :title="`Welcome, ${userName}!`"
        :subtitle="`${greeting} — Admissions Pipeline`"
        :meta-items="heroMeta"
        variant="success"
      >
        <template #actions>
          <button class="btn btn-primary" @click="openCreateStudent">
            <span class="icon-svg" v-html="icons.user"></span>
            Create Student
          </button>
        </template>
      </HeroBanner>

      <!-- Stat Cards -->
      <div class="stats-grid">
        <StatCard :value="stats.total_inquiries" label="Total Inquiries" color="#0f172a" :icon="icons.clipboard" variant="primary" />
        <StatCard :value="stats.open_inquiries" label="Open Inquiries" color="#d97706" :icon="icons.refresh" variant="primary" />
        <StatCard :value="stats.under_review" label="Under Review" color="#0d9488" :icon="icons.eye" variant="primary" />
        <StatCard :value="stats.approved" label="Approved" color="#059669" :icon="icons.checkCircle" variant="primary" />
      </div>

      <!-- Main Grid -->
      <div class="dash-grid">
        <!-- Create Student Form -->
        <div class="card card-hover dash-card--wide">
          <div class="card-header">
            <h3>Create Student Record</h3>
            <p class="card-desc">Admission Inquiry → Applicant → Approval → Auto Student + Guardian creation</p>
          </div>
          <div class="card-body">
            <form @submit.prevent="handleCreateStudent" class="create-student-form">
              <div class="form-row">
                <div class="form-group">
                  <label class="form-label">Applicant Name</label>
                  <input v-model="applicant_name" type="text" class="form-input" placeholder="e.g. Arjun Kumar" required />
                </div>
                <div class="form-group">
                  <label class="form-label">Program</label>
                  <select v-model="program" class="form-select" required>
                    <option value="">Select program</option>
                    <option value="B.Sc Computer Science">B.Sc Computer Science</option>
                    <option value="B.Com">B.Com</option>
                    <option value="BBA">BBA</option>
                    <option value="B.A. English">B.A. English</option>
                  </select>
                </div>
              </div>
              <div class="form-row">
                <div class="form-group">
                  <label class="form-label">Guardian Name</label>
                  <input v-model="guardian_name" type="text" class="form-input" placeholder="e.g. Rajesh Kumar" required />
                </div>
                <div class="form-group">
                  <label class="form-label">Guardian Email</label>
                  <input v-model="guardian_email" type="email" class="form-input" placeholder="guardian@demo.institution.local" required />
                </div>
              </div>
              <div class="form-group">
                <label class="form-label">Previous School</label>
                <input v-model="previous_school" type="text" class="form-input" placeholder="e.g. Delhi Public School" />
              </div>
              <div class="form-group">
                <label class="form-label">Previous School Marks (%)</label>
                <input v-model="previous_school_marks" type="number" class="form-input" placeholder="85" />
              </div>
              <button type="submit" class="btn btn-primary btn-block" :disabled="formLoading">
                {{ formLoading ? 'Creating...' : 'Create Admission Applicant' }}
              </button>
            </form>
          </div>
        </div>

        <!-- Recent Inquiries / Pipeline -->
        <div class="card card-hover">
          <div class="card-header">
            <h3>Admission Pipeline</h3>
          </div>
          <div class="card-body">
            <div class="pipeline-stages">
              <div v-for="stage in pipelineStages" :key="stage.key" class="pipeline-stage" :class="{ active: activePipelineStage === stage.key }">
                <span class="pipeline-stage-label">{{ stage.label }}</span>
                <span class="pipeline-stage-count">{{ stage.count }}</span>
              </div>
            </div>
            <div class="pipeline-arrows">
              <span v-for="(_, i) in pipelineStages.slice(0, -1)" :key="i" class="pipeline-arrow">→</span>
            </div>
            <div class="recent-inquiries" style="margin-top: var(--space-4);">
              <div v-for="inq in recentInquiries" :key="inq.name" class="inquiry-item">
                <span class="inquiry-name">{{ inq.applicant_name }}</span>
                <span class="inquiry-program">{{ inq.program }}</span>
                <StatusBadge :text="inq.status" :variant="inquiryVariant(inq.status)" size="sm" />
              </div>
            </div>
          </div>
        </div>

        <!-- Auto Enrollment Result -->
        <div v-if="enrollmentResult" class="card card-hover card-gradient-success card-padded">
          <div class="enrollment-result">
            <div class="enrollment-icon" v-html="icons.graduation"></div>
            <div>
              <h4 style="color: white; margin: 0 0 var(--space-1) 0;">Student Auto-Enrolled</h4>
              <p style="color: rgba(255,255,255,0.9); margin: 0; font-size: var(--text-sm);">
                {{ enrollmentResult.student_name }} ({{ enrollmentResult.student_id }}) created and linked to guardian {{ enrollmentResult.guardian_name }}
              </p>
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
import { icons } from '../utils/icons.js'
import StatCard from '../components/StatCard.vue'
import StatusBadge from '../components/StatusBadge.vue'
import EmptyState from '../components/EmptyState.vue'
import HeroBanner from '../components/HeroBanner.vue'
import Skeleton from '../components/Skeleton.vue'

const user = ref(null)
const userName = computed(() => user.value?.user_name || 'Admissions Officer')
const stats = ref({ total_inquiries: 0, open_inquiries: 0, under_review: 0, approved: 0 })
const recentInquiries = ref([])
const loading = ref(true)
const formLoading = ref(false)
const enrollmentResult = ref(null)
const activePipelineStage = ref('open')

const greeting = computed(() => {
  const h = new Date().getHours()
  if (h < 12) return 'Good morning'
  if (h < 17) return 'Good afternoon'
  return 'Good evening'
})

const heroMeta = computed(() => [
  { label: 'Department', value: 'Admissions', icon: icons.building },
  { label: 'Role', value: 'Admissions Officer', icon: icons.clipboard }
])

const pipelineStages = computed(() => [
  { key: 'open', label: 'Open', count: stats.value.total_inquiries || 0 },
  { key: 'applied', label: 'Applied', count: stats.value.open_inquiries || 0 },
  { key: 'review', label: 'Under Review', count: stats.value.under_review || 0 },
  { key: 'approved', label: 'Approved', count: stats.value.approved || 0 },
])

const applicant_name = ref('')
const program = ref('')
const guardian_name = ref('')
const guardian_email = ref('')
const previous_school = ref('')
const previous_school_marks = ref('')

const inquiryVariant = (status) => {
  const map = { Open: 'warning', Converted: 'success', Closed: 'danger', 'Follow-up': 'info', Rejected: 'danger' }
  return map[status] || 'neutral'
}

function openCreateStudent() {
  // Scroll to form if needed
  const formEl = document.querySelector('.create-student-form')
  if (formEl) formEl.scrollIntoView({ behavior: 'smooth' })
}

async function handleCreateStudent() {
  formLoading.value = true
  try {
    // Simulate creating admission applicant
    await new Promise(r => setTimeout(r, 1000))
    
    // Auto-enrollment result
    enrollmentResult.value = {
      student_name: applicant_name.value || 'New Student',
      student_id: 'STU-2026-00' + Math.floor(Math.random() * 90 + 10),
      guardian_name: guardian_name.value || 'Guardian',
    }
    
    stats.value.approved += 1
    applicant_name.value = ''
    program.value = ''
    guardian_name.value = ''
    guardian_email.value = ''
    previous_school.value = ''
    previous_school_marks.value = ''
    
    alert('Student applicant created and approved! Student and Guardian records auto-created.')
  } catch (e) {
    alert('Error creating student: ' + e.message)
  } finally {
    formLoading.value = false
  }
}

onMounted(async () => {
  user.value = getSessionUser()
  if (!user.value) return
  try {
    stats.value = {
      total_inquiries: 18,
      open_inquiries: 6,
      under_review: 4,
      approved: 8,
    }
    recentInquiries.value = [
      { applicant_name: 'Arjun Kumar', program: 'B.Sc Computer Science', status: 'Open', name: 'INQ001' },
      { applicant_name: 'Shruti Agarwal', program: 'B.Com', status: 'Converted', name: 'INQ002' },
      { applicant_name: 'Karthik S', program: 'BBA', status: 'Under Review', name: 'INQ003' },
      { applicant_name: 'Divya Nair', program: 'B.A. English', status: 'Follow-up', name: 'INQ004' },
    ]
  } catch (e) {
    console.error('Admissions cockpit load error:', e)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.cockpit-page { animation: fadeIn var(--transition-base); }
.cockpit-loading { padding: var(--space-6); }
.stats-skeleton { display: grid; grid-template-columns: repeat(4, 1fr); gap: var(--space-4); }

.dash-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--space-4);
}

.dash-card--wide {
  grid-column: span 2;
}

.card-desc {
  font-size: var(--text-sm);
  color: var(--color-text-muted);
  margin: var(--space-1) 0 var(--space-4) 0;
}

.create-student-form { display: flex; flex-direction: column; gap: var(--space-3); }
.form-row { display: grid; grid-template-columns: repeat(2, 1fr); gap: var(--space-3); }

.pipeline-stages {
  display: flex;
  justify-content: space-between;
  margin-bottom: var(--space-4);
}
.pipeline-stage {
  text-align: center;
  flex: 1;
  padding: var(--space-3) var(--space-2);
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-border-light);
  background: var(--color-surface);
}
.pipeline-stage.active {
  background: var(--role-active-gradient-subtle);
  border-color: var(--role-active-accent);
}
.pipeline-stage-label {
  font-size: var(--text-xs);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-secondary);
  display: block;
  margin-bottom: var(--space-1);
}
.pipeline-stage.active .pipeline-stage-label { color: var(--role-active-accent); }
.pipeline-stage-count {
  font-size: var(--text-xl);
  font-weight: var(--font-weight-bold);
  color: var(--color-text);
}
.pipeline-stage.active .pipeline-stage-count { color: var(--role-active-accent); }

.pipeline-arrows {
  display: flex;
  justify-content: center;
  gap: var(--space-2);
  margin-bottom: var(--space-2);
}
.pipeline-arrow {
  color: var(--color-text-muted);
  font-weight: var(--font-weight-bold);
}

.recent-inquiries { display: flex; flex-direction: column; gap: var(--space-2); }
.inquiry-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-3);
  border-radius: var(--radius-md);
  border: 1px solid var(--color-border-light);
  background: var(--color-surface);
}
.inquiry-name { font-size: var(--text-sm); font-weight: var(--font-weight-semibold); color: var(--color-text); }
.inquiry-program { font-size: var(--text-xs); color: var(--color-text-muted); }

.enrollment-result {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}
.enrollment-icon {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-lg);
  background: rgba(255, 255, 255, 0.15);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.enrollment-icon :deep(svg) {
  width: 28px;
  height: 28px;
}

.card-gradient-success {
  background: linear-gradient(135deg, #059669 0%, #047857 100%);
  border: none;
  color: white;
}

@media (max-width: 768px) {
  .dash-grid { grid-template-columns: 1fr; }
  .dash-card--wide { grid-column: span 1; }
  .form-row { grid-template-columns: 1fr; }
  .pipeline-stages { gap: var(--space-1); }
  .pipeline-stage { padding: var(--space-2); }
}
</style>
