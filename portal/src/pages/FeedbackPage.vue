<template>
  <div class="feedback-page">
    <PageHeader title="Feedback" subtitle="Submit feedback and view your history" />

    <div class="feedback-grid">
      <div class="card card-padded">
        <h4 class="section-title">Submit Feedback</h4>
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
            <textarea v-model="form.message" class="form-textarea" rows="4" placeholder="Your feedback or complaint..." required></textarea>
          </div>
          <div class="form-actions">
            <span class="success-msg" v-if="success">Feedback submitted successfully!</span>
            <button type="submit" class="btn btn-primary" :disabled="submitting">
              {{ submitting ? 'Submitting...' : 'Submit Feedback' }}
            </button>
          </div>
        </form>
      </div>

      <div class="card card-padded" v-if="history.length">
        <h4 class="section-title">Your History</h4>
        <div class="history-list">
          <div v-for="f in history" :key="f.name" class="history-item">
            <div class="history-top">
              <span class="history-category">{{ f.category }}</span>
              <StatusBadge :text="f.status" :variant="fbVariant(f.status)" />
            </div>
            <div class="history-subject">{{ f.subject }}</div>
            <div class="history-desc">{{ f.description }}</div>
            <div class="history-date">{{ formatDate(f.raised_date) }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { getSessionUser, callAPI } from '../utils/api.js'
import PageHeader from '../components/PageHeader.vue'
import StatusBadge from '../components/StatusBadge.vue'

const user = getSessionUser()
const history = ref([])
const submitting = ref(false)
const success = ref(false)

const form = reactive({
  feedback_type: '',
  subject: '',
  message: '',
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
.feedback-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-4);
}

.section-title {
  font-size: var(--text-md);
  font-weight: 600;
  margin-bottom: var(--space-5);
  padding-bottom: var(--space-3);
  border-bottom: 1px solid var(--color-border-light);
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: var(--space-3);
  margin-top: var(--space-4);
}
.success-msg { color: var(--color-success); font-size: var(--text-sm); font-weight: 500; }

.history-list {
  display: flex;
  flex-direction: column;
}

.history-item {
  padding: var(--space-4) 0;
  border-bottom: 1px solid var(--color-border-light);
}
.history-item:last-child { border-bottom: none; }

.history-top {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  margin-bottom: var(--space-2);
}
.history-category {
  font-size: 10px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--color-purple);
  background: var(--color-purple-light);
  padding: 2px var(--space-2);
  border-radius: var(--radius-full);
}

.history-subject {
  font-size: var(--text-md);
  font-weight: 600;
  color: var(--color-text);
  margin-bottom: var(--space-1);
}
.history-desc {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  line-height: var(--leading-relaxed);
}
.history-date {
  font-size: var(--text-xs);
  color: var(--color-text-muted);
  margin-top: var(--space-2);
}

@media (max-width: 768px) {
  .feedback-grid { grid-template-columns: 1fr; }
}
</style>
