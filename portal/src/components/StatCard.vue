<template>
  <div class="stat-card card card-hover" :class="variantClass" :style="{ borderLeftColor: color }">
    <div class="stat-card-inner">
      <div class="stat-card-content">
        <div class="stat-value" :style="{ color: color }" v-text="formattedValue"></div>
        <div class="stat-label">{{ label }}</div>
        <div v-if="trend" class="stat-trend" :class="trendClass">
          <span v-html="trendIcon"></span>
          <span>{{ trend }}</span>
        </div>
      </div>
      <div v-if="icon" class="stat-icon" :style="{ background: color + '15', color: color }">
        <span v-html="icon"></span>
      </div>
    </div>
    <div v-if="subtitle" class="stat-subtitle">{{ subtitle }}</div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  value: { type: [String, Number], required: true },
  label: { type: String, required: true },
  color: { type: String, default: '#0f172a' },
  icon: { type: String, default: '' },
  subtitle: { type: String, default: '' },
  trend: { type: String, default: '' },
  trendVariant: { type: String, default: 'positive' },
  format: { type: String, default: '' },
  variant: { type: String, default: 'default' }
})

const formattedValue = computed(() => {
  if (props.format === 'currency') {
    return '₹' + Number(props.value || 0).toLocaleString('en-IN', { minimumFractionDigits: 0 })
  }
  if (props.format === 'percent') {
    return Number(props.value || 0).toFixed(1) + '%'
  }
  if (props.format === 'number') {
    return Number(props.value || 0).toLocaleString('en-IN')
  }
  return props.value
})

const trendClass = computed(() => `stat-trend--${props.trendVariant}`)
const trendIcon = computed(() => {
  const icons = {
    positive: '&#9650;',
    negative: '&#9660;',
    neutral: '&#8212;'
  }
  return icons[props.trendVariant] || ''
})

const variantClass = computed(() => `stat-card--${props.variant}`)
</script>

<style scoped>
.stat-card-inner {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--space-4);
}
.stat-card-content { flex: 1; min-width: 0; }
.stat-value {
  font-size: var(--text-3xl);
  font-weight: var(--font-weight-bold);
  line-height: 1;
  font-variant-numeric: tabular-nums;
  color: var(--color-text);
}
.stat-label {
  font-size: var(--text-xs);
  font-weight: var(--font-weight-medium);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--color-text-muted);
  margin-top: var(--space-1-5);
}
.stat-trend {
  display: inline-flex;
  align-items: center;
  gap: var(--space-1);
  font-size: var(--text-xs);
  font-weight: var(--font-weight-medium);
  padding: var(--space-1) var(--space-2);
  border-radius: var(--radius-full);
  margin-top: var(--space-2);
}
.stat-trend--positive { background: var(--color-success-light); color: var(--color-success-dark); }
.stat-trend--negative { background: var(--color-danger-light); color: var(--color-danger-dark); }
.stat-trend--neutral { background: var(--gray-100); color: var(--gray-600); }
.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  flex-shrink: 0;
}
.stat-icon :deep(svg) {
  width: 22px;
  height: 22px;
}
.stat-subtitle {
  font-size: var(--text-xs);
  color: var(--color-text-muted);
  margin-top: var(--space-3);
  padding-top: var(--space-3);
  border-top: 1px solid var(--color-border-light);
}

/* Variants */
.stat-card--default { border-left-color: var(--color-primary); }
.stat-card--accent { border-left-color: var(--color-accent); }
.stat-card--amber { border-left-color: var(--color-amber); }
.stat-card--success { border-left-color: var(--color-success); }
.stat-card--purple { border-left-color: var(--color-purple); }
.stat-card--info { border-left-color: var(--color-info); }
.stat-card--danger { border-left-color: var(--color-danger); }
</style>