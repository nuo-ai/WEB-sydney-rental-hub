<!--
  BaseCard - 可复用的卡片组件
  用于包裹内容，提供清晰的视觉边界
-->
<template>
  <div class="base-card">
    <slot />
  </div>
</template>

<script setup>
// No props needed for this basic version
</script>

<style scoped>
.base-card {
  background-color: var(--color-semantic-bg-primary);
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-semantic-border-subtle);
  padding: var(--space-xl);
  box-shadow: var(--shadow-sm);
  transition: box-shadow 0.2s;
}

.base-card:hover {
  box-shadow: var(--shadow-md);
}
</style>
