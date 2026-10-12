<template>
  <div class="skeleton" :class="typeClass">
    <slot />
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  type: { type: String, default: 'text' },
  width: { type: [String, Number], default: '100%' },
  height: { type: [String, Number], default: 'auto' },
  rounded: { type: Boolean, default: true },
  animated: { type: Boolean, default: true }
})

const typeClass = computed(() => {
  const classes = [`skeleton--${props.type}`]
  if (!props.rounded) classes.push('skeleton--sharp')
  if (!props.animated) classes.push('skeleton--static')
  return classes.join(' ')
})

const inlineStyle = computed(() => ({
  width: props.width,
  height: props.height
}))
</script>

<style scoped>
.skeleton {
  background: linear-gradient(90deg, var(--gray-100) 25%, var(--gray-200) 50%, var(--gray-100) 75%);
  background-size: 200% 100%;
  animation: skeleton-pulse 1.5s ease-in-out infinite;
  display: inline-block;
}
.skeleton--static { animation: none; }
.skeleton--sharp { border-radius: 0; }
.skeleton--rounded { border-radius: var(--radius-sm); }
.skeleton--text { height: 14px; border-radius: var(--radius-sm); }
.skeleton--text-sm { height: 12px; border-radius: var(--radius-sm); }
.skeleton--heading { height: 22px; border-radius: var(--radius-sm); }
.skeleton--card { height: 140px; border-radius: var(--radius-xl); }
.skeleton--circle { border-radius: var(--radius-full); }
.skeleton--avatar { width: 40px; height: 40px; border-radius: var(--radius-full); }
.skeleton--button { height: 40px; border-radius: var(--radius-md); }
.skeleton--badge { height: 20px; width: 80px; border-radius: var(--radius-full); }
.skeleton--stat { height: 120px; border-radius: var(--radius-xl); }
.skeleton--table-row { height: 48px; }
.skeleton--chart { height: 280px; border-radius: var(--radius-xl); }

@keyframes skeleton-pulse {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

/* Convenience components */
.skeleton-wrapper { display: flex; flex-direction: column; gap: var(--space-3); }
.skeleton-card-wrapper {
  background: var(--color-surface);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-xl);
  padding: var(--space-6);
}
.skeleton-list-item {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3) 0;
}
.skeleton-table-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--space-4);
  padding: var(--space-3) 0;
  border-bottom: 1px solid var(--color-border-light);
}
</style>