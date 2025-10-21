<!--
  BaseButton - 可复用的按钮组件
  基于 shadcn-vue Button 组件构建，提供一致的按钮体验

  使用示例：
  <BaseButton @click="handleClick">默认按钮</BaseButton>
  <BaseButton variant="primary" :loading="isLoading">主要按钮</BaseButton>
  <BaseButton variant="secondary" size="small">次要按钮</BaseButton>
-->

<template>
  <Button
    :variant="buttonVariant"
    :size="buttonSize"
    :type="type"
    :disabled="disabled || loading"
    :class="cn(
      block ? 'w-full' : '',
      disabled ? 'opacity-50 cursor-not-allowed pointer-events-none' : '',
      loading ? 'cursor-wait' : ''
    )"
    @click="handleClick"
  >
    <!-- 加载图标 -->
    <Loader2Icon v-if="loading" class="w-4 h-4 animate-spin" />

    <!-- 前置图标 -->
    <slot v-else-if="$slots.icon" name="icon" />

    <!-- 按钮文本 -->
    <slot />

    <!-- 后置图标 -->
    <slot v-if="$slots.iconRight && !loading" name="iconRight" />
  </Button>
</template>

<script setup>
import { computed } from 'vue'
import { Loader2Icon } from 'lucide-vue-next'
import { Button } from './ui/button'
import { cn } from '../lib/utils'

// 中文注释：基于 shadcn-vue 的可复用按钮组件

const props = defineProps({
  // 按钮变体：primary（主要）、secondary（次要）、ghost（幽灵）、link
  variant: {
    type: String,
    default: 'secondary',
    validator: (value) => ['primary', 'secondary', 'ghost', 'link'].includes(value),
  },

  // 按钮尺寸：small（小）、medium（中）、large（大）
  size: {
    type: String,
    default: 'medium',
    validator: (value) => ['small', 'medium', 'large'].includes(value),
  },

  // 按钮类型
  type: {
    type: String,
    default: 'button',
    validator: (value) => ['button', 'submit', 'reset'].includes(value),
  },

  // 是否禁用
  disabled: {
    type: Boolean,
    default: false,
  },

  // 是否加载中
  loading: {
    type: Boolean,
    default: false,
  },

  // 是否块级按钮（占满宽度）
  block: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['click'])

// 映射旧的 variant 到新的 shadcn-vue variant
const buttonVariant = computed(() => {
  const variantMap = {
    primary: 'default',
    secondary: 'secondary',
    ghost: 'ghost',
    link: 'link'
  }
  return variantMap[props.variant] || 'secondary'
})

// 映射旧的 size 到新的 shadcn-vue size
const buttonSize = computed(() => {
  const sizeMap = {
    small: 'sm',
    medium: 'default',
    large: 'lg'
  }
  return sizeMap[props.size] || 'default'
})

// 处理点击事件
const handleClick = (event) => {
  if (!props.disabled && !props.loading) {
    emit('click', event)
  }
}
</script>
