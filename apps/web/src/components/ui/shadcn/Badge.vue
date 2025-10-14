<script setup lang="ts">
import { badgeVariants } from './badge'
import { cn } from '@/lib/utils'

interface Props {
  variant?: NonNullable<Parameters<typeof badgeVariants>[0]>['variant']
}

defineProps<Props>()
</script>

<template>
  <div :class="cn(badgeVariants({ variant }), $attrs.class ?? '')">
    <slot />
  </div>
</template>
