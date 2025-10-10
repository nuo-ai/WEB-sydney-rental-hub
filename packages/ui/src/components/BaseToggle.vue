<template>
  <!-- 中文注释：原子化开关。语义使用 role="switch" + aria-checked，键盘支持 Space/Enter -->
  <button
    class="base-toggle"
    :class="[sizeClass, { 'is-on': modelValue, disabled }]"
    role="switch"
    :aria-checked="String(modelValue)"
    :aria-label="ariaLabel"
    :disabled="disabled"
    type="button"
    @click="toggle"
    @keydown.space.prevent="toggle"
    @keydown.enter.prevent="toggle"
  >
    <span class="toggle-track" aria-hidden="true">
      <span class="toggle-thumb"></span>
    </span>
    <span v-if="showLabels" class="toggle-text">
      {{ modelValue ? labels.on : labels.off }}
    </span>
  </button>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  modelValue: { type: Boolean, default: false },
  size: { type: String, default: 'md' }, // 'sm' | 'md'
  disabled: { type: Boolean, default: false },
  ariaLabel: { type: String, default: '' },
  showLabels: { type: Boolean, default: true },
  labels: {
    type: Object,
    default: () => ({ on: 'On', off: 'Off' }),
  },
})

const emit = defineEmits(['update:modelValue', 'change'])

const sizeClass = computed(() => (props.size === 'sm' ? 'size-sm' : 'size-md'))

function toggle() {
  if (props.disabled) return
  const next = !props.modelValue
  emit('update:modelValue', next)
  emit('change', next)
}
</script>

<style scoped>
.base-toggle {
  display: inline-flex;
  align-items: center;
  gap: var(--component-toggle-text-gap);
  border: 0;
  background: transparent;
  color: var(--component-toggle-text-color);
  cursor: pointer;
  padding: 0;
  transition: var(--component-toggle-transition);
}

.base-toggle.disabled,
.base-toggle:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.base-toggle .toggle-track {
  position: relative;
  display: inline-block;
  background: var(--component-toggle-track-off-bg);
  border: 1px solid var(--component-toggle-track-off-border);
  border-radius: 9999px;
  transition: inherit;
  box-sizing: border-box;
}

.base-toggle .toggle-thumb {
  position: absolute;
  top: 50%;
  background: var(--component-toggle-thumb-bg);
  border: 1px solid var(--component-toggle-thumb-border);
  border-radius: 9999px;
  transform: translate(0, -50%);
  transition: inherit;
  box-sizing: border-box;
}

/* 尺寸：md (默认) */
.base-toggle.size-md .toggle-track {
  width: var(--component-toggle-md-width);
  height: var(--component-toggle-md-height);
}
.base-toggle.size-md .toggle-thumb {
  left: var(--component-toggle-md-padding);
  width: var(--component-toggle-md-thumb-size);
  height: var(--component-toggle-md-thumb-size);
}

/* 尺寸：sm */
.base-toggle.size-sm .toggle-track {
  width: var(--component-toggle-sm-width);
  height: var(--component-toggle-sm-height);
}
.base-toggle.size-sm .toggle-thumb {
  left: var(--component-toggle-sm-padding);
  width: var(--component-toggle-sm-thumb-size);
  height: var(--component-toggle-sm-thumb-size);
}

/* on 态：使用品牌主色作为轨道背景；thumb 移至右侧 */
.base-toggle.is-on .toggle-track {
  background: var(--component-toggle-track-on-bg);
  border-color: var(--component-toggle-track-on-border);
}
.base-toggle.is-on .toggle-thumb {
  border-color: var(--component-toggle-track-on-border);
}
.base-toggle.size-md.is-on .toggle-thumb {
  transform: translate(calc(var(--component-toggle-md-width) - var(--component-toggle-md-thumb-size) - var(--component-toggle-md-padding) * 2), -50%);
}
.base-toggle.size-sm.is-on .toggle-thumb {
  transform: translate(calc(var(--component-toggle-sm-width) - var(--component-toggle-sm-thumb-size) - var(--component-toggle-sm-padding) * 2), -50%);
}

/* hover：中性灰加强 */
.base-toggle:not(.disabled):hover .toggle-track {
  border-color: var(--component-toggle-track-hover-border);
}

/* 文案（可选） */
.toggle-text {
  font-size: var(--component-toggle-text-font-size);
  font-weight: var(--component-toggle-text-font-weight);
  color: var(--component-toggle-text-color);
}

/* 焦点可见性：中性可见焦点 */
.base-toggle:focus-visible .toggle-track {
  outline: 2px solid var(--component-toggle-focus-outline);
  outline-offset: 2px;
}
</style>
