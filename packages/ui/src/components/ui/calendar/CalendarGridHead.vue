<script lang="ts" setup>
import type { CalendarGridHeadProps } from "reka-ui"
import { CalendarGridHead, useForwardProps } from "reka-ui"
import { cn } from "../../../lib/utils"

const props = defineProps<CalendarGridHeadProps>()
const forwardedProps = useForwardProps(props)
</script>

<template>
  <CalendarGridHead
    v-bind="forwardedProps"
    :class="cn('w-full', props.class)"
  >
    <slot />
  </CalendarGridHead>
</template>
