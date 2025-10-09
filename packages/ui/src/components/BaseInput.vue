<!--
  BaseInput - 可复用的输入框组件
  基于设计令牌系统构建，提供一致的表单体验
-->
<template>
  <div class="base-input-wrapper">
    <input
      class="base-input"
      :value="modelValue"
      @input="$emit('update:modelValue', $event.target.value)"
      :placeholder="placeholder"
      :disabled="disabled"
    />
  </div>
</template>

<script setup>
defineProps({
  modelValue: {
    type: [String, Number],
    default: '',
  },
  placeholder: {
    type: String,
    default: '请输入内容...',
  },
  disabled: {
    type: Boolean,
    default: false,
  },
});

defineEmits(['update:modelValue']);
</script>

<style scoped>
.base-input {
  width: 100%;
  padding: var(--space-sm) var(--space-md);
  font-size: var(--font-size-md);
  color: var(--color-semantic-text-primary);
  background-color: var(--color-semantic-bg-primary);
  border: 1px solid var(--color-semantic-border-default);
  border-radius: var(--radius-md);
  transition: border-color 0.2s, box-shadow 0.2s;
}

.base-input:focus {
  outline: none;
  border-color: var(--color-brand-primary);
  box-shadow: 0 0 0 2px rgba(0, 87, 255, 0.2);
}

.base-input::placeholder {
  color: var(--color-semantic-text-muted);
}

.base-input:disabled {
  background-color: var(--color-semantic-bg-secondary);
  cursor: not-allowed;
}
</style>
