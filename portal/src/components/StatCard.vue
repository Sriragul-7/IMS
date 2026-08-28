<template>
  <div class="stat-card" :style="{ borderLeftColor: color }">
    <div class="stat-card-inner">
      <div class="stat-card-content">
        <div class="stat-value" :style="{ color: color }">{{ value }}</div>
        <div class="stat-label">{{ label }}</div>
      </div>
      <div v-if="icon" class="stat-icon" :style="{ background: color + '12', color: color }">
        <span v-html="icon"></span>
      </div>
    </div>
    <div v-if="subtitle" class="stat-subtitle">{{ subtitle }}</div>
  </div>
</template>

<script setup>
defineProps({
  value: { type: [String, Number], required: true },
  label: { type: String, required: true },
  color: { type: String, default: '#1e40af' },
  icon: { type: String, default: '' },
  subtitle: { type: String, default: '' },
})
</script>

<style scoped>
.stat-card-inner {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
}
.stat-card-content { flex: 1; }
.stat-subtitle {
  font-size: var(--text-xs);
  color: var(--color-text-muted);
  margin-top: var(--space-2);
  padding-top: var(--space-2);
  border-top: 1px solid var(--color-border-light);
}
</style>
