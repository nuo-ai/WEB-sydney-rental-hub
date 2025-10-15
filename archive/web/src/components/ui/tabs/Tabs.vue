<script setup lang="ts">
import { provide, ref, watch, toRef } from 'vue'

export type TabsValue = string

const props = defineProps<{
  modelValue?: TabsValue
  defaultValue?: TabsValue
}>();

const emit = defineEmits<{
  (e: 'update:modelValue', v: TabsValue): void
}>();

// 当前选中的标签值（受控/非受控）
const inner = ref<TabsValue | undefined>(props.modelValue ?? props.defaultValue)
watch(() => props.modelValue, (v) => {
  if (v !== undefined) inner.value = v
})

function setValue(v: TabsValue) {
  inner.value = v
  emit('update:modelValue', v)
}

// 在子组件中通过 inject 使用
provide('tabs.value', inner)
provide('tabs.setValue', setValue)
</script>

<template>
  <div class="w-full">
    <slot />
  </div>
</template>
