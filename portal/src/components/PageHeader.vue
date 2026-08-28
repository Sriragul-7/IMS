<template>
  <div class="page-header">
    <div class="page-header-row">
      <div>
        <h1>{{ title }}</h1>
        <p class="page-subtitle" v-if="subtitle">{{ subtitle }}</p>
      </div>
      <div class="page-header-actions" v-if="$slots.actions">
        <slot name="actions" />
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: { type: String, required: true },
  subtitle: { type: String, default: '' },
})
</script>

<style scoped>
.page-header-row {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--space-4);
}
.page-header-actions {
  display: flex;
  gap: var(--space-2);
  flex-shrink: 0;
}
@media (max-width: 640px) {
  .page-header-row { flex-direction: column; }
}
</style>
