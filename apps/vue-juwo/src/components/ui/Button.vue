<script setup lang="ts">
import type { HTMLAttributes } from 'vue'
import { cn } from '@/lib/utils'
import { type ButtonVariants, buttonVariants } from './buttonVariants'

interface Props {
  variant?: ButtonVariants['variant']
  size?: ButtonVariants['size']
  as?: string
  class?: HTMLAttributes['class']
}

const props = withDefaults(defineProps<Props>(), {
  as: 'button',
})
</script>

<template>
  <component
    :is="as"
    :class="cn(buttonVariants({ variant, size }), props.class)"
  >
    <slot />
  </component>
</template>
