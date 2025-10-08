<template>
  <!-- 中文注释：通过 variant / pill 控制徽章的语义色与形态，统一展示房源标签 -->
  <span class="base-badge" :class="[`base-badge--${variant}`, { 'base-badge--pill': pill }]">
    <slot />
  </span>
</template>

<script setup>
defineProps({
  // 中文注释：默认品牌色，支撑“新上线”等高亮标签
  variant: {
    type: String,
    default: 'brand',
    validator: (value) =>
      ['brand', 'neutral', 'success', 'warning', 'danger', 'info'].includes(value),
  },
  // 中文注释：开启后前端表现为完全圆角的胶囊态（配合小写字母更友好）
  pill: {
    type: Boolean,
    default: true,
  },
})
</script>

<style scoped>
.base-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-1) var(--space-1-5);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  line-height: var(--line-height-tight);
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: var(--color-text-inverse);
  background: var(--brand-primary);
  border-radius: var(--radius-full);
  border: 1px solid transparent;
  min-height: var(--size-20);
  gap: var(--space-1);
}

/* 中文注释：pill 关闭时使用较小圆角，适合矩形标签 */
.base-badge--pill {
  border-radius: var(--radius-full);
}

.base-badge:not(.base-badge--pill) {
  border-radius: var(--radius-compact-sm);
  text-transform: none;
  letter-spacing: 0;
}

/* 语义色：与设计令牌保持一致，便于统一维护 */
.base-badge--brand {
  background: var(--brand-primary);
  border-color: var(--brand-primary);
  color: var(--color-text-inverse);
}

.base-badge--neutral {
  background: var(--color-bg-muted);
  border-color: var(--color-border-default);
  color: var(--color-text-secondary);
}

.base-badge--success {
  background: var(--success-soft-bg);
  border-color: var(--success-border);
  color: var(--color-success);
}

.base-badge--warning {
  background: var(--warning-soft-bg);
  border-color: var(--warning-border);
  color: var(--color-warning);
}

.base-badge--danger {
  background: var(--danger-soft-bg);
  border-color: var(--danger-border);
  color: var(--color-danger);
}

.base-badge--info {
  background: var(--info-soft-bg);
  border-color: var(--info-border);
  color: var(--color-info);
}
</style>
