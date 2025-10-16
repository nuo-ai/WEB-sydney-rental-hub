<script setup lang="ts">
/*
  文件职责：价格段 + 自定义价格输入的小节
  为什么：筛选面板的核心联动区域；选中价格段→填充输入框；手动输入→清空价格段
  技术权衡：
  - 不直接持久化整体 FilterState，仅通过 props/emits 向父层同步
  - 价格段以 label 作为“rangeKey”（由父层决定 label 与业务 key 的映射是否相同）
*/

import BaseInputNumber from '../base/BaseInputNumber.vue'
import TagGroup from './TagGroup.vue'
import type { PriceRange } from '@/types/ui'

const props = withDefaults(defineProps<{
  // 价格段配置
  ranges: PriceRange[]
  // 当前选中的段位（使用 label 作为 key）
  modelValue?: string | null
  // 展示在输入框中的数值（可由父层派生自 rangeKey）
  min?: number | null
  max?: number | null
}>(), {
  ranges: () => [],
  modelValue: null,
  min: null,
  max: null,
})

const emit = defineEmits<{
  // 段位选择变更：若选择某一段，父层应设置 price 为 { rangeKey }; 若取消，则可置 null
  (e: 'update:modelValue', value: string | null): void
  // 自定义输入变更：父层应将 price 置为 { min, max } 并清空 rangeKey
  (e: 'update:min', value: number | null): void
  (e: 'update:max', value: number | null): void
}>()

function onSelectRange(val: string | string[] | null) {
  const next = Array.isArray(val) ? val[0] ?? null : val
  // 选择段位时，父层将据此设置 price = { rangeKey: val }；本组件不直接改 min/max（可由父层派生）
  emit('update:modelValue', next)
}

function onMinChange(v: number | null) {
  emit('update:min', v)
  // 手输即清空段位
  emit('update:modelValue', null)
}

function onMaxChange(v: number | null) {
  emit('update:max', v)
  // 手输即清空段位
  emit('update:modelValue', null)
}
</script>

<template>
  <section class="space-y-3">
    <h3 class="text-sm font-medium text-gray-900">租金 (AUD/周)</h3>

    <!-- 段位（单选） -->
    <TagGroup
      :options="ranges.map(r => r.label)"
      mode="single"
      :model-value="modelValue"
      @update:modelValue="onSelectRange"
    />

    <!-- 自定义输入（手输则清空段位） -->
    <div class="grid grid-cols-[1fr_auto_1fr] items-center gap-2">
      <BaseInputNumber
        :model-value="min ?? null"
        placeholder="最低"
        @change="onMinChange"
      />
      <span class="text-gray-500">-</span>
      <BaseInputNumber
        :model-value="max ?? null"
        placeholder="最高"
        @change="onMaxChange"
      />
    </div>
  </section>
</template>
