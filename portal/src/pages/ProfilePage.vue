<template>
  <div class="profile-page" v-if="profile">
    <div class="profile-hero">
      <div class="hero-avatar">{{ initials }}</div>
      <div class="hero-info">
        <h2>{{ profile.student_name || profile.guardian_name }}</h2>
        <span class="hero-id">{{ profile.name }}</span>
        <span v-if="profile.type === 'student'" class="hero-program">{{ profile.program }}</span>
      </div>
    </div>

    <div class="profile-grid">
      <div class="card card-padded">
        <h4 class="section-title">Personal Information</h4>
        <div class="info-list">
          <div class="info-row" v-for="item in personalInfo" :key="item.label">
            <span class="info-label">{{ item.label }}</span>
            <span class="info-value">{{ item.value || '\u2014' }}</span>
          </div>
        </div>
      </div>

      <div class="card card-padded" v-if="profile.type === 'student'">
        <h4 class="section-title">Academic Details</h4>
        <div class="info-list">
          <div class="info-row" v-for="item in academicInfo" :key="item.label">
            <span class="info-label">{{ item.label }}</span>
            <span class="info-value">{{ item.value || '\u2014' }}</span>
          </div>
        </div>
      </div>

      <div class="card card-padded" v-if="profile.type === 'student' && profile.guardians?.length">
        <h4 class="section-title">Guardian Information</h4>
        <div v-for="g in profile.guardians" :key="g.guardian" class="guardian-card">
          <div class="guardian-avatar">{{ getInitials(g.guardian_name) }}</div>
          <div>
            <div class="guardian-name">{{ g.guardian_name }}</div>
            <div class="guardian-relation">{{ g.relation }}</div>
          </div>
        </div>
      </div>

      <div class="card card-padded" v-if="profile.type === 'guardian'">
        <h4 class="section-title">My Children</h4>
        <div v-for="c in profile.children" :key="c.student" class="child-row">
          <div class="child-avatar">{{ getInitials(c.student_name) }}</div>
          <div class="child-info">
            <span class="child-name">{{ c.student_name }}</span>
            <span class="child-program">{{ c.program }}</span>
          </div>
          <StatusBadge :text="c.status" :variant="c.status === 'Active' ? 'success' : 'neutral'" />
        </div>
      </div>
    </div>
  </div>

  <div v-else class="loading-overlay">
    <div class="spinner spinner-lg"></div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { callAPI } from '../utils/api.js'
import StatusBadge from '../components/StatusBadge.vue'

const profile = ref(null)

const initials = computed(() => {
  const name = profile.value?.student_name || profile.value?.guardian_name || '?'
  return name.split(' ').map(w => w[0]).join('').toUpperCase().slice(0, 2)
})

function getInitials(name) {
  if (!name) return '?'
  return name.split(' ').map(w => w[0]).join('').toUpperCase().slice(0, 2)
}

const personalInfo = computed(() => {
  if (!profile.value) return []
  const p = profile.value
  if (p.type === 'student') {
    return [
      { label: 'Name', value: p.student_name },
      { label: 'Email', value: p.email },
      { label: 'Gender', value: p.gender },
      { label: 'Date of Birth', value: p.date_of_birth },
      { label: 'Blood Group', value: p.blood_group },
      { label: 'Status', value: p.status },
    ]
  }
  return [
    { label: 'Name', value: p.guardian_name },
    { label: 'Email', value: p.email },
    { label: 'Mobile', value: p.mobile_phone },
  ]
})

const academicInfo = computed(() => {
  if (!profile.value || profile.value.type !== 'student') return []
  const p = profile.value
  return [
    { label: 'Program', value: p.program },
    { label: 'Academic Year', value: p.academic_year },
    { label: 'Enrollment Date', value: p.enrollment_date },
    { label: 'Status', value: p.status },
  ]
})

onMounted(async () => {
  try {
    profile.value = await callAPI('portal_get_profile')
  } catch (e) {
    console.error('Failed to load profile:', e)
  }
})
</script>

<style scoped>
.profile-hero {
  display: flex;
  align-items: center;
  gap: var(--space-6);
  background: linear-gradient(135deg, var(--color-primary) 0%, #2563eb 100%);
  color: white;
  padding: var(--space-8);
  border-radius: var(--radius-xl);
  margin-bottom: var(--space-6);
}

.hero-avatar {
  width: 72px; height: 72px;
  border-radius: var(--radius-xl);
  background: rgba(255,255,255,0.15);
  border: 2px solid rgba(255,255,255,0.25);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: var(--text-2xl);
  font-weight: 700;
  flex-shrink: 0;
}

.hero-info h2 { font-size: var(--text-2xl); font-weight: 700; margin-bottom: var(--space-1); }
.hero-id { font-size: var(--text-sm); opacity: 0.8; display: block; }
.hero-program { font-size: var(--text-sm); opacity: 0.8; display: block; margin-top: var(--space-1); }

.profile-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
  gap: var(--space-4);
}

.section-title {
  font-size: var(--text-md);
  font-weight: 600;
  margin-bottom: var(--space-4);
  padding-bottom: var(--space-3);
  border-bottom: 1px solid var(--color-border-light);
}

.info-list { display: flex; flex-direction: column; }
.info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-3) 0;
  border-bottom: 1px solid var(--color-border-light);
}
.info-row:last-child { border-bottom: none; }
.info-label { font-size: var(--text-sm); color: var(--color-text-secondary); }
.info-value { font-size: var(--text-sm); font-weight: 500; color: var(--color-text); }

.guardian-card {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3);
  background: var(--gray-50);
  border-radius: var(--radius-md);
  margin-bottom: var(--space-2);
}
.guardian-avatar {
  width: 36px; height: 36px;
  border-radius: var(--radius-full);
  background: var(--color-primary-100);
  color: var(--color-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: var(--text-xs);
  font-weight: 600;
}
.guardian-name { font-size: var(--text-sm); font-weight: 500; }
.guardian-relation { font-size: var(--text-xs); color: var(--color-text-muted); }

.child-row {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3) 0;
  border-bottom: 1px solid var(--color-border-light);
}
.child-row:last-child { border-bottom: none; }
.child-avatar {
  width: 36px; height: 36px;
  border-radius: var(--radius-full);
  background: var(--color-purple-light);
  color: var(--color-purple);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: var(--text-xs);
  font-weight: 600;
}
.child-info { flex: 1; }
.child-name { display: block; font-size: var(--text-sm); font-weight: 500; }
.child-program { font-size: var(--text-xs); color: var(--color-text-muted); }

@media (max-width: 640px) {
  .profile-hero { flex-direction: column; text-align: center; padding: var(--space-6); }
  .profile-grid { grid-template-columns: 1fr; }
}
</style>
