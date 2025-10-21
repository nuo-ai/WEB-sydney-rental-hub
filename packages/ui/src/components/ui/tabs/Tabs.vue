<script setup lang="ts">
import type { HTMLAttributes } from "vue"
import { provide, computed } from "vue"
import { useVModel } from "@vueuse/core"
import { cn } from "../../../lib/utils"

/**
 * 纯 Vue Tabs 实现，避免 reka-ui 依赖；API 对齐 shadcn：
 * - 组件：Tabs / TabsList / TabsTrigger / TabsContent
 * - 状态：v-model（受控）或 defaultValue（非受控初始）
 * - 数据属性：data-state="active|inactive" 供样式控制
 */
const props = withDefaults(defineProps<{
  modelValue?: string | null
  defaultValue?: string | null
  class?: HTMLAttributes["class"]
}>(), {
  defaultValue: null,
})

const emit = defineEmits<{
  (e: "update:modelValue", value: string | null): void
  (e: "change", value: string | null): void
}>()

// 统一为受控/非受控；默认值回落 defaultValue
const valueRef = useVModel(props, "modelValue", emit, {
  passive: true,
  defaultValue: props.defaultValue ?? null,
})

function setValue(v: string | null) {
  if (valueRef.value === v) return
  valueRef.value = v
  emit("change", v)
}

const ctx = {
  valueRef,
  setValue,
}

provide("srh-tabs-ctx", ctx)

const rootClass = computed(() =>
  cn("grid", props.class),
)
</script>

<template>
  <div :class="rootClass">
    <slot />
  </div>
</template>
