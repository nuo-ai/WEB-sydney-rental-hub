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
/* 中文注释：令牌化，不引入硬编码色；on 态使用品牌主色，off 态中性灰 */
.base-toggle {
  --toggle-w-md: 42px;
  --toggle-h-md: 24px;
  --toggle-w-sm: 36px;
  --toggle-h-sm: 20px;
  --thumb-d-md: 18px;
  --thumb-d-sm: 16px;
  --pad: 3px;

  display: inline-flex;
  align-items: center;
  gap: 8px;
  border: 0;
  background: transparent;
  color: var(--color-text-secondary);
  cursor: pointer;
  padding: 0;
}

.base-toggle.disabled,
.base-toggle:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.base-toggle .toggle-track {
  position: relative;
  display: inline-block;
  width: var(--toggle-w-md);
  height: var(--toggle-h-md);
  background: var(--surface-2, var(--bg-hover));
  border: 1px solid var(--color-border-default);
  border-radius: 9999px;
  transition:
    background-color var(--motion-base, 180ms) var(--easing-standard, cubic-bezier(0.2, 0, 0, 1)),
    border-color var(--motion-base, 180ms) var(--easing-standard, cubic-bezier(0.2, 0, 0, 1));
  box-sizing: border-box;
}

.base-toggle .toggle-thumb {
  position: absolute;
  top: 50%;
  left: var(--pad);
  width: var(--thumb-d-md);
  height: var(--thumb-d-md);
  background: var(--color-bg-card);
  border: 1px solid var(--color-border-default);
  border-radius: 9999px;
  transform: translate(0, -50%);
  transition:
    transform var(--motion-fast, 120ms) var(--easing-standard, cubic-bezier(0.2, 0, 0, 1)),
    border-color var(--motion-base, 180ms) var(--easing-standard, cubic-bezier(0.2, 0, 0, 1));
  box-sizing: border-box;
}

/* 尺寸：sm */
.base-toggle.size-sm .toggle-track {
  width: var(--toggle-w-sm);
  height: var(--toggle-h-sm);
}
.base-toggle.size-sm .toggle-thumb {
  width: var(--thumb-d-sm);
  height: var(--thumb-d-sm);
}

/* on 态：使用品牌主色作为轨道背景；thumb 移至右侧 */
.base-toggle.is-on .toggle-track {
  background: var(--juwo-primary);
  border-color: var(--juwo-primary);
}
.base-toggle.is-on .toggle-thumb {
  border-color: var(--juwo-primary);
  transform: translate(calc(var(--toggle-w-md) - var(--thumb-d-md) - var(--pad) * 2), -50%);
}
.base-toggle.size-sm.is-on .toggle-thumb {
  transform: translate(calc(var(--toggle-w-sm) - var(--thumb-d-sm) - var(--pad) * 2), -50%);
}

/* hover：中性灰加强 */
.base-toggle:not(.disabled):hover .toggle-track {
  border-color: var(--color-border-strong, var(--color-border-default));
}

/* 文案（可选） */
.toggle-text {
  font-size: 12px;
  font-weight: 500;
  color: var(--color-text-secondary);
}

/* 焦点可见性：中性可见焦点 */
.base-toggle:focus-visible .toggle-track {
  outline: 2px solid var(--color-border-strong);
  outline-offset: 2px;
}
</style>
