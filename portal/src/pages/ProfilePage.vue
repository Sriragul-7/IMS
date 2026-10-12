<template>
  <div class="profile-page" v-if="profile">
    <HeroBanner 
      :title="profile.student_name || profile.guardian_name"
      :subtitle="profile.type === 'student' ? profile.program : 'Guardian'"
      :compact="true"
      variant="primary"
    >
      <template #actions>
        <div class="hero-avatar-large">
          <AvatarChip :name="profile.student_name || profile.guardian_name" size="2xl" :color-index="getColorIndex(profile.email)" />
        </div>
      </template>
    </HeroBanner>

    <div class="profile-grid">
      <div class="card card-hover card-padded">
        <h4 class="section-title">Personal Information</h4>
        <div class="info-list">
          <div class="info-row" v-for="item in personalInfo" :key="item.label">
            <span class="info-label">{{ item.label }}</span>
            <span class="info-value">{{ item.value || '—' }}</span>
          </div>
        </div>
      </div>

      <div class="card card-hover card-padded" v-if="profile.type === 'student'">
        <h4 class="section-title">Academic Details</h4>
        <div class="info-list">
          <div class="info-row" v-for="item in academicInfo" :key="item.label">
            <span class="info-label">{{ item.label }}</span>
            <span class="info-value">{{ item.value || '—' }}</span>
          </div>
        </div>
      </div>

      <div class="card card-hover card-padded" v-if="profile.type === 'student' && profile.guardians?.length">
        <h4 class="section-title">Guardian Information</h4>
        <div v-for="g in profile.guardians" :key="g.guardian" class="guardian-card">
          <AvatarChip :name="g.guardian_name" size="sm" :color-index="getColorIndex(g.guardian)" class="guardian-avatar" />
          <div>
            <div class="guardian-name">{{ g.guardian_name }}</div>
            <div class="guardian-relation">{{ g.relation }}</div>
          </div>
        </div>
      </div>

      <div class="card card-hover card-padded" v-if="profile.type === 'guardian'">
        <h4 class="section-title">My Children</h4>
        <div v-for="c in profile.children" :key="c.student" class="child-row">
          <AvatarChip :name="c.student_name" size="sm" :color-index="getColorIndex(c.student)" class="child-avatar" />
          <div class="child-info">
            <span class="child-name">{{ c.student_name }}</span>
            <span class="child-program">{{ c.program }}</span>
          </div>
          <StatusBadge :text="c.status" :variant="c.status === 'Active' ? 'success' : 'neutral'" size="sm" />
        </div>
      </div>
    </div>
  </div>

  <div v-else class="page-loading">
    <div class="skeleton skeleton--heading" style="width: 30%;"></div>
    <div class="skeleton skeleton--text" style="width: 50%; margin-top: var(--space-2);"></div>
    <div class="stats-skeleton" style="margin-top: var(--space-6);">
      <Skeleton type="card" v-for="i in 3" :key="i" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { callAPI } from '../utils/api.js'
import StatusBadge from '../components/StatusBadge.vue'
import HeroBanner from '../components/HeroBanner.vue'
import AvatarChip from '../components/AvatarChip.vue'
import Skeleton from '../components/Skeleton.vue'

const profile = ref(null)

const personalInfo = computed(() => {
  if (!profile.value) return []
  const p = profile.value
  if (p.type === 'student') {
    return [
      { label: 'Name', value: p.student_name },
      { label: 'Student ID', value: p.name },
      { label: 'Email', value: p.email },
      { label: 'Gender', value: p.gender },
      { label: 'Date of Birth', value: p.date_of_birth ? new Date(p.date_of_birth).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' }) : '—' },
      { label: 'Blood Group', value: p.blood_group },
      { label: 'Status', value: p.status },
      { label: 'Phone', value: p.phone_number }
    ]
  }
  return [
    { label: 'Name', value: p.guardian_name },
    { label: 'Guardian ID', value: p.name },
    { label: 'Email', value: p.email },
    { label: 'Mobile', value: p.mobile_phone },
    { label: 'Phone', value: p.phone_number },
    { label: 'Occupation', value: p.occupation },
    { label: 'Relation', value: p.relation_to_student }
  ]
})

const academicInfo = computed(() => {
  if (!profile.value || profile.value.type !== 'student') return []
  const p = profile.value
  return [
    { label: 'Program', value: p.program },
    { label: 'Academic Year', value: p.academic_year },
    { label: 'Semester', value: p.semester },
    { label: 'Enrollment Date', value: p.enrollment_date ? new Date(p.enrollment_date).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' }) : '—' },
    { label: 'Status', value: p.status },
    { label: 'Previous School', value: p.previous_school }
  ]
})

function getColorIndex(str) {
  if (!str) return 0
  let hash = 0
  for (let i = 0; i < str.length; i++) {
    hash = str.charCodeAt(i) + ((hash << 5) - hash)
  }
  return Math.abs(hash) % 10
}

onMounted(async () => {
  try {
    profile.value = await callAPI('portal_get_profile')
  } catch (e) {
    console.error('Failed to load profile:', e)
  }
})
</script>

<style scoped>
.profile-page { animation: fadeIn var(--transition-base); }
.page-loading { padding: var(--space-6); }
.stats-skeleton { display: grid; grid-template-columns: repeat(3, 1fr); gap: var(--space-4); }

.profile-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(360px, 1fr));
  gap: var(--space-4);
}

.section-title {
  font-size: var(--text-md);
  font-weight: var(--font-weight-semibold);
  margin-bottom: var(--space-5);
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
.info-value { 
  font-size: var(--text-sm); 
  font-weight: var(--font-weight-medium); 
  color: var(--color-text); 
  text-align: right;
  max-width: 60%;
  word-break: break-word;
}

.guardian-card {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3);
  background: var(--gray-50);
  border-radius: var(--radius-md);
  margin-bottom: var(--space-2);
}
.guardian-avatar { flex-shrink: 0; }
.guardian-name { font-size: var(--text-sm); font-weight: var(--font-weight-medium); }
.guardian-relation { font-size: var(--text-xs); color: var(--color-text-muted); }

.child-row {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3) 0;
  border-bottom: 1px solid var(--color-border-light);
}
.child-row:last-child { border-bottom: none; }
.child-avatar { flex-shrink: 0; }
.child-info { flex: 1; }
.child-name { display: block; font-size: var(--text-sm); font-weight: var(--font-weight-medium); }
.child-program { font-size: var(--text-xs); color: var(--color-text-muted); }

.hero-avatar-large { flex-shrink: 0; }

@media (max-width: 640px) {
  .profile-grid { grid-template-columns: 1fr; }
  .info-value { max-width: 100%; text-align: left; }
  .info-row { flex-direction: column; align-items: flex-start; gap: var(--space-1); }
}
</style>