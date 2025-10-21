<script lang="ts" setup>
import type { CalendarHeadCellProps } from "reka-ui"
import { CalendarHeadCell, useForwardProps } from "reka-ui"
import { cn } from "../../../lib/utils"

const props = defineProps<CalendarHeadCellProps>()
const forwardedProps = useForwardProps(props)
</script>

<template>
  <CalendarHeadCell
    v-bind="forwardedProps"
    :class="cn('w-9 rounded-md text-sm font-normal text-muted-foreground', props.class)"
  >
    <slot />
  </CalendarHeadCell>
</template>
