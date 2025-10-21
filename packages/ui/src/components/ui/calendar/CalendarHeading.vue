<script lang="ts" setup>
import type { CalendarHeadingProps } from "reka-ui"
import { CalendarHeading, useForwardProps } from "reka-ui"
import { cn } from "../../../lib/utils"

const props = defineProps<CalendarHeadingProps>()
const forwardedProps = useForwardProps(props)
</script>

<template>
  <CalendarHeading
    v-bind="forwardedProps"
    :class="cn('text-sm font-medium', props.class)"
  >
    <slot />
  </CalendarHeading>
</template>
