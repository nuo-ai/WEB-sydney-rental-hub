<!--
  BaseSearchInput - 可复用的搜索输入框组件
  基于设计令牌系统构建，提供一致的搜索体验

  使用示例：
  <BaseSearchInput v-model="keyword" placeholder="搜索区域" @clear="handleClear" />
  <BaseSearchInput v-model="query" :clearable="false" />
-->

<template>
  <div class="base-search-input">
    <div class="base-search-input__wrapper">
      <!-- 搜索图标 -->
      <svg
        class="base-search-input__icon"
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
        stroke-linecap="round"
        stroke-linejoin="round"
        aria-hidden="true"
      >
        <circle cx="11" cy="11" r="8" />
        <path d="m21 21-4.35-4.35" />
      </svg>

      <!-- 输入框 -->
      <input
        ref="inputRef"
        v-model="inputValue"
        type="text"
        class="base-search-input__field"
        :placeholder="placeholder"
        :disabled="disabled"
        :aria-label="ariaLabel || placeholder"
        @input="handleInput"
        @focus="handleFocus"
        @blur="handleBlur"
        @keydown="handleKeydown"
      />

      <!-- 清除按钮 -->
      <button
        v-if="clearable && inputValue && !disabled"
        class="base-search-input__clear"
        type="button"
        :aria-label="clearLabel"
        @click="handleClear"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
        >
          <path d="M18 6 6 18M6 6l12 12" />
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, nextTick } from 'vue'

// 中文注释：基于设计令牌的可复用搜索输入框组件

const props = defineProps({
  // v-model 绑定值
  modelValue: {
    type: String,
    default: '',
  },

  // 占位符文本
  placeholder: {
    type: String,
    default: '搜索...',
  },

  // 是否显示清除按钮
  clearable: {
    type: Boolean,
    default: true,
  },

  // 是否禁用
  disabled: {
    type: Boolean,
    default: false,
  },

  // 无障碍标签
  ariaLabel: {
    type: String,
    default: '',
  },

  // 清除按钮的无障碍标签
  clearLabel: {
    type: String,
    default: '清除搜索',
  },

  // 是否自动聚焦
  autofocus: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['update:modelValue', 'input', 'focus', 'blur', 'clear', 'keydown'])

// 模板引用
const inputRef = ref(null)

// 内部值管理
const inputValue = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value),
})

// 事件处理
const handleInput = (event) => {
  emit('input', event.target.value, event)
}

const handleFocus = (event) => {
  emit('focus', event)
}

const handleBlur = (event) => {
  emit('blur', event)
}

const handleClear = () => {
  inputValue.value = ''
  emit('clear')
  // 清除后重新聚焦输入框
  nextTick(() => {
    if (inputRef.value) {
      inputRef.value.focus()
    }
  })
}

const handleKeydown = (event) => {
  emit('keydown', event)

  // ESC 键清除内容
  if (event.key === 'Escape' && props.clearable && inputValue.value) {
    handleClear()
    event.preventDefault()
  }
}

// 公开方法
const focus = () => {
  if (inputRef.value) {
    inputRef.value.focus()
  }
}

const blur = () => {
  if (inputRef.value) {
    inputRef.value.blur()
  }
}

// 自动聚焦
if (props.autofocus) {
  nextTick(() => {
    focus()
  })
}

// 暴露方法给父组件
defineExpose({
  focus,
  blur,
  inputRef,
})
</script>

<style scoped>
.base-search-input {
  position: relative;
  width: 100%;
}

.base-search-input__wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.base-search-input__icon {
  position: absolute;
  left: var(--filter-search-icon-left);
  width: var(--filter-search-icon-size);
  height: var(--filter-search-icon-size);
  color: var(--filter-search-icon-color);
  pointer-events: none;
  z-index: 1;
}

.base-search-input__field {
  width: 100%;
  padding: var(--filter-search-padding-y) var(--filter-search-padding-x)
    var(--filter-search-padding-y) var(--filter-search-padding-left);
  font-size: var(--filter-search-font-size);
  color: var(--filter-color-text-primary);
  background: var(--filter-color-bg-primary);
  border: 1px solid var(--filter-search-border);
  border-radius: var(--filter-search-radius);
  outline: none;
  transition: var(--filter-transition-normal);
  line-height: var(--filter-line-height-normal);
}

.base-search-input__field::placeholder {
  color: var(--filter-color-text-muted);
}

.base-search-input__field:focus {
  border-color: var(--filter-search-focus-border);
  box-shadow: var(--filter-shadow-focus);
}

.base-search-input__field:hover:not(:focus):not(:disabled) {
  border-color: var(--filter-search-hover-border);
}

.base-search-input__field:disabled {
  background: var(--filter-color-bg-muted);
  color: var(--filter-color-text-muted);
  cursor: not-allowed;
}

.base-search-input__clear {
  position: absolute;
  right: var(--filter-clear-btn-right);
  background: none;
  border: none;
  color: var(--filter-color-text-secondary);
  cursor: pointer;
  padding: var(--filter-clear-btn-padding);
  border-radius: var(--filter-clear-btn-radius);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: var(--filter-transition-fast);
  width: var(--filter-clear-btn-size);
  height: var(--filter-clear-btn-size);
}

.base-search-input__clear svg {
  width: var(--filter-clear-btn-size);
  height: var(--filter-clear-btn-size);
}

.base-search-input__clear:hover {
  background: var(--filter-clear-btn-hover-bg);
  color: var(--filter-color-text-primary);
}

.base-search-input__clear:focus-visible {
  outline: 2px solid var(--filter-color-focus-ring);
  outline-offset: 1px;
}

/* 有清除按钮时调整输入框右内边距 */
.base-search-input__field:not(:disabled) {
  padding-right: calc(
    var(--filter-clear-btn-right) * 2 + var(--filter-clear-btn-size) +
      var(--filter-clear-btn-padding) * 2
  );
}

/* 响应式调整 */
@media (max-width: 767px) {
  .base-search-input__field {
    font-size: 16px; /* iOS 防缩放 */
    padding: calc(var(--filter-search-padding-y) + 2px) var(--filter-search-padding-x)
      calc(var(--filter-search-padding-y) + 2px) var(--filter-search-padding-left);
  }

  .base-search-input__clear {
    width: calc(var(--filter-clear-btn-size) + 4px);
    height: calc(var(--filter-clear-btn-size) + 4px);
    padding: calc(var(--filter-clear-btn-padding) + 2px);
  }
}

/* 加载状态（可选扩展） */
.base-search-input--loading .base-search-input__icon {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>
