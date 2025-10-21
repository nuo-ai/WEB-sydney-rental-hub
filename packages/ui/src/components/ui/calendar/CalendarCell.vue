<script lang="ts" setup>
import type { CalendarCellProps } from "reka-ui"
import { CalendarCell, useForwardProps } from "reka-ui"
import { cn } from "../../../lib/utils"

const props = defineProps<CalendarCellProps>()
const forwardedProps = useForwardProps(props)
</script>

<template>
  <CalendarCell v-bind="forwardedProps">
    <slot />
  </CalendarCell>
</template>
