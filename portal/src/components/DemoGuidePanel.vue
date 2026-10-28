<template>
  <div class="demo-guide-overlay" @click.self="close">
    <div class="demo-guide-panel">
      <div class="demo-guide-header">
        <h3>Demo Guide</h3>
        <button class="btn-icon" @click="close" aria-label="Close demo guide">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
      </div>
      <div class="demo-guide-content">
        <div class="demo-guide-section">
          <h4>Recommended Demo Flow</h4>
          <ol class="demo-flow-steps">
            <li v-for="(step, i) in demoFlow" :key="i" :class="{ active: currentStep === i }">
              <span class="step-number">{{ i + 1 }}</span>
              <span class="step-text">{{ step }}</span>
            </li>
          </ol>
        </div>
        <div class="demo-guide-section">
          <h4>Current Screen: {{ currentScreenTitle }}</h4>
          <p class="screen-desc" v-if="screenDescription">{{ screenDescription }}</p>
          <ul class="talking-points" v-if="talkingPoints.length">
            <li v-for="(point, i) in talkingPoints" :key="i">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="point-icon">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
              <span>{{ point }}</span>
            </li>
          </ul>
          <p class="no-points" v-else>No specific talking points for this screen.</p>
        </div>
        <div class="demo-guide-section">
          <h4>Quick Actions</h4>
          <div class="quick-actions-grid">
            <button class="btn btn-secondary btn-sm" @click="goToLogin">Back to Login</button>
            <button class="btn btn-accent btn-sm" @click="switchRole">Switch Role</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits, computed } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps({
  currentRoute: { type: String, default: '' },
  userRole: { type: String, default: '' }
})

const emit = defineEmits(['close'])
const router = useRouter()

const demoFlow = [
  'Login page (role cards)',
  'Admin mission control',
  'Admissions pipeline',
  'Academic Head overview',
  'Instructor (attendance/marks)',
  'Fee Manager',
  'Facility Manager',
  'Communication Officer',
  'Student portal (dashboard, results, fees)',
  'Guardian child switcher',
  'Back to Admin'
]

const currentStep = computed(() => {
  const routeMap = {
    'login': 0,
    'admin-cockpit': 1,
    'admissions-cockpit': 2,
    'academichead-cockpit': 3,
    'instructor-cockpit': 4,
    'feemanager-cockpit': 5,
    'facilitymanager-cockpit': 6,
    'communication-cockpit': 7,
    'dashboard': 8,
    'profile': 8,
    'attendance': 8,
    'results': 8,
    'fees': 8,
    'library': 8,
    'notices': 8,
    'feedback': 8,
    'guardian-dashboard': 9,
  }
  return routeMap[props.currentRoute] || 0
})

const screenInfo = computed(() => {
  const info = {
    'login': {
      title: 'Login Page',
      description: 'Split layout with branded left panel and clean form. Demo role cards auto-fill credentials.',
      points: [
        'Branded left panel with BIT logo, tagline, and 6 feature highlights',
        'Clean right panel with email/password form and password visibility toggle',
        '14 demo role cards - click any to auto-fill and login instantly',
        'No external dependencies - all fonts/icons self-hosted'
      ]
    },
    'admin-cockpit': {
      title: 'Admin Cockpit - Mission Control',
      description: 'Institution-wide aggregate view across all modules with stats, charts, and quick access.',
      points: [
        '8 stat cards covering students, staff, attendance, fees, programs, courses, feedback, library',
        'Enrollment trend chart (6 months) and fee health donut chart',
        'Module usage tiles and system status panel with color-coded indicators',
        'Quick access grid to all 8 Desk modules - each opens full CRUD in new tab'
      ]
    },
    'admissions-cockpit': {
      title: 'Admissions Cockpit',
      description: 'Visual pipeline funnel with inquiry counts and recent applicant cards.',
      points: [
        '4-stage pipeline: Open → Applied → Under Review → Approved/Rejected with counts',
        'Recent inquiries list with status badges (Open=amber, Converted=green, Closed=gray)',
        'Quick actions: New Inquiry, New Applicant, Review Applicants → all open Desk forms',
        'Auto-creation of Student + Guardian records on approval (show in Desk)'
      ]
    },
    'academichead-cockpit': {
      title: 'Academic Head Cockpit',
      description: 'Cross-module academic overview with program distribution and exam performance.',
      points: [
        'Program-wise student distribution chart (donut) and attendance by group (bar)',
        'Exam performance trend line chart across 3 assessments',
        'Quick navigation to Programs, Courses, Student Groups, Course Schedules',
        'Attendance overview with color-coded badges (green ≥80%, amber ≥60%, red <60%)'
      ]
    },
    'instructor-cockpit': {
      title: 'Instructor Cockpit',
      description: 'Today\'s timetable, pending marks, and class strength with quick actions.',
      points: [
        'Today\'s classes timeline with status badges (Ongoing=green, Upcoming=blue, Completed=gray)',
        'Pending marks entry list with due dates and direct "Enter Marks" Desk links',
        'Class strength chart showing enrollment per assigned group',
        'Quick actions: Mark Attendance, Enter Marks, Assessment Plans → Desk'
      ]
    },
    'feemanager-cockpit': {
      title: 'Fee Manager Cockpit',
      description: 'Collection vs outstanding donut, monthly trend, top defaulters, pending discounts.',
      points: [
        'Collection vs Outstanding donut chart with exact amounts',
        'Monthly fee collection bar chart (last 6 months) showing seasonal trends',
        'Top defaulters list with outstanding amounts and overdue days',
        'Pending discount approvals with Review buttons opening Desk'
      ]
    },
    'facilitymanager-cockpit': {
      title: 'Facility Manager Cockpit',
      description: 'Library circulation, hostel occupancy, and transport utilization.',
      points: [
        'Library stats: available books, active issues, overdue items (red badge)',
        'Hostel occupancy bars per hostel with capacity vs occupied progress rings',
        'Transport route utilization bars with vehicle capacity and current load',
        'Quick actions: Issue Book, Return Book, Hostel Allocations → Desk'
      ]
    },
    'communication-cockpit': {
      title: 'Communication Cockpit',
      description: 'Recent notices feed and open feedback queue with status chips.',
      points: [
        'Recent notices with category tags and publish dates',
        'Open feedback queue with status badges (Open=amber, In Progress=blue, Resolved=green)',
        'Quick actions: Create Notice, All Notices, Communication Logs → Desk',
        'Notice audience targeting demo: All / Program-wise / Group-wise'
      ]
    },
    'dashboard': {
      title: 'Student Dashboard',
      description: 'Hero banner with semester, 4 stat cards, attendance donut, upcoming classes, notices, fees, quick links.',
      points: [
        'Hero banner with greeting, date, and semester/program meta chips',
        '4 stat cards: Attendance %, CGPA, Fee Outstanding, Library Books - all with trend chips',
        'Attendance donut with breakdown (Present/Absent/Late/Excused) and today\'s classes timeline',
        'Results gating banner (blue) when assessments not yet published - key feature!'
      ]
    },
    'guardian-dashboard': {
      title: 'Guardian Portal - Child Switcher',
      description: 'Prominent card strip at top for switching between children with avatar, name, program.',
      points: [
        'Child switcher as card strip (not dropdown) - avatar, name, program, active highlight',
        'All dashboard data updates instantly when switching children',
        'Each child\'s data properly isolated via User Permissions',
        'Works across Attendance, Results, Fees, Library, Notices, Feedback'
      ]
    }
  }
  return info[props.currentRoute] || { title: props.currentRoute, description: '', points: [] }
})

const currentScreenTitle = computed(() => screenInfo.value.title)
const screenDescription = computed(() => screenInfo.value.description)
const talkingPoints = computed(() => screenInfo.value.points)

function close() {
  emit('close')
}

function goToLogin() {
  close()
  router.push({ name: 'login' })
}

function switchRole() {
  close()
  // Logout and redirect to login
  localStorage.removeItem('institution_portal_user')
  router.push({ name: 'login' })
}
</script>

<style scoped>
.demo-guide-overlay {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.5);
  z-index: var(--z-modal-backdrop);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-4);
  animation: fadeIn var(--transition-base);
}
.demo-guide-panel {
  width: 100%;
  max-width: 480px;
  max-height: 90vh;
  background: var(--color-surface);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-2xl);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  animation: slideUp var(--transition-base);
}
.demo-guide-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-4) var(--space-6);
  border-bottom: 1px solid var(--color-border-light);
}
.demo-guide-header h3 {
  font-size: var(--text-lg);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text);
}
.demo-guide-content {
  padding: var(--space-6);
  overflow-y: auto;
  flex: 1;
}
.demo-guide-section {
  margin-bottom: var(--space-6);
}
.demo-guide-section:last-child { margin-bottom: 0; }
.demo-guide-section h4 {
  font-size: var(--text-sm);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: var(--space-3);
}

.demo-flow-steps {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}
.demo-flow-steps li {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-2) var(--space-3);
  border-radius: var(--radius-md);
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  transition: all var(--transition-fast);
}
.demo-flow-steps li.active {
  background: var(--color-accent-50);
  color: var(--color-accent);
  font-weight: var(--font-weight-medium);
}
.step-number {
  width: 24px;
  height: 24px;
  border-radius: var(--radius-full);
  background: var(--gray-200);
  color: var(--gray-600);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: var(--text-xs);
  font-weight: var(--font-weight-bold);
  flex-shrink: 0;
}
.demo-flow-steps li.active .step-number {
  background: var(--color-accent);
  color: white;
}

.screen-desc {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  margin-bottom: var(--space-3);
  line-height: var(--leading-relaxed);
}

.talking-points {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}
.talking-points li {
  display: flex;
  align-items: flex-start;
  gap: var(--space-2);
  font-size: var(--text-sm);
  color: var(--color-text);
  line-height: var(--leading-relaxed);
}
.point-icon {
  color: var(--color-accent);
  flex-shrink: 0;
  margin-top: 2px;
}
.no-points {
  font-size: var(--text-sm);
  color: var(--color-text-muted);
  font-style: italic;
}

.quick-actions-grid {
  display: flex;
  gap: var(--space-2);
}

@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes slideUp { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }
</style>