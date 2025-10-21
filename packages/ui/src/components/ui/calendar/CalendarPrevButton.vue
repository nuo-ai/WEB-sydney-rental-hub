<script lang="ts" setup>
import type { HTMLAttributes } from "vue"
import { CalendarPrevButton, useForwardProps } from "reka-ui"
import { cn } from "../../../lib/utils"
import { ChevronLeft } from "lucide-vue-next"

const props = defineProps<{
  disabled?: boolean
  class?: HTMLAttributes["class"]
}>()
const forwardedProps = useForwardProps(props)
</script>

<template>
  <CalendarPrevButton
    v-bind="forwardedProps"
    :class="cn(
      'h-7 w-7 rounded-md p-0 text-sm font-medium ring-offset-background transition-colors hover:bg-accent hover:text-accent-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50',
      props.class,
    )"
  >
    <slot>
      <ChevronLeft class="h-4 w-4" />
    </slot>
  </CalendarPrevButton>
</template>
