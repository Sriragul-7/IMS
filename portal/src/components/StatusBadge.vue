<template>
  <span class="badge" :class="variantClass">
    <span v-if="dot" class="badge-dot"></span>
    {{ label || text }}
  </span>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  text: { type: String, required: true },
  label: { type: String, default: '' },
  variant: { type: String, default: 'neutral' },
  dot: { type: Boolean, default: false },
})

const variantClass = computed(() => `badge-${props.variant}`)
</script>

<style scoped>
.badge-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: currentColor;
  flex-shrink: 0;
}
</style>
