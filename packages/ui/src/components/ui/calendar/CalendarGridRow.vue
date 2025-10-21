<script lang="ts" setup>
import type { CalendarGridRowProps } from "reka-ui"
import { CalendarGridRow, useForwardProps } from "reka-ui"
import { cn } from "../../../lib/utils"

const props = defineProps<CalendarGridRowProps>()
const forwardedProps = useForwardProps(props)
</script>

<template>
  <CalendarGridRow
    v-bind="forwardedProps"
    :class="cn('flex', props.class)"
  >
    <slot />
  </CalendarGridRow>
</template>
