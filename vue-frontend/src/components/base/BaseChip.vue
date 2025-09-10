<!--
  BaseChip - 可复用的标签组件
  基于设计令牌系统构建，提供一致的视觉风格

  使用示例：
  <BaseChip @remove="handleRemove">区域名称</BaseChip>
  <BaseChip variant="selected" removable>已选择</BaseChip>
-->

<template>
  <div class="base-chip" :class="[`base-chip--${variant}`, { 'base-chip--removable': removable }]">
    <span class="base-chip__text">
      <slot />
    </span>
    <button
      v-if="removable"
      class="base-chip__remove"
      type="button"
      :aria-label="removeLabel"
      @click="handleRemove"
    >
      ×
    </button>
  </div>
</template>

<script setup>
// 中文注释：基于设计令牌的可复用标签组件

defineProps({
  // 变体类型：default（默认）、selected（选中）、hover（悬浮）
  variant: {
    type: String,
    default: 'default',
    validator: (value) => ['default', 'selected', 'hover'].includes(value),
  },

  // 是否可移除
  removable: {
    type: Boolean,
    default: true,
  },

  // 移除按钮的无障碍标签
  removeLabel: {
    type: String,
    default: '移除',
  },
})

const emit = defineEmits(['remove'])

// 处理移除事件
const handleRemove = (event) => {
  event.stopPropagation()
  emit('remove')
}
</script>

<style scoped>
.base-chip {
  /* 使用设计令牌 */
  display: inline-flex;
  align-items: center;
  gap: var(--filter-chip-gap);
  padding: var(--filter-chip-padding-y) var(--filter-chip-padding-x);
  border: 1px solid var(--filter-chip-border);
  border-radius: var(--filter-chip-radius);
  background: var(--filter-chip-bg);
  color: var(--filter-chip-text);
  font-size: var(--filter-chip-font-size);
  font-weight: var(--filter-chip-font-weight);
  line-height: var(--filter-line-height-normal);
  max-width: 200px;
  transition: var(--filter-transition-fast);
  cursor: default;
}

.base-chip__text {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  flex: 1;
}

.base-chip__remove {
  background: var(--filter-chip-remove-bg);
  border: none;
  color: var(--filter-chip-remove-color);
  width: var(--filter-chip-remove-size);
  height: var(--filter-chip-remove-size);
  border-radius: var(--filter-chip-remove-radius);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  line-height: 1;
  padding: 0;
  cursor: pointer;
  transition: var(--filter-transition-fast);
  flex-shrink: 0;
}

/* 悬浮状态 */
.base-chip:hover {
  border-color: var(--filter-chip-hover-border);
  background: var(--filter-chip-hover-bg);
}

.base-chip__remove:hover {
  background: var(--filter-chip-remove-hover-bg);
  color: var(--filter-chip-remove-hover-color);
}

/* 变体样式 */
.base-chip--selected {
  background: var(--filter-color-selected-bg);
  border-color: var(--filter-color-selected-border);
  color: var(--filter-color-text-primary);
  font-weight: var(--filter-font-weight-semibold);
}

.base-chip--hover {
  background: var(--filter-chip-hover-bg);
  border-color: var(--filter-chip-hover-border);
}

/* 可移除状态的额外样式 */
.base-chip--removable {
  padding-right: calc(var(--filter-chip-padding-x) - 2px); /* 为移除按钮调整内边距 */
}

/* 无障碍支持 */
.base-chip__remove:focus-visible {
  outline: 2px solid var(--filter-color-focus-ring);
  outline-offset: 1px;
}

/* 响应式调整 */
@media (max-width: 767px) {
  .base-chip {
    font-size: var(--filter-font-size-md); /* 移动端稍大字体 */
    padding: calc(var(--filter-chip-padding-y) + 1px) var(--filter-chip-padding-x);
  }

  .base-chip__remove {
    width: calc(var(--filter-chip-remove-size) + 2px);
    height: calc(var(--filter-chip-remove-size) + 2px);
  }
}
</style>
