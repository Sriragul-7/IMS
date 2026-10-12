<template>
  <div class="feedback-page">
    <PageHeader 
      title="Feedback" 
      subtitle="Submit feedback and view your history"
      :meta-items="metaItems"
    />

    <div class="feedback-grid">
      <!-- Submit Feedback Form -->
      <div class="card card-hover">
        <div class="card-header">
          <h3>Submit Feedback</h3>
        </div>
        <div class="card-body">
          <form @submit.prevent="handleSubmit">
            <div class="form-group">
              <label class="form-label">Category</label>
              <select v-model="form.feedback_type" class="form-select" required>
                <option value="">Select category...</option>
                <option value="Academic">Academic</option>
                <option value="Facility">Facility</option>
                <option value="Service">Service</option>
                <option value="General">General</option>
              </select>
            </div>
            <div class="form-group">
              <label class="form-label">Subject</label>
              <input v-model="form.subject" type="text" class="form-input" placeholder="Brief subject" required />
            </div>
            <div class="form-group">
              <label class="form-label">Message</label>
              <textarea v-model="form.message" class="form-textarea" rows="5" placeholder="Your feedback or complaint..." required></textarea>
            </div>
            <div class="form-actions">
              <span class="success-msg" v-if="success">✅ Feedback submitted successfully!</span>
              <button type="submit" class="btn btn-primary btn-lg" :disabled="submitting">
                <span v-if="submitting" class="btn-spinner">
                  <svg class="spinner" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><circle cx="12" cy="12" r="10" stroke-opacity="0.25"></circle><path d="M12 2a10 10 0 0 1 10 10" stroke-opacity="1"></path></svg>
                </span>
                {{ submitting ? 'Submitting...' : 'Submit Feedback' }}
              </button>
            </div>
          </form>
        </div>
      </div>

      <!-- Feedback History -->
      <div class="card card-hover" v-if="history.length">
        <div class="card-header">
          <h3>Your Feedback History</h3>
        </div>
        <div class="card-body">
          <TimelineList 
            :items="feedbackTimelineItems"
            :vertical="true"
            empty-title="No feedback yet"
            empty-description="Submit your first feedback above"
            empty-icon="💬"
          >
            <template #actions="{ item }">
              <router-link v-if="item.canView" :to="`/feedback/${item.id}`" class="btn btn-ghost btn-xs">View Details</router-link>
            </template>
          </TimelineList>
        </div>
      </div>
      <div class="card card-hover" v-else style="min-height: 200px;">
        <div class="card-header">
          <h3>Your Feedback History</h3>
        </div>
        <div class="card-body">
          <EmptyState title="No feedback yet" description="Submit your first feedback using the form on the left" icon="💬" size="md" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { getSessionUser, callAPI } from '../utils/api.js'
import PageHeader from '../components/PageHeader.vue'
import StatusBadge from '../components/StatusBadge.vue'
import EmptyState from '../components/EmptyState.vue'
import TimelineList from '../components/TimelineList.vue'

const user = getSessionUser()
const history = ref([])
const submitting = ref(false)
const success = ref(false)

const metaItems = computed(() => [
  { label: 'Submitted', value: history.value.length, icon: '💬' }
])

const form = reactive({
  feedback_type: '',
  subject: '',
  message: ''
})

const feedbackTimelineItems = computed(() => {
  return history.value.map(f => ({
    id: f.name,
    title: f.subject,
    time: f.raised_date,
    body: f.description,
    badge: { text: f.status, variant: fbVariant(f.status), dot: true },
    meta: [
      { label: 'Category', value: f.category },
      { label: 'Status', value: f.status }
    ],
    canView: false
  }))
})

function formatDate(d) {
  return d ? new Date(d).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }) : ''
}

function fbVariant(status) {
  const map = { Open: 'warning', 'In Progress': 'info', Resolved: 'success', Closed: 'neutral' }
  return map[status] || 'neutral'
}

async function handleSubmit() {
  submitting.value = true
  success.value = false
  try {
    await callAPI('portal_submit_feedback', {
      student: user.record_name,
      feedback_type: form.feedback_type,
      subject: form.subject,
      message: form.message,
    })
    success.value = true
    form.feedback_type = ''
    form.subject = ''
    form.message = ''
    await loadHistory()
  } catch (e) {
    alert('Error: ' + e.message)
  } finally {
    submitting.value = false
  }
}

async function loadHistory() {
  try {
    const result = await callAPI('portal_get_feedback', { student: user.record_name })
    history.value = result.feedback || []
  } catch (e) {
    console.error('Failed to load feedback:', e)
  }
}

onMounted(loadHistory)
</script>

<style scoped>
.feedback-page { animation: fadeIn var(--transition-base); }

.feedback-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-4);
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: var(--space-3);
  margin-top: var(--space-4);
}
.success-msg { color: var(--color-success); font-size: var(--text-sm); font-weight: var(--font-weight-medium); }
.btn-spinner { display: inline-flex; }
.spinner { animation: spin 0.8s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

@media (max-width: 768px) {
  .feedback-grid { grid-template-columns: 1fr; }
}
</style>