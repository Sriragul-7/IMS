<template>
  <div class="page-header">
    <div class="page-header-row">
      <div class="page-header-main">
        <h1>{{ title }}</h1>
        <p class="page-subtitle" v-if="subtitle">{{ subtitle }}</p>
        <div class="page-header-meta" v-if="metaItems.length">
          <span v-for="item in metaItems" :key="item.label" class="meta-item">
            <span class="meta-label">{{ item.label }}</span>
            <span class="meta-value">{{ item.value }}</span>
          </span>
        </div>
      </div>
      <div class="page-header-actions" v-if="$slots.actions">
        <slot name="actions" />
      </div>
    </div>
    <div class="page-header-tabs" v-if="$slots.tabs">
      <slot name="tabs" />
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: { type: String, required: true },
  subtitle: { type: String, default: '' },
  metaItems: { type: Array, default: () => [] }
})
</script>

<style scoped>
.page-header { margin-bottom: var(--space-6); }
.page-header-row {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--space-4);
  flex-wrap: wrap;
}
.page-header-main { flex: 1; min-width: 0; }
.page-header h1 {
  font-size: var(--text-2xl);
  font-weight: var(--font-weight-bold);
  color: var(--color-text);
  margin-bottom: var(--space-1);
  line-height: var(--leading-tight);
}
.page-subtitle {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  margin-bottom: var(--space-3);
}
.page-header-meta {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-4);
  align-items: center;
}
.meta-item {
  display: flex;
  align-items: center;
  gap: var(--space-1-5);
  font-size: var(--text-sm);
}
.meta-label { color: var(--color-text-muted); }
.meta-value { font-weight: var(--font-weight-medium); color: var(--color-text); }
.page-header-actions {
  display: flex;
  gap: var(--space-2);
  flex-shrink: 0;
  flex-wrap: wrap;
}
.page-header-tabs {
  margin-top: var(--space-4);
  padding-top: var(--space-4);
  border-top: 1px solid var(--color-border-light);
}

@media (max-width: 640px) {
  .page-header-row { flex-direction: column; align-items: stretch; }
  .page-header-actions { width: 100%; justify-content: stretch; }
  .page-header-actions .btn { flex: 1; }
}
</style>