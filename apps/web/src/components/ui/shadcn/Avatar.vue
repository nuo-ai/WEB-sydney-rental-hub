<script setup lang="ts">
import { Avatar, AvatarFallback, AvatarImage } from 'radix-vue'
import { cn } from '@/lib/utils'

const props = defineProps({
  class: {
    type: String,
    default: '',
  },
  src: {
    type: String,
    default: '',
  },
  alt: {
    type: String,
    default: '',
  },
  fallback: {
    type: String,
    default: '',
  },
})
</script>

<template>
  <Avatar :class="cn('h-10 w-10', props.class)">
    <AvatarImage :src="src" :alt="alt" />
    <AvatarFallback>{{ fallback }}</AvatarFallback>
  </Avatar>
</template>
