<script setup lang="ts">
import { inject, computed } from "vue"
import type { HTMLAttributes } from "vue"
import { cn } from "../../../lib/utils"

const props = withDefaults(defineProps<{
  value: string
  disabled?: boolean
  class?: HTMLAttributes["class"]
}>(), {
  disabled: false,
})

const ctx = inject<{
  valueRef: { value: string | null }
  setValue: (v: string | null) => void
}>("srh-tabs-ctx")

if (!ctx) {
  throw new Error("[TabsTrigger] must be used inside <Tabs> root")
}

const isActive = computed(() => ctx.valueRef.value === props.value)

function onClick() {
  if (props.disabled) return
  ctx.setValue(props.value)
}
</script>

<template>
  <button
    role="tab"
    type="button"
    :aria-selected="isActive"
    :disabled="disabled"
    :data-state="isActive ? 'active' : 'inactive'"
    @click="onClick"
    :class="cn(
      'inline-flex items-center justify-center whitespace-nowrap rounded-sm px-3 py-1.5 text-sm font-medium ring-offset-background transition-all',
      'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2',
      'disabled:pointer-events-none disabled:opacity-50',
      // active/inactive 风格（对齐 shadcn）
      'data-[state=active]:bg-background data-[state=active]:text-foreground data-[state=active]:shadow',
      'data-[state=inactive]:text-muted-foreground',
      props.class
    )"
  >
    <slot />
  </button>
</template>
