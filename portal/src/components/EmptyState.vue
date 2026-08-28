<template>
  <div class="empty-state">
    <div class="empty-state-icon" :style="{ background: iconBg }">
      <span v-html="icon"></span>
    </div>
    <div class="empty-state-title">{{ title }}</div>
    <div class="empty-state-desc" v-if="description">{{ description }}</div>
    <slot />
  </div>
</template>

<script setup>
defineProps({
  title: { type: String, required: true },
  description: { type: String, default: '' },
  icon: { type: String, default: '&#9744;' },
  iconBg: { type: String, default: 'var(--gray-100)' },
})
</script>
