<template>
  <div class="chart-card card card-hover" :class="variantClass">
    <div class="chart-card-header" v-if="title || subtitle || actions">
      <div class="chart-card-title-group">
        <h3 v-if="title" class="chart-card-title">{{ title }}</h3>
        <p v-if="subtitle" class="chart-card-subtitle">{{ subtitle }}</p>
      </div>
      <div class="chart-card-actions" v-if="actions">
        <slot name="actions" />
      </div>
    </div>
    <div class="chart-card-body">
      <div class="chart-wrapper" :style="{ height: height + 'px' }">
        <canvas v-if="!loading && chartData" ref="canvas"></canvas>
        <div v-else class="chart-skeleton" :style="{ height: height + 'px' }">
          <div class="skeleton skeleton-card" style="width: 100%; height: 100%;"></div>
        </div>
        <div v-if="!loading && !chartData && !error" class="empty-chart">
          <div class="empty-state" style="padding: var(--space-8);">
            <div class="empty-state-icon" style="background: var(--gray-100); color: var(--color-text-muted);" v-html="icons.chart"></div>
            <div class="empty-state-title">No data available</div>
            <div class="empty-state-desc">{{ emptyMessage }}</div>
          </div>
        </div>
        <div v-if="error" class="error-chart">
          <div class="empty-state" style="padding: var(--space-8);">
            <div class="empty-state-icon" style="background: var(--color-danger-light); color: var(--color-danger);" v-html="icons.alert"></div>
            <div class="empty-state-title">Failed to load chart</div>
            <div class="empty-state-desc">{{ error }}</div>
          </div>
        </div>
      </div>
      <div class="chart-card-legend" v-if="showLegend && legendItems.length">
        <div v-for="item in legendItems" :key="item.label" class="legend-item">
          <span class="legend-color" :style="{ background: item.color }"></span>
          <span class="legend-label">{{ item.label }}</span>
          <span v-if="item.value !== undefined" class="legend-value">{{ item.value }}</span>
        </div>
      </div>
      <div class="chart-card-footer" v-if="footer">
        <slot name="footer">{{ footer }}</slot>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick, computed } from 'vue'
import { Chart } from 'chart.js'
import { icons } from '../utils/icons.js'

const props = defineProps({
  type: { type: String, default: 'line' },
  title: { type: String, default: '' },
  subtitle: { type: String, default: '' },
  chartData: { type: Object, default: null },
  options: { type: Object, default: () => ({}) },
  height: { type: Number, default: 280 },
  loading: { type: Boolean, default: false },
  error: { type: String, default: '' },
  showLegend: { type: Boolean, default: true },
  legendItems: { type: Array, default: () => [] },
  footer: { type: String, default: '' },
  emptyMessage: { type: String, default: 'No data to display' },
  variant: { type: String, default: 'default' }
})

const canvas = ref(null)
let chartInstance = null

const variantClass = computed(() => `chart-card--${props.variant}`)

function createChart() {
  if (!canvas.value || !props.chartData) return
  
  try {
    if (chartInstance) {
      chartInstance.destroy()
    }
    
    const ctx = canvas.value.getContext('2d')
    const defaultOptions = getDefaultOptions()
    const mergedOptions = deepMerge(defaultOptions, props.options)
    
    chartInstance = new Chart(ctx, {
      type: props.type,
      data: props.chartData,
      options: mergedOptions
    })
  } catch (e) {
    console.error('Chart creation failed:', e)
  }
}

function getDefaultOptions() {
  const isDark = false
  const gridColor = 'rgba(15, 23, 42, 0.06)'
  const textColor = '#64748b'
  
  const base = {
    responsive: true,
    maintainAspectRatio: false,
    animation: { duration: 800, easing: 'easeOutQuart' },
    interaction: { intersect: false, mode: 'index' },
    plugins: {
      legend: { display: false },
      tooltip: {
        backgroundColor: '#0f172a',
        titleColor: '#ffffff',
        bodyColor: '#e2e8f0',
        padding: 12,
        cornerRadius: 8,
        displayColors: true,
        borderColor: 'rgba(255,255,255,0.1)',
        borderWidth: 1
      }
    },
    scales: {
      x: {
        grid: { display: false, drawBorder: false },
        ticks: { color: textColor, font: { size: 11, family: 'Inter' }, maxRotation: 0, autoSkip: true, maxTicksLimit: 8 }
      },
      y: {
        grid: { color: gridColor, drawBorder: false },
        ticks: { color: textColor, font: { size: 11, family: 'Inter' }, stepSize: undefined },
        beginAtZero: true
      }
    }
  }
  
  if (props.type === 'doughnut' || props.type === 'pie') {
    return {
      ...base,
      scales: {},
      plugins: {
        ...base.plugins,
        tooltip: {
          ...base.plugins.tooltip,
          callbacks: {
            label: (ctx) => {
              const label = ctx.label || ''
              const value = ctx.parsed
              return `${label}: ${value.toLocaleString()}`
            }
          }
        }
      },
      cutout: '70%',
      radius: '85%'
    }
  }
  
  if (props.type === 'bar') {
    return {
      ...base,
      plugins: {
        ...base.plugins,
        tooltip: {
          ...base.plugins.tooltip,
          callbacks: {
            label: (ctx) => {
              const label = ctx.dataset.label || ''
              const value = ctx.parsed.y
              return `${label}: ${value.toLocaleString()}`
            }
          }
        }
      }
    }
  }
  
  return base
}

function deepMerge(target, source) {
  const result = { ...target }
  for (const key of Object.keys(source)) {
    if (source[key] && typeof source[key] === 'object' && !Array.isArray(source[key])) {
      result[key] = deepMerge(target[key] || {}, source[key])
    } else {
      result[key] = source[key]
    }
  }
  return result
}

onMounted(() => {
  nextTick(() => {
    createChart()
  })
})

watch(() => props.chartData, () => {
  nextTick(() => {
    if (chartInstance && props.chartData) {
      chartInstance.data = props.chartData
      chartInstance.update()
    } else {
      createChart()
    }
  })
}, { deep: true })

watch(() => props.options, () => {
  nextTick(() => {
    if (chartInstance) {
      chartInstance.destroy()
    }
    createChart()
  })
}, { deep: true })

watch(() => props.type, () => {
  nextTick(() => createChart())
})
</script>

<style scoped>
.chart-card {
  overflow: hidden;
}
.chart-card--default { border-left-color: var(--color-primary); }
.chart-card--accent { border-left-color: var(--color-accent); }
.chart-card--amber { border-left-color: var(--color-amber); }
.chart-card--success { border-left-color: var(--color-success); }
.chart-card--purple { border-left-color: var(--color-purple); }
.chart-card--info { border-left-color: var(--color-info); }
.chart-card-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  padding: var(--space-5) var(--space-6);
  border-bottom: 1px solid var(--color-border-light);
}
.chart-card-title-group { flex: 1; }
.chart-card-title {
  font-size: var(--text-md);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text);
  margin-bottom: var(--space-1);
}
.chart-card-subtitle {
  font-size: var(--text-sm);
  color: var(--color-text-muted);
}
.chart-card-actions { flex-shrink: 0; }
.chart-card-body { padding: var(--space-6); position: relative; }
.chart-wrapper { position: relative; width: 100%; }
.chart-skeleton { width: 100%; display: flex; align-items: center; justify-content: center; }
.empty-chart, .error-chart { width: 100%; display: flex; align-items: center; justify-content: center; }
.empty-state-icon {
  width: 64px;
  height: 64px;
  border-radius: var(--radius-xl);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto var(--space-4);
}
.empty-state-icon :deep(svg) { width: 28px; height: 28px; }
.empty-state-title {
  font-size: var(--text-lg);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text);
  margin-bottom: var(--space-1);
  text-align: center;
}
.empty-state-desc {
  font-size: var(--text-sm);
  color: var(--color-text-muted);
  text-align: center;
}
.chart-card-legend {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: var(--space-4);
  padding: var(--space-4) var(--space-6) 0;
  border-top: 1px solid var(--color-border-light);
  margin-top: var(--space-4);
}
.legend-item {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
}
.legend-color {
  width: 10px;
  height: 10px;
  border-radius: var(--radius-sm);
  flex-shrink: 0;
}
.legend-label { font-weight: var(--font-weight-medium); }
.legend-value {
  font-weight: var(--font-weight-semibold);
  color: var(--color-text);
  font-variant-numeric: tabular-nums;
}
.chart-card-footer {
  padding: var(--space-4) var(--space-6);
  border-top: 1px solid var(--color-border-light);
  margin-top: var(--space-4);
  font-size: var(--text-sm);
  color: var(--color-text-muted);
  display: flex;
  align-items: center;
  justify-content: space-between;
}
</style>