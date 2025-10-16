<script setup lang="ts">
/*
  文件职责：展示房源规格三元组（卧室/浴室/车位）
  为什么：在卡片与详情等多处复用，统一视觉与间距
  技术权衡：
  - 为避免引入额外图标库，使用 emoji 作为占位；后续可由上层替换为统一图标组件
  - 保持最小 props；若需要自定义图标/顺序，可使用插槽或后续扩展
*/

const props = withDefaults(defineProps<{
  beds: number
  baths: number
  cars: number
}>(), {})
</script>

<template>
  <div class="flex items-center gap-6 text-gray-700">
    <div class="flex items-center gap-2 text-sm">
      <span aria-hidden="true">🛏️</span>
      <span>{{ props.beds }}</span>
    </div>
    <div class="flex items-center gap-2 text-sm">
      <span aria-hidden="true">🛁</span>
      <span>{{ props.baths }}</span>
    </div>
    <div class="flex items-center gap-2 text-sm">
      <span aria-hidden="true">🚗</span>
      <span>{{ props.cars }}</span>
    </div>
  </div>
</template>
