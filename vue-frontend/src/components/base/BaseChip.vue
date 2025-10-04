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
  line-height: var(--line-height-normal);
  max-width: 200px;
  transition: var(--transition-fast);
  cursor: default;
}

.base-chip__text {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  flex: 1;
}

.base-chip__remove {
  /* 使用中性 remove 背景，避免父级选中/hover 背景透出 */
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
  transition: var(--transition-fast);
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

/* 选中/hover 场景下，仍保持 x 的中性背景，避免父级底色透出 */
.base-chip:hover .base-chip__remove,
.base-chip--selected .base-chip__remove,
.base-chip.base-chip--hover .base-chip__remove {
  background: var(--filter-chip-remove-bg) !important;
}

/* 规范化原生外观与点击高亮（消除桌面端浅蓝背景） */
.base-chip__remove {
  -webkit-appearance: none;
  appearance: none;
  -webkit-tap-highlight-color: transparent;
}

.base-chip__remove:active {
  /* 点击时使用 hover-bg，非选中/焦点时保持透明 */
  background: var(--filter-chip-remove-hover-bg);
  color: var(--filter-chip-remove-hover-color);
}

/* 变体样式 */
.base-chip--selected {
  background: var(--color-selected-bg);
  border-color: var(--color-selected-border);
  color: var(--color-text-primary);
  font-weight: var(--font-weight-semibold);
}

.base-chip--hover {
  background: var(--filter-chip-hover-bg);
  border-color: var(--filter-chip-hover-border);
}

/* 可移除状态的额外样式 */
.base-chip--removable {
  padding-right: calc(var(--filter-chip-padding-x) - 2px); /* 为移除按钮调整内边距 */
}

/* 无障碍支持（中性化：移除浏览器默认浅蓝高亮） */
.base-chip__remove:focus,
.base-chip__remove:focus-visible {
  outline: none !important;
  box-shadow: none !important;
  /* 焦点保持中性 remove 背景，避免父级选中底色透出 */
  background: var(--filter-chip-remove-bg) !important;
  color: var(--filter-chip-remove-color) !important;
}

/* Firefox 内边距/边框清理，避免焦点内边线 */
.base-chip__remove::-moz-focus-inner {
  border: 0;
  padding: 0;
}

/* 响应式调整 */
@media (width <= 767px) {
  .base-chip {
    font-size: var(--font-size-sm); /* 移动端稍大字体 */
    padding: calc(var(--filter-chip-padding-y) + 1px) var(--filter-chip-padding-x);
  }

  .base-chip__remove {
    width: calc(var(--filter-chip-remove-size) + 2px);
    height: calc(var(--filter-chip-remove-size) + 2px);
  }
}
</style>
