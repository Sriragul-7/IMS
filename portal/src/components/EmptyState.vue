<template>
  <div class="empty-state" :class="sizeClass">
    <div class="empty-state-icon" :style="{ background: iconBg }">
      <span v-html="icon"></span>
    </div>
    <div class="empty-state-title">{{ title }}</div>
    <div class="empty-state-desc" v-if="description">{{ description }}</div>
    <div class="empty-state-action" v-if="$slots.default">
      <slot />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { icons } from '../utils/icons.js'

const props = defineProps({
  title: { type: String, required: true },
  description: { type: String, default: '' },
  icon: { type: String, default: icons.document },
  iconBg: { type: String, default: 'var(--gray-100)' },
  size: { type: String, default: 'md' }
})

const sizeClass = computed(() => `empty-state--${props.size}`)
</script>

<style scoped>
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
}
.empty-state--sm { padding: var(--space-6) var(--space-4); }
.empty-state--md { padding: var(--space-10) var(--space-6); }
.empty-state--lg { padding: var(--space-16) var(--space-8); }
.empty-state--xl { padding: var(--space-20) var(--space-10); }

.empty-state-icon {
  width: 64px;
  height: 64px;
  border-radius: var(--radius-xl);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.75rem;
  margin-bottom: var(--space-4);
  flex-shrink: 0;
  color: var(--color-text-muted);
}
.empty-state-icon :deep(svg) { width: 28px; height: 28px; }
.empty-state--sm .empty-state-icon { width: 48px; height: 48px; border-radius: var(--radius-lg); }
.empty-state--sm .empty-state-icon :deep(svg) { width: 22px; height: 22px; }
.empty-state--lg .empty-state-icon { width: 80px; height: 80px; border-radius: var(--radius-2xl); }
.empty-state--lg .empty-state-icon :deep(svg) { width: 36px; height: 36px; }
.empty-state--xl .empty-state-icon { width: 96px; height: 96px; border-radius: var(--radius-3xl); }
.empty-state--xl .empty-state-icon :deep(svg) { width: 44px; height: 44px; }

.empty-state-title {
  font-size: var(--text-lg);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text);
  margin-bottom: var(--space-1);
}
.empty-state--sm .empty-state-title { font-size: var(--text-md); }
.empty-state--lg .empty-state-title { font-size: var(--text-xl); }
.empty-state--xl .empty-state-title { font-size: var(--text-2xl); }

.empty-state-desc {
  font-size: var(--text-sm);
  color: var(--color-text-muted);
  max-width: 320px;
  line-height: var(--leading-relaxed);
}
.empty-state--sm .empty-state-desc { font-size: var(--text-xs); max-width: 240px; }
.empty-state--lg .empty-state-desc { font-size: var(--text-md); max-width: 400px; }
.empty-state--xl .empty-state-desc { font-size: var(--text-lg); max-width: 480px; }

.empty-state-action { margin-top: var(--space-4); }
</style>
