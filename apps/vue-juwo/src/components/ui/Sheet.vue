<script setup lang="ts">
import { Dialog, DialogPanel, DialogTitle, DialogDescription } from '@headlessui/vue'
import type { HTMLAttributes } from 'vue'
import { cn } from '@/lib/utils'

const props = defineProps<{
  open?: boolean
  class?: HTMLAttributes['class']
}>()

const emit = defineEmits<{
  (e: 'update:open', value: boolean): void
}>()

function close() {
  emit('update:open', false)
}
</script>

<template>
  <Dialog :open="open" @close="close" class="relative z-50">
    <!-- Backdrop -->
    <div class="fixed inset-0 bg-black/30" aria-hidden="true" />
    
    <!-- Dialog container -->
    <div class="fixed inset-0 flex items-center justify-center p-4">
      <DialogPanel
        :class="cn('w-full max-w-md rounded-lg bg-white p-6 shadow-lg', props.class)"
      >
        <slot name="header">
          <DialogTitle v-if="$slots.title" class="text-lg font-semibold">
            <slot name="title" />
          </DialogTitle>
          <DialogDescription v-if="$slots.description" class="mt-1 text-sm text-gray-500">
            <slot name="description" />
          </DialogDescription>
        </slot>
        
        <slot />
        
        <slot name="footer" />
      </DialogPanel>
    </div>
  </Dialog>
</template>
