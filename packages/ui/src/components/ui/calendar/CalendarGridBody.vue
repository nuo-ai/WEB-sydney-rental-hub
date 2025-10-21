<script lang="ts" setup>
import type { CalendarGridBodyProps } from "reka-ui"
import { CalendarGridBody, useForwardProps } from "reka-ui"
import { cn } from "../../../lib/utils"

const props = defineProps<CalendarGridBodyProps>()
const forwardedProps = useForwardProps(props)
</script>

<template>
  <CalendarGridBody
    v-bind="forwardedProps"
    :class="cn('w-full', props.class)"
  >
    <slot />
  </CalendarGridBody>
</template>
