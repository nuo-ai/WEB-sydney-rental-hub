<script setup lang="ts">
import type { HTMLAttributes } from "vue"
import { computed } from "vue"
import { useVModel } from "@vueuse/core"
import { cn } from "../../../lib/utils"

// 采用纯 Vue 日期选择器库，完全规避 reka-ui 与 React 依赖
// 说明：该封装提供最小 API（v-model + mode + class）
// - mode: 'single' | 'range'，用于切换单选/区间
// - v-model: Date | [Date, Date] | null
// - class: 自定义样式类名（沿用项目的 cn + tokens）
// TODO: 如有进一步交互/样式对齐需求，再在 design system 层逐步增强
import VueDatePicker from "@vuepic/vue-datepicker"
import "@vuepic/vue-datepicker/dist/main.css"

const props = withDefaults(
  defineProps<{
    modelValue?: Date | [Date, Date] | null
    mode?: "single" | "range"
    class?: HTMLAttributes["class"]
  }>(),
  {
    mode: "single",
  },
)

const emit = defineEmits<{
  (e: "update:modelValue", value: Date | [Date, Date] | null): void
}>()

// 与 v-model 双向绑定
const value = useVModel(props, "modelValue", emit)

// 是否区间模式
const isRange = computed(() => props.mode === "range")
</script>

<template>
  <div data-slot="calendar" :class="cn('p-3', props.class)">
    <VueDatePicker
      v-model="value"
      :range="isRange"
      :enable-time-picker="false"
      :teleport="true"
      :auto-apply="true"
      :popover="{ visibility: 'click' }"
      :clearable="true"
      :hide-input-icon="true"
      :month-change-on-scroll="false"
      :state="undefined"
      :flow="['calendar']"
      :focus-start-date="true"
      :transition="'fade'"
    />
  </div>
</template>
