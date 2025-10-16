<script setup lang="ts">
/*
  文件职责：数字输入的轻量封装（用于价格自定义输入）
  为什么：统一样式与可访问性，避免各处重复 class/校验
  技术权衡：
  - 原生 input[type=number]，不引入第三方库，最小依赖
  - 仅透传常用属性，父层负责更复杂的校验/格式化
*/

const props = withDefaults(defineProps<{
  modelValue?: number | null
  placeholder?: string
  min?: number
  max?: number
  step?: number
  disabled?: boolean
  inputClass?: string
}>(), {
  modelValue: null,
  placeholder: '',
  min: undefined,
  max: undefined,
  step: 1,
  disabled: false,
  inputClass: '',
})

const emit = defineEmits<{
  (e: 'update:modelValue', value: number | null): void
  (e: 'change', value: number | null): void
}>()

function onInput(e: Event) {
  const target = e.target as HTMLInputElement
  const val = target.value === '' ? null : Number(target.value)
  if (val !== null && Number.isNaN(val)) {
    emit('update:modelValue', null)
    emit('change', null)
    return
  }
  emit('update:modelValue', val)
}

function onChange(e: Event) {
  const target = e.target as HTMLInputElement
  const val = target.value === '' ? null : Number(target.value)
  if (val !== null && Number.isNaN(val)) {
    emit('change', null)
    return
  }
  emit('change', val)
}
</script>

<template>
  <input
    type="number"
    :value="modelValue ?? ''"
    :placeholder="placeholder"
    :min="min"
    :max="max"
    :step="step"
    :disabled="disabled"
    @input="onInput"
    @change="onChange"
    class="w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm text-gray-900 placeholder:text-gray-400
           focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-teal-500 disabled:cursor-not-allowed disabled:opacity-50
           [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
    :class="inputClass"
  />
</template>
