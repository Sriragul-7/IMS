<template>
  <div class="progress-ring-wrapper" :style="{ width: size + 'px', height: size + 'px' }">
    <svg class="progress-ring-svg" :viewBox="`0 0 ${diameter} ${diameter}`" :style="{ transform: 'rotate(-90deg)' }">
      <circle
        class="progress-ring-bg"
        :cx="radius"
        :cy="radius"
        :r="radius"
        :stroke-width="strokeWidth"
        fill="none"
      />
      <circle
        class="progress-ring-fill"
        :cx="radius"
        :cy="radius"
        :r="radius"
        :stroke-width="strokeWidth"
        fill="none"
        :stroke-dasharray="circumference"
        :stroke-dashoffset="strokeDashoffset"
        stroke-linecap="round"
        :style="{ stroke: strokeColor, transition: 'stroke-dashoffset 1s ease-out' }"
      />
    </svg>
    <div class="progress-ring-content">
      <slot>
        <div v-if="showValue" class="progress-ring-value">
          <span class="progress-ring-number">{{ displayValue }}</span>
          <span v-if="unit" class="progress-ring-unit">{{ unit }}</span>
        </div>
        <div v-if="label" class="progress-ring-label">{{ label }}</div>
      </slot>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, watch } from 'vue'

const props = defineProps({
  value: { type: Number, required: true },
  max: { type: Number, default: 100 },
  size: { type: Number, default: 80 },
  strokeWidth: { type: Number, default: 4 },
  strokeColor: { type: String, default: '' },
  label: { type: String, default: '' },
  unit: { type: String, default: '%' },
  showValue: { type: Boolean, default: true },
  animate: { type: Boolean, default: true }
})

const diameter = computed(() => props.size)
const radius = computed(() => (props.size - props.strokeWidth) / 2)
const circumference = computed(() => 2 * Math.PI * radius.value)
const percentage = computed(() => Math.max(0, Math.min(1, props.value / props.max)))
const strokeDashoffset = computed(() => circumference.value * (1 - percentage.value))
const displayValue = computed(() => Math.round(props.value))

const strokeColor = computed(() => {
  if (props.strokeColor) return props.strokeColor
  const pct = percentage.value * 100
  if (pct >= 80) return 'var(--color-success)'
  if (pct >= 60) return 'var(--color-warning)'
  return 'var(--color-danger)'
})

let animated = false
onMounted(() => {
  if (props.animate) {
    animated = true
  }
})
watch(() => props.value, () => {
  if (props.animate) {
    animated = true
  }
})
</script>

<style scoped>
.progress-ring-wrapper {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  position: relative;
}
.progress-ring-svg {
  width: 100%;
  height: 100%;
}
.progress-ring-bg {
  stroke: var(--gray-200);
}
.progress-ring-content {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  pointer-events: none;
}
.progress-ring-value {
  display: flex;
  align-items: flex-end;
  gap: 2px;
  line-height: 1;
}
.progress-ring-number {
  font-size: clamp(1rem, 20%, 1.5rem);
  font-weight: var(--font-weight-bold);
  color: var(--color-text);
  font-variant-numeric: tabular-nums;
}
.progress-ring-unit {
  font-size: clamp(0.6rem, 12%, 0.875rem);
  font-weight: var(--font-weight-medium);
  color: var(--color-text-muted);
  margin-bottom: 2px;
}
.progress-ring-label {
  font-size: var(--text-xs);
  color: var(--color-text-muted);
  margin-top: var(--space-1);
  white-space: nowrap;
}
</style>