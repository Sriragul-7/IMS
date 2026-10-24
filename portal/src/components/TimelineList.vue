<template>
  <div class="timeline-list" :class="{ 'timeline-list--vertical': vertical, 'timeline-list--horizontal': !vertical }">
    <div v-if="loading" class="timeline-skeleton">
      <div v-for="i in skeletonItems" :key="i" class="timeline-skeleton-item">
        <div class="skeleton skeleton-circle" :style="{ width: dotSize + 'px', height: dotSize + 'px' }"></div>
        <div class="skeleton skeleton-text" style="width: 60%;"></div>
        <div class="skeleton skeleton-text-sm" style="width: 40%;"></div>
      </div>
    </div>
    
    <template v-else>
      <div class="timeline-items" v-if="items.length">
        <div v-for="(item, index) in items" :key="item.id || index" class="timeline-item" :class="{ 'timeline-item--first': index === 0, 'timeline-item--last': index === items.length - 1 }">
          <div class="timeline-marker" :style="markerStyle(item, index)">
            <div class="timeline-dot" :class="item.dotClass" :style="dotStyle(item)"></div>
            <div v-if="vertical && index < items.length - 1" class="timeline-line" :style="lineStyle(index)"></div>
          </div>
          <div class="timeline-content">
            <div class="timeline-header" v-if="item.time || item.badge">
              <time v-if="item.time" class="timeline-time" :datetime="item.timeISO">{{ formatTime(item.time) }}</time>
              <StatusBadge v-if="item.badge" :text="item.badge.text" :variant="item.badge.variant" :dot="item.badge.dot" />
            </div>
            <div class="timeline-title" v-if="item.title">{{ item.title }}</div>
            <div class="timeline-body" v-if="item.body" v-html="item.body"></div>
            <div class="timeline-meta" v-if="item.meta">
              <span v-for="m in item.meta" :key="m.label" class="timeline-meta-item">
                <span class="timeline-meta-label">{{ m.label }}:</span>
                <span class="timeline-meta-value">{{ m.value }}</span>
              </span>
            </div>
            <div class="timeline-actions" v-if="item.actions && item.actions.length">
              <slot name="actions" :item="item">
                <button v-for="a in item.actions" :key="a.key" class="btn btn-sm btn-ghost" @click="a.handler(item)">{{ a.label }}</button>
              </slot>
            </div>
          </div>
        </div>
      </div>
      
      <EmptyState v-else :title="emptyTitle" :description="emptyDescription" :icon="emptyIcon" />
    </template>
    
    <div class="timeline-load-more" v-if="showLoadMore && !loading">
      <button class="btn btn-secondary" @click="loadMore">{{ loadMoreText }}</button>
    </div>
  </div>
</template>

<script setup>
import EmptyState from './EmptyState.vue'
import StatusBadge from './StatusBadge.vue'
import { icons } from '../utils/icons.js'

const props = defineProps({
  items: { type: Array, default: () => [] },
  loading: { type: Boolean, default: false },
  vertical: { type: Boolean, default: true },
  showLoadMore: { type: Boolean, default: false },
  loadMoreText: { type: String, default: 'Load more' },
  emptyTitle: { type: String, default: 'No items' },
  emptyDescription: { type: String, default: 'No items to display' },
  emptyIcon: { type: String, default: icons.clipboard },
  skeletonItems: { type: Number, default: 3 },
  dotSize: { type: Number, default: 12 },
  lineWidth: { type: Number, default: 2 }
})

const emit = defineEmits(['load-more', 'action'])

const markerStyle = (item, index) => {
  if (!props.vertical) return {}
  return {
    width: props.dotSize + 'px',
    flexShrink: 0
  }
}

const dotStyle = (item) => {
  const size = props.dotSize
  const color = item.dotColor || 'var(--color-primary)'
  return {
    width: size + 'px',
    height: size + 'px',
    background: color,
    borderColor: color
  }
}

const lineStyle = (index) => {
  return {
    width: props.lineWidth + 'px',
    background: 'var(--color-border-light)',
    left: (props.dotSize / 2 - props.lineWidth / 2) + 'px'
  }
}

function formatTime(time) {
  if (!time) return ''
  const date = new Date(time)
  const now = new Date()
  const diff = now - date
  const minutes = Math.floor(diff / 60000)
  const hours = Math.floor(diff / 3600000)
  const days = Math.floor(diff / 86400000)
  
  if (minutes < 1) return 'Just now'
  if (minutes < 60) return `${minutes}m ago`
  if (hours < 24) return `${hours}h ago`
  if (days < 7) return `${days}d ago`
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
}

function loadMore() {
  emit('load-more')
}
</script>

<style scoped>
.timeline-list { position: relative; }
.timeline-list--vertical { display: flex; flex-direction: column; }
.timeline-list--horizontal { display: flex; flex-direction: row; overflow-x: auto; gap: var(--space-4); padding: var(--space-2) 0; }

.timeline-skeleton { display: flex; flex-direction: column; gap: var(--space-4); }
.timeline-skeleton-item { display: flex; align-items: flex-start; gap: var(--space-3); }

.timeline-items { display: flex; flex-direction: column; }
.timeline-list--horizontal .timeline-items { flex-direction: row; gap: var(--space-4); }

.timeline-item {
  display: flex;
  gap: var(--space-3);
  position: relative;
}
.timeline-list--horizontal .timeline-item { flex-direction: column; align-items: center; min-width: 200px; flex-shrink: 0; }

.timeline-marker {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  z-index: 1;
}
.timeline-list--horizontal .timeline-marker { flex-direction: row; }

.timeline-dot {
  width: 100%;
  aspect-ratio: 1;
  border-radius: 50%;
  border: 3px solid var(--color-surface);
  box-shadow: var(--shadow-sm);
  position: relative;
  background: var(--color-primary);
  flex-shrink: 0;
}
.timeline-dot::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 50%;
  height: 50%;
  border-radius: 50%;
  background: currentColor;
  opacity: 0;
}
.timeline-dot.success { background: var(--color-success); }
.timeline-dot.warning { background: var(--color-warning); }
.timeline-dot.danger { background: var(--color-danger); }
.timeline-dot.info { background: var(--color-info); }
.timeline-dot.purple { background: var(--color-purple); }
.timeline-dot.accent { background: var(--color-accent); }

.timeline-line {
  flex: 1;
  width: 2px;
  background: var(--color-border-light);
}
.timeline-item--last .timeline-line { display: none; }
.timeline-list--horizontal .timeline-line { display: none; }

.timeline-content { flex: 1; min-width: 0; padding: var(--space-1) 0; }
.timeline-header { display: flex; align-items: center; gap: var(--space-2); margin-bottom: var(--space-1); flex-wrap: wrap; }
.timeline-time { font-size: var(--text-xs); color: var(--color-text-muted); white-space: nowrap; font-variant-numeric: tabular-nums; }
.timeline-title { font-size: var(--text-sm); font-weight: var(--font-weight-semibold); color: var(--color-text); line-height: var(--leading-tight); }
.timeline-body { font-size: var(--text-sm); color: var(--color-text-secondary); line-height: var(--leading-relaxed); margin-top: var(--space-1); }
.timeline-meta { display: flex; flex-wrap: wrap; gap: var(--space-3); margin-top: var(--space-2); font-size: var(--text-xs); }
.timeline-meta-item { display: flex; align-items: center; gap: var(--space-1); color: var(--color-text-muted); }
.timeline-meta-label { font-weight: var(--font-weight-medium); }
.timeline-meta-value { color: var(--color-text); }
.timeline-actions { display: flex; gap: var(--space-2); margin-top: var(--space-2); flex-wrap: wrap; }

.timeline-load-more { display: flex; justify-content: center; padding: var(--space-4) 0; margin-top: var(--space-4); border-top: 1px solid var(--color-border-light); }
</style>