<!--
  BaseButton - 可复用的按钮组件
  基于设计令牌系统构建，提供一致的按钮体验

  使用示例：
  <BaseButton @click="handleClick">默认按钮</BaseButton>
  <BaseButton variant="primary" :loading="isLoading">主要按钮</BaseButton>
  <BaseButton variant="secondary" size="small">次要按钮</BaseButton>
-->

<template>
  <button
    class="base-button"
    :class="[
      `base-button--${variant}`,
      `base-button--${size}`,
      {
        'base-button--loading': loading,
        'base-button--disabled': disabled,
        'base-button--block': block
      }
    ]"
    :type="type"
    :disabled="disabled || loading"
    @click="handleClick"
  >
    <!-- 加载图标 -->
    <svg
      v-if="loading"
      class="base-button__loading-icon"
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      stroke-width="2"
      stroke-linecap="round"
      stroke-linejoin="round"
    >
      <path d="M21 12a9 9 0 11-6.219-8.56"/>
    </svg>

    <!-- 前置图标 -->
    <span v-if="$slots.icon && !loading" class="base-button__icon">
      <slot name="icon" />
    </span>

    <!-- 按钮文本 -->
    <span v-if="$slots.default" class="base-button__text">
      <slot />
    </span>

    <!-- 后置图标 -->
    <span v-if="$slots.iconRight && !loading" class="base-button__icon base-button__icon--right">
      <slot name="iconRight" />
    </span>
  </button>
</template>

<script setup>
// 中文注释：基于设计令牌的可复用按钮组件

defineProps({
  // 按钮变体：primary（主要）、secondary（次要）、ghost（幽灵）、danger（危险）
  variant: {
    type: String,
    default: 'secondary',
    validator: (value) => ['primary', 'secondary', 'ghost', 'danger'].includes(value)
  },

  // 按钮尺寸：small（小）、medium（中）、large（大）
  size: {
    type: String,
    default: 'medium',
    validator: (value) => ['small', 'medium', 'large'].includes(value)
  },

  // 按钮类型
  type: {
    type: String,
    default: 'button',
    validator: (value) => ['button', 'submit', 'reset'].includes(value)
  },

  // 是否禁用
  disabled: {
    type: Boolean,
    default: false
  },

  // 是否加载中
  loading: {
    type: Boolean,
    default: false
  },

  // 是否块级按钮（占满宽度）
  block: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['click'])

// 处理点击事件
const handleClick = (event) => {
  emit('click', event)
}
</script>

<style scoped>
.base-button {
  /* 基础样式使用设计令牌 */
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--filter-btn-gap);
  padding: var(--filter-btn-padding-y) var(--filter-btn-padding-x);
  font-size: var(--filter-btn-font-size);
  font-weight: var(--filter-btn-font-weight);
  line-height: var(--filter-line-height-normal);
  border-radius: var(--filter-btn-radius);
  border: 1px solid transparent;
  cursor: pointer;
  transition: var(--filter-transition-normal);
  text-decoration: none;
  white-space: nowrap;
  user-select: none;
  outline: none;
  position: relative;
  overflow: hidden;
}

.base-button__text {
  flex: 1;
}

.base-button__icon {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.base-button__loading-icon {
  width: 16px;
  height: 16px;
  animation: spin 1s linear infinite;
}

/* 按钮变体样式 */

/* 主要按钮 */
.base-button--primary {
  background: var(--filter-btn-primary-bg);
  color: var(--filter-btn-primary-color);
  border-color: var(--filter-btn-primary-bg);
}

.base-button--primary:hover:not(:disabled) {
  background: var(--filter-btn-primary-hover-bg);
  border-color: var(--filter-btn-primary-hover-bg);
}

.base-button--primary:active:not(:disabled) {
  transform: translateY(1px);
}

/* 次要按钮 */
.base-button--secondary {
  background: var(--filter-btn-secondary-bg);
  color: var(--filter-btn-secondary-color);
  border-color: var(--filter-btn-secondary-border);
}

.base-button--secondary:hover:not(:disabled) {
  border-color: var(--filter-btn-secondary-hover-border);
  color: var(--filter-btn-secondary-hover-color);
  background: var(--filter-color-hover-bg);
}

.base-button--secondary:active:not(:disabled) {
  transform: translateY(1px);
}

/* 幽灵按钮 */
.base-button--ghost {
  background: transparent;
  color: var(--filter-color-text-secondary);
  border-color: transparent;
}

.base-button--ghost:hover:not(:disabled) {
  background: var(--filter-color-hover-bg);
  color: var(--filter-color-text-primary);
}

/* 危险按钮 */
.base-button--danger {
  background: var(--filter-color-danger);
  color: #ffffff;
  border-color: var(--filter-color-danger);
}

.base-button--danger:hover:not(:disabled) {
  background: var(--filter-color-danger-hover);
  border-color: var(--filter-color-danger-hover);
}

/* 按钮尺寸 */

.base-button--small {
  padding: var(--filter-space-sm) var(--filter-space-lg);
  font-size: var(--filter-font-size-sm);
  gap: var(--filter-space-sm);
}

.base-button--small .base-button__loading-icon {
  width: 14px;
  height: 14px;
}

.base-button--medium {
  /* 使用默认令牌值 */
}

.base-button--large {
  padding: var(--filter-space-xl) var(--filter-space-2xl);
  font-size: var(--filter-font-size-lg);
  gap: var(--filter-space-lg);
}

.base-button--large .base-button__loading-icon {
  width: 18px;
  height: 18px;
}

/* 状态样式 */

.base-button--disabled {
  opacity: 0.5;
  cursor: not-allowed;
  pointer-events: none;
}

.base-button--loading {
  cursor: wait;
}

.base-button--loading .base-button__text,
.base-button--loading .base-button__icon {
  opacity: 0.7;
}

/* 块级按钮 */
.base-button--block {
  width: 100%;
}

/* 焦点样式 */
.base-button:focus-visible {
  outline: 2px solid var(--filter-color-focus-ring);
  outline-offset: 2px;
}

/* 加载动画 */
@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

/* 响应式调整 */
@media (max-width: 767px) {
  .base-button {
    padding: calc(var(--filter-btn-padding-y) + 2px) var(--filter-btn-padding-x);
    font-size: var(--filter-font-size-md);
  }

  .base-button--small {
    padding: var(--filter-space-md) var(--filter-space-lg);
  }

  .base-button--large {
    padding: calc(var(--filter-space-xl) + 2px) var(--filter-space-2xl);
  }
}

/* 按钮组合样式（当多个按钮相邻时） */
.base-button + .base-button {
  margin-left: var(--filter-space-lg);
}

/* 在 flex 容器中的按钮间距 */
.base-button-group {
  display: flex;
  gap: var(--filter-space-lg);
  align-items: center;
}

.base-button-group .base-button {
  margin: 0;
}

/* 垂直按钮组 */
.base-button-group--vertical {
  flex-direction: column;
}

.base-button-group--vertical .base-button {
  width: 100%;
}
</style>
