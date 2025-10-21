<script lang="ts" setup>
import type { CalendarGridProps } from "reka-ui"
import { CalendarGrid, useForwardProps } from "reka-ui"
import { cn } from "../../../lib/utils"

const props = defineProps<CalendarGridProps>()
const forwardedProps = useForwardProps(props)
</script>

<template>
  <CalendarGrid
    v-bind="forwardedProps"
    :class="cn('w-full border-collapse space-y-1', props.class)"
  >
    <slot />
  </CalendarGrid>
</template>
