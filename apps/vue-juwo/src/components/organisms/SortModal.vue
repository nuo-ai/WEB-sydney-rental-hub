<script setup lang="ts">
/*
  文件职责：排序选择弹层（底部弹出），支持单选与“默认排序”恢复
  为什么：与 Header 解耦，页面层负责持久化当前排序；该组件仅处理 UI 与选择事件
  业务规则：
  - 选项为单选；点击即选中并关闭弹层
  - “默认排序”按钮将选中第一个选项（options[0]）
  - 遮罩点击关闭（由通用 BottomSheet 处理）
*/

import { computed, withDefaults } from 'vue'
import BottomSheet from './BottomSheet.vue'

const props = withDefaults(defineProps<{
  open?: boolean
  options?: string[]
  modelValue?: string
  height?: number
}>(), {
  open: false,
  options: () => ['最新上架', '最新发布', '离我最近'],
  modelValue: undefined,
  height: 0.45,
})

const emit = defineEmits<{
  (e: 'update:open', value: boolean): void
  (e: 'update:modelValue', value: string): void
  (e: 'close'): void
}>()

// 当前选中值：若外部未传，默认首项（仅用于渲染高亮，不修改父值）
const current = computed(() => {
  return props.modelValue ?? props.options[0]
})

function choose(val: string) {
  emit('update:modelValue', val)
  emit('update:open', false)
}

function resetDefault() {
  if (props.options.length > 0) {
    emit('update:modelValue', props.options[0])
  }
}

function onClose() {
  emit('update:open', false)
  emit('close')
}
</script>

<template>
  <BottomSheet
    :open="open"
    :height="height"
    :show-header="true"
    :show-footer="false"
    @update:open="val => emit('update:open', val)"
    @close="onClose"
  >
    <template #title>
      <div class="flex items-center justify-between">
        <span class="text-base text-gray-900">选择排序方式：</span>
        <button
          type="button"
          class="text-sm text-gray-500 hover:text-gray-800"
          @click="resetDefault"
        >
          默认排序
        </button>
      </div>
    </template>

    <div class="py-1">
      <ul class="divide-y divide-gray-100">
        <li
          v-for="opt in options"
          :key="opt"
          class="px-4 py-3 cursor-pointer transition-colors"
          :class="opt === current ? 'text-teal-600' : 'text-gray-900 hover:bg-gray-50'"
          @click="choose(opt)"
        >
          <div class="flex items-center justify-between">
            <span>{{ opt }}</span>
            <span
              class="ml-2 inline-flex h-5 w-5 items-center justify-center rounded text-sm"
              :class="opt === current ? 'text-teal-600' : 'text-transparent'"
              aria-hidden="true"
            >
              ✓
            </span>
          </div>
        </li>
      </ul>
    </div>
  </BottomSheet>
</template>
