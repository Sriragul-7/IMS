<template>
  <span class="avatar-chip" :class="['avatar-' + size, 'avatar-' + colorIndex]" :style="customStyle">
    <span v-if="!src">{{ initials }}</span>
    <img v-else :src="src" :alt="alt" class="avatar-img" />
    <span v-if="status" class="avatar-status" :class="statusClass"></span>
  </span>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  name: { type: String, required: true },
  size: { type: String, default: 'md' },
  src: { type: String, default: '' },
  alt: { type: String, default: '' },
  status: { type: String, default: '' },
  colorIndex: { type: Number, default: null }
})

const initials = computed(() => {
  if (!props.name) return '?'
  return props.name.split(' ').map(w => w[0]).join('').toUpperCase().slice(0, 2)
})

const colorIndex = computed(() => {
  if (props.colorIndex !== null) return props.colorIndex
  let hash = 0
  for (let i = 0; i < props.name.length; i++) {
    hash = props.name.charCodeAt(i) + ((hash << 5) - hash)
  }
  return Math.abs(hash) % 10
})

const customStyle = computed(() => ({
  width: `var(--avatar-${props.size}-width, 40px)`,
  height: `var(--avatar-${props.size}-height, 40px)`,
  fontSize: `var(--avatar-${props.size}-font, 1rem)`
}))

const statusClass = computed(() => {
  const map = {
    online: 'status-online',
    offline: 'status-offline',
    busy: 'status-busy',
    away: 'status-away'
  }
  return map[props.status] || ''
})
</script>

<style scoped>
.avatar-chip {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-full);
  font-weight: var(--font-weight-semibold);
  color: white;
  flex-shrink: 0;
  position: relative;
  overflow: hidden;
  background: var(--color-primary);
}

.avatar-xs { width: 24px; height: 24px; font-size: var(--text-xs); }
.avatar-sm { width: 32px; height: 32px; font-size: var(--text-sm); }
.avatar-md { width: 40px; height: 40px; font-size: var(--text-base); }
.avatar-lg { width: 56px; height: 56px; font-size: var(--text-lg); }
.avatar-xl { width: 72px; height: 72px; font-size: var(--text-xl); }
.avatar-2xl { width: 96px; height: 96px; font-size: var(--text-2xl); }

.avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: inherit;
}

.avatar-status {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 25%;
  height: 25%;
  border-radius: 50%;
  border: 2px solid var(--color-surface);
  min-width: 8px;
  min-height: 8px;
}
.status-online { background: var(--color-success); }
.status-offline { background: var(--gray-400); }
.status-busy { background: var(--color-danger); }
.status-away { background: var(--color-warning); }

/* Deterministic color classes */
.avatar-0 { background: #0f172a; }
.avatar-1 { background: #0d9488; }
.avatar-2 { background: #d97706; }
.avatar-3 { background: #7c3aed; }
.avatar-4 { background: #2563eb; }
.avatar-5 { background: #dc2626; }
.avatar-6 { background: #059669; }
.avatar-7 { background: #f59e0b; }
.avatar-8 { background: #ec4899; }
.avatar-9 { background: #06b6d4; }
</style>