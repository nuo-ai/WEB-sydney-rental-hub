<script setup lang="ts">
/*
  文件职责：展示价格与周期（如 $500 每周）
  为什么：卡片头部价格区复用性高，抽出分子组件便于统一格式/样式
  技术权衡：
  - 价格格式统一由 utils.formatPrice 处理（$ 与千位分隔）
  - 周期保持文案传入，当前固定“每周”，保留扩展空间
*/

import { formatPrice } from '@/utils/ui'

const props = withDefaults(defineProps<{
  price: number
  period: string // 示例：'每周'
}>(), {
  period: '每周',
})
</script>

<template>
  <div class="flex items-baseline gap-2">
    <span class="text-xl font-bold text-gray-900">{{ formatPrice(props.price) }}</span>
    <span class="text-sm text-gray-500">{{ props.period }}</span>
  </div>
</template>
