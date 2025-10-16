<script setup lang="ts">
/*
  文件职责：通用标签组选项（单选/多选）
  为什么：筛选面板内多处需要一致的选项组交互（价格段/出租方式/户型/配套）
  技术权衡：
  - 通过 mode 控制单/多选；不关心业务语义，仅发出变更
  - 选项为字符串数组，保持最小结构；后续若需要 value/label 可向上封装映射
*/

const props = withDefaults(defineProps<{
  // 展示文案项
  options: string[]
  // 单选或多选
  mode?: 'single' | 'multiple'
  // 选中值：single 模式下为 string|null；multiple 模式下为 string[]
  modelValue?: string | string[] | null
}>(), {
  options: () => [],
  mode: 'multiple',
  modelValue: null,
})

const emit = defineEmits<{
  (e: 'update:modelValue', value: string | string[] | null): void
}>()

function isSelected(opt: string) {
  if (props.mode === 'single') {
    return props.modelValue === opt
  }
  const arr = Array.isArray(props.modelValue) ? props.modelValue : []
  return arr.includes(opt)
}

function onToggle(opt: string) {
  if (props.mode === 'single') {
    // 单选：再次点击同一项可取消选择（回到 null）
    const next = props.modelValue === opt ? null : opt
    emit('update:modelValue', next)
    return
  }
  // 多选：集合增删
  const set = new Set(Array.isArray(props.modelValue) ? props.modelValue : [])
  if (set.has(opt)) set.delete(opt)
  else set.add(opt)
  emit('update:modelValue', Array.from(set))
}
</script>

<template>
  <div class="grid gap-3" :class="{'grid-cols-3': true}">
    <button
      v-for="opt in options"
      :key="opt"
      type="button"
      class="rounded-md border px-3 py-2 text-sm text-left transition-colors"
      :class="isSelected(opt)
        ? 'bg-teal-50 text-teal-600 border-teal-200'
        : 'bg-gray-50 text-gray-700 border-gray-200 hover:bg-gray-100'"
      @click="onToggle(opt)"
    >
      {{ opt }}
    </button>
  </div>
</template>
