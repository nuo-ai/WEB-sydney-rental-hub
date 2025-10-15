<script setup lang="ts">
import { inject, computed } from 'vue'

const props = defineProps<{
  value: string
}>()

// 从 Tabs 根组件注入
const current = inject<any>('tabs.value', null)
const setValue = inject<((v: string) => void) | null>('tabs.setValue', null)

const selected = computed(() => {
  return (current?.value ?? undefined) === props.value
})

function onClick() {
  setValue?.(props.value)
}
</script>

<template>
  <button
    type="button"
    role="tab"
    :aria-selected="selected"
    :data-state="selected ? 'active' : 'inactive'"
    class="inline-flex items-center justify-center whitespace-nowrap rounded-sm px-3 py-1.5 text-sm font-medium ring-offset-background transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50"
    :class="selected ? 'bg-background text-foreground shadow-sm' : 'text-muted-foreground hover:text-foreground'"
    @click="onClick"
  >
    <slot />
  </button>
</template>
