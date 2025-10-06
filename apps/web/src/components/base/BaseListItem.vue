<!--
  BaseListItem - 可复用的列表项组件
  基于设计令牌系统构建，提供一致的列表项体验

  使用示例：
  <BaseListItem @click="handleClick">基础列表项</BaseListItem>
  <BaseListItem selected>已选择的项</BaseListItem>
  <BaseListItem disabled>禁用的项</BaseListItem>
-->

<template>
  <div
    class="base-list-item"
    :class="{
      'base-list-item--selected': selected,
      'base-list-item--disabled': disabled,
      'base-list-item--clickable': clickable,
      'base-list-item--bordered': bordered,
    }"
    :role="role"
    :aria-selected="selected"
    :aria-disabled="disabled"
    :tabindex="tabindex"
    @click="handleClick"
    @keydown="handleKeydown"
  >
    <!-- 前置内容插槽 -->
    <div v-if="$slots.prefix" class="base-list-item__prefix">
      <slot name="prefix" />
    </div>

    <!-- 主要内容区域 -->
    <div class="base-list-item__content">
      <!-- 标题 -->
      <div v-if="$slots.default" class="base-list-item__title">
        <slot />
      </div>

      <!-- 描述 -->
      <div v-if="$slots.description" class="base-list-item__description">
        <slot name="description" />
      </div>
    </div>

    <!-- 后置内容插槽 -->
    <div v-if="$slots.suffix" class="base-list-item__suffix">
      <slot name="suffix" />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

// 中文注释：基于设计令牌的可复用列表项组件

const props = defineProps({
  // 是否选中
  selected: {
    type: Boolean,
    default: false,
  },

  // 是否禁用
  disabled: {
    type: Boolean,
    default: false,
  },

  // 是否可点击
  clickable: {
    type: Boolean,
    default: true,
  },

  // 是否显示边框
  bordered: {
    type: Boolean,
    default: true,
  },

  // ARIA 角色
  role: {
    type: String,
    default: 'listitem',
  },
})

const emit = defineEmits(['click', 'select'])

// 计算 tabindex
const tabindex = computed(() => {
  if (props.disabled) return -1
  if (props.clickable) return 0
  return -1
})

// 处理点击事件
const handleClick = (event) => {
  if (props.disabled) return

  emit('click', event)

  if (props.clickable) {
    emit('select', !props.selected)
  }
}

// 处理键盘事件
const handleKeydown = (event) => {
  if (props.disabled) return

  // 空格键或回车键触发点击
  if (event.key === ' ' || event.key === 'Enter') {
    event.preventDefault()
    handleClick(event)
  }
}
</script>

<style scoped>
.base-list-item {
  /* 使用设计令牌 */
  display: flex;
  align-items: center;
  padding: var(--list-item-padding-y) var(--list-item-padding-x);
  min-height: var(--list-item-min-height);
  background: var(--color-bg-primary);
  color: var(--color-text-primary);
  transition: var(--transition-fast);
  position: relative;
}

.base-list-item__prefix {
  display: flex;
  align-items: center;
  margin-right: var(--space-md);
  flex-shrink: 0;
}

.base-list-item__content {
  flex: 1;
  min-width: 0; /* 允许文本截断 */
}

.base-list-item__title {
  font-size: var(--font-size-md);
  font-weight: var(--font-weight-regular);
  line-height: var(--line-height-normal);
  color: var(--color-text-primary);

  /* 文本截断 */
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.base-list-item__description {
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-regular);
  line-height: var(--line-height-normal);
  color: var(--color-text-secondary);
  margin-top: var(--space-2xs);

  /* 文本截断 */
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.base-list-item__suffix {
  display: flex;
  align-items: center;
  margin-left: var(--space-md);
  flex-shrink: 0;
}

/* 边框样式 */
.base-list-item--bordered {
  border-bottom: 1px solid var(--list-item-border);
}

.base-list-item--bordered:last-child {
  border-bottom: none;
}

/* 可点击状态 */
.base-list-item--clickable {
  cursor: pointer;
}

.base-list-item--clickable:hover:not(.base-list-item--disabled) {
  background: var(--list-item-hover-bg);
}

.base-list-item--clickable:active:not(.base-list-item--disabled) {
  background: var(--color-bg-muted);
}

/* 选中状态 */
.base-list-item--selected {
  background: var(--list-item-selected-bg);
  border-color: var(--list-item-selected-border);
}

.base-list-item--selected .base-list-item__title {
  color: var(--color-text-primary);
  font-weight: var(--font-weight-semibold);
}

/* 禁用状态 */
.base-list-item--disabled {
  opacity: 0.5;
  cursor: not-allowed;
  pointer-events: none;
}

/* 焦点样式 */
.base-list-item--clickable:focus-visible {
  outline: 2px solid var(--color-focus-ring);
  outline-offset: -2px;
}

/* 分组标题样式（特殊变体） */
.base-list-item--group-title {
  background: var(--panel-group-bg);
  padding: var(--panel-group-padding-y) var(--panel-group-padding-x);
  font-size: var(--panel-group-font-size);
  font-weight: var(--panel-group-font-weight);
  color: var(--panel-group-color);
  border-bottom: 1px solid var(--panel-group-border);
  position: sticky;
  top: 0;
  z-index: 2;
  cursor: default;
  pointer-events: none;
}

.base-list-item--group-title .base-list-item__title {
  font-size: inherit;
  font-weight: inherit;
  color: inherit;
  letter-spacing: 0.025em;
}

/* 响应式调整 */
@media (width <= 767px) {
  .base-list-item {
    padding: calc(var(--list-item-padding-y) + 2px) var(--list-item-padding-x);
    min-height: calc(var(--list-item-min-height) + 4px);
  }

  .base-list-item__title {
    font-size: var(--font-size-md);
  }

  .base-list-item__description {
    font-size: var(--font-size-sm);
  }

  .base-list-item__prefix {
    margin-right: var(--space-sm);
  }

  .base-list-item__suffix {
    margin-left: var(--space-sm);
  }
}

/* 加载状态（可选扩展） */
.base-list-item--loading {
  position: relative;
  overflow: hidden;
}

.base-list-item--loading::after {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgb(255 255 255 / 40%), transparent);
  animation: shimmer 1.5s infinite;
}

@keyframes shimmer {
  0% {
    left: -100%;
  }

  100% {
    left: 100%;
  }
}

/* 紧凑模式 */
.base-list-item--compact {
  padding: var(--space-xs) var(--list-item-padding-x);
  min-height: auto;
}

.base-list-item--compact .base-list-item__title {
  font-size: var(--font-size-sm);
}

.base-list-item--compact .base-list-item__description {
  font-size: var(--font-size-2xs);
  margin-top: var(--space-2xs);
}

/* 多行文本支持 */
.base-list-item--multiline .base-list-item__title,
.base-list-item--multiline .base-list-item__description {
  white-space: normal;
  overflow: visible;
  text-overflow: initial;
}

.base-list-item--multiline .base-list-item__description {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
