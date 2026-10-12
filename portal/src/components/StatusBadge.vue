<template>
  <span class="badge" :class="variantClass" :style="customStyle">
    <span v-if="dot" class="badge-dot"></span>
    <slot>{{ label || text }}</slot>
  </span>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  text: { type: String, default: '' },
  label: { type: String, default: '' },
  variant: { type: String, default: 'neutral' },
  dot: { type: Boolean, default: false },
  size: { type: String, default: 'md' },
  outline: { type: Boolean, default: false }
})

const variantClass = computed(() => {
  const base = `badge--${props.size}`
  const variant = props.outline ? `badge--outline-${props.variant}` : `badge--${props.variant}`
  return `${base} ${variant}`
})

const customStyle = computed(() => {
  if (!props.outline) return {}
  const colors = {
    success: 'var(--color-success)',
    warning: 'var(--color-warning)',
    danger: 'var(--color-danger)',
    info: 'var(--color-info)',
    purple: 'var(--color-purple)',
    neutral: 'var(--gray-400)',
    primary: 'var(--color-primary)',
    accent: 'var(--color-accent)',
    amber: 'var(--color-amber)'
  }
  const color = colors[props.variant] || colors.neutral
  return {
    borderColor: color,
    color: color,
    background: 'transparent'
  }
})
</script>

<style scoped>
.badge {
  display: inline-flex;
  align-items: center;
  gap: var(--space-1);
  font-weight: var(--font-weight-medium);
  border-radius: var(--radius-full);
  line-height: 1;
  white-space: nowrap;
  border: 1px solid transparent;
}
.badge-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: currentColor;
  flex-shrink: 0;
}

/* Sizes */
.badge--xs { padding: 2px var(--space-2); font-size: 10px; }
.badge--sm { padding: var(--space-1) var(--space-2-5); font-size: var(--text-xs); }
.badge--md { padding: var(--space-1-5) var(--space-3); font-size: var(--text-sm); }
.badge--lg { padding: var(--space-2) var(--space-4); font-size: var(--text-base); }

/* Filled variants */
.badge--success { background: var(--color-success-light); color: var(--color-success-dark); }
.badge--warning { background: var(--color-warning-light); color: var(--color-warning-dark); }
.badge--danger { background: var(--color-danger-light); color: var(--color-danger-dark); }
.badge--info { background: var(--color-info-light); color: var(--color-info); }
.badge--purple { background: var(--color-purple-light); color: var(--color-purple); }
.badge--neutral { background: var(--gray-100); color: var(--gray-600); }
.badge--primary { background: var(--color-primary-100); color: var(--color-primary); }
.badge--accent { background: var(--color-accent-100); color: var(--color-accent); }
.badge--amber { background: var(--color-amber-100); color: var(--color-amber); }

/* Outline variants */
.badge--outline-success { border-color: var(--color-success); color: var(--color-success); }
.badge--outline-warning { border-color: var(--color-warning); color: var(--color-warning); }
.badge--outline-danger { border-color: var(--color-danger); color: var(--color-danger); }
.badge--outline-info { border-color: var(--color-info); color: var(--color-info); }
.badge--outline-purple { border-color: var(--color-purple); color: var(--color-purple); }
.badge--outline-neutral { border-color: var(--gray-400); color: var(--gray-600); }
.badge--outline-primary { border-color: var(--color-primary); color: var(--color-primary); }
.badge--outline-accent { border-color: var(--color-accent); color: var(--color-accent); }
.badge--outline-amber { border-color: var(--color-amber); color: var(--color-amber); }
</style>