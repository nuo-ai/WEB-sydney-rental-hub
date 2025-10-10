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
  padding: var(--space-xs) var(--space-sm);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  line-height: var(--font-line-height-xs);
  text-transform: uppercase;
  letter-spacing: 0.04em;
  border: 1px solid transparent;
  min-height: 20px; /* Fallback, consider adding to tokens */
  gap: var(--space-xs);
}

/* 中文注释：pill 开启时使用完全圆角的胶囊态 */
.base-badge--pill {
  border-radius: var(--radius-full);
}

/* 中文注释：pill 关闭时使用较小圆角，适合矩形标签 */
.base-badge:not(.base-badge--pill) {
  border-radius: var(--radius-sm);
  text-transform: none;
  letter-spacing: 0;
}

/* 语义色：与设计令牌保持一致，便于统一维护 */
.base-badge--brand {
  background: var(--color-brand-primary);
  border-color: var(--color-brand-primary);
  color: var(--color-semantic-text-inverse);
}

.base-badge--neutral {
  background: var(--color-semantic-bg-secondary);
  border-color: var(--color-semantic-border-default);
  color: var(--color-semantic-text-secondary);
}

.base-badge--success {
  background: var(--color-semantic-feedback-success-soft-bg);
  border-color: var(--color-semantic-feedback-success-border);
  color: var(--color-semantic-feedback-success);
}

.base-badge--warning {
  background: var(--color-semantic-feedback-warning-soft-bg);
  border-color: var(--color-semantic-feedback-warning-border);
  color: var(--color-semantic-feedback-warning);
}

.base-badge--danger {
  background: var(--color-semantic-feedback-danger-soft-bg);
  border-color: var(--color-semantic-feedback-danger-border);
  color: var(--color-semantic-feedback-error);
}

.base-badge--info {
  background: var(--color-semantic-feedback-info-soft-bg);
  border-color: var(--color-semantic-feedback-info-border);
  color: var(--color-semantic-feedback-info);
}
</style>
