<template>
  <button type="button" class="base-button" :class="buttonClasses">
    <slot></slot>
  </button>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  primary: {
    type: Boolean,
    default: false,
  },
  size: {
    type: String,
    default: 'md',
    validator: function (value) {
      return ['sm', 'md', 'lg'].indexOf(value) !== -1;
    },
  },
});

const buttonClasses = computed(() => ({
  'base-button--primary': props.primary,
  [`base-button--${props.size}`]: true,
}));
</script>

<style scoped>
.base-button {
  /* Font tokens */
  font-family: sans-serif;
  font-weight: var(--font-weight-bold);
  border: 0;
  cursor: pointer;
  display: inline-block;
  line-height: 1;

  /* Shape tokens */
  border-radius: var(--radius-md);

  /* Default Colors (non-primary) */
  color: var(--color-semantic-text-primary);
  background-color: var(--color-white);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--color-semantic-border-default);
}

.base-button--primary {
  /* Component tokens */
  color: var(--component-button-primary-color);
  background-color: var(--component-button-primary-bg);
  border: 1px solid transparent;
}

.base-button--primary:hover {
    background-color: var(--color-brand-hover);
}

.base-button--sm {
  font-size: var(--font-size-sm);
  padding: var(--space-sm) var(--space-md);
}
.base-button--md {
  font-size: var(--font-size-md);
  padding: var(--space-md) var(--space-lg);
}
.base-button--lg {
  font-size: var(--font-size-lg);
  padding: var(--space-lg) var(--space-xl);
}
</style>
