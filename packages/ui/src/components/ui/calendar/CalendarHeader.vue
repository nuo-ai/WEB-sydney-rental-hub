<script lang="ts" setup>
import type { CalendarHeaderProps } from "reka-ui"
import { CalendarHeader, useForwardProps } from "reka-ui"
import { cn } from "../../../lib/utils"

const props = defineProps<CalendarHeaderProps>()
const forwardedProps = useForwardProps(props)
</script>

<template>
  <CalendarHeader
    v-bind="forwardedProps"
    :class="cn('flex w-full items-center justify-between', props.class)"
  >
    <slot />
  </CalendarHeader>
</template>
