<template>
  <!-- 中文注释：原子化图标按钮。统一命中区尺寸与中性灰交互，图标颜色随 currentColor -->
  <button
    class="base-icon-btn"
    :class="[variantClass, sizeClass]"
    :aria-label="ariaLabel"
    :disabled="disabled"
    type="button"
    @click="onClick"
  >
    <slot />
  </button>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  // 视觉变体：ghost（透明背景，悬停中性灰）/ secondary（中性浅底）
  variant: { type: String, default: 'ghost' }, // 'ghost' | 'secondary'
  // 尺寸：md=36×36（默认），sm=32×32；命中区尺寸遵循无障碍最小标准
  size: { type: String, default: 'md' }, // 'sm' | 'md'
  // 可用性
  disabled: { type: Boolean, default: false },
  // 无障碍标签
  ariaLabel: { type: String, default: '' }
})

const emit = defineEmits(['click'])

const variantClass = computed(() =>
  props.variant === 'secondary' ? 'variant-secondary' : 'variant-ghost'
)
const sizeClass = computed(() => (props.size === 'sm' ? 'size-sm' : 'size-md'))

function onClick(e) {
  if (props.disabled) return
  emit('click', e)
}
</script>

<style scoped>
/* 基础样式：令牌化 + 可达性 */
.base-icon-btn {
  /* 中文注释：统一图标按钮基线样式，图标颜色继承 currentColor */
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border: 1px solid var(--color-border-default);
  color: var(--color-text-secondary);
  background: transparent;
  padding: 0;
  cursor: pointer;
  border-radius: var(--radius-full, 9999px);
  transition:
    background-color var(--motion-base, 180ms) var(--easing-standard, cubic-bezier(0.2, 0, 0, 1)),
    color var(--motion-base, 180ms) var(--easing-standard, cubic-bezier(0.2, 0, 0, 1)),
    transform var(--motion-fast, 120ms) var(--easing-standard, cubic-bezier(0.2, 0, 0, 1));
}

/* 尺寸命中区 */
.base-icon-btn.size-md { width: 36px; height: 36px; }
.base-icon-btn.size-sm { width: 32px; height: 32px; }

/* 视觉变体 */
.base-icon-btn.variant-ghost { background: transparent; }
.base-icon-btn.variant-secondary { background: var(--surface-2, transparent); }

.base-icon-btn:hover {
  background: var(--bg-hover);
  color: var(--color-text-primary);
}

.base-icon-btn:active {
  transform: translateY(1px);
}

.base-icon-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* 插槽内图标统一尺寸与颜色（图标应使用 currentColor） */
.base-icon-btn :deep(svg),
.base-icon-btn :deep(.spec-icon) {
  width: 18px;
  height: 18px;
  stroke: currentColor;
  fill: currentColor; /* 兜底：部分图标使用 fill 渲染 */
}
</style>
