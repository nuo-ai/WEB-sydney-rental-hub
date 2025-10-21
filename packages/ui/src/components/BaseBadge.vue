<template>
  <Badge
    :variant="badgeVariant"
    :class="[
      {
        'rounded-full': pill,
        'rounded-sm normal-case tracking-normal': !pill,
      },
    ]"
  >
    <slot />
  </Badge>
</template>

<script setup>
import { computed } from 'vue'
import { Badge } from './ui/badge'

const props = defineProps({
  // 中文注释：默认品牌色，支撑"新上线"等高亮标签
  variant: {
    type: String,
    default: 'brand',
    validator: (value) =>
      ['brand', 'neutral', 'success', 'warning', 'danger', 'info'].includes(value),
  },
  // 中文注释：开启后前端表现为完全圆角的胶囊态（配合小写字母更友好）
  pill: {
    type: Boolean,
    default: true,
  },
})

// 映射旧的 variant 到新的 shadcn-vue variant
const badgeVariant = computed(() => {
  const variantMap = {
    brand: 'default',
    neutral: 'outline',
    success: 'secondary',
    warning: 'destructive',
    danger: 'destructive',
    info: 'secondary'
  }
  return variantMap[props.variant] || 'default'
})
</script>
