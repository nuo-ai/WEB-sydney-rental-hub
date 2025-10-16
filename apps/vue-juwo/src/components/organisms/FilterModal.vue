<script setup lang="ts">
/*
  文件职责：综合筛选弹层（底部弹出）：价格段/自定义价格、出租方式、户型、配套
  为什么：将 demo.html 的筛选逻辑组件化；与 Header/页面解耦，便于复用
  业务规则：
  - 价格段与自定义输入互斥：选择段位→输入框显示对应范围；手动输入→清空段位
  - 清除：还原为空（不选段位、无自定义输入、其它组清空）
  - 确定：emit('apply', FilterState) 并关闭；父层负责持久化与触发列表刷新
*/

import { computed, withDefaults } from 'vue'
import BottomSheet from './BottomSheet.vue'
import TagGroup from '../molecules/TagGroup.vue'
import PriceRangeSection from '../molecules/PriceRangeSection.vue'
import type { FilterState, PriceRange } from '@/types/ui'
import { isRangeSelected } from '@/utils/ui'

const props = withDefaults(defineProps<{
  open?: boolean
  // 价格段配置（用于“价格段”单选组）
  priceRanges?: PriceRange[]
  // v-model：完整筛选状态
  modelValue: FilterState
  // 可配置的标签组选项（若不传则使用默认）
  rentTypeOptions?: string[]
  bedroomOptions?: string[]
  amenityOptions?: string[]
  // 弹层高度（默认 0.85）
  height?: number
}>(), {
  open: false,
  priceRanges: () => ([
    { label: '500 以下', max: 500 },
    { label: '500-1000', min: 500, max: 1000 },
    { label: '1000-1500', min: 1000, max: 1500 },
    { label: '1500-2000', min: 1500, max: 2000 },
    { label: '2000-2500', min: 2000, max: 2500 },
    { label: '2500 以上', min: 2500 },
  ]),
  rentTypeOptions: () => (['整租', '合租']),
  bedroomOptions: () => (['1室', '2室', '3室', '4室', '5室及以上']),
  amenityOptions: () => (['带家具']),
  height: 0.85,
})

const emit = defineEmits<{
  (e: 'update:open', value: boolean): void
  (e: 'update:modelValue', value: FilterState): void
  (e: 'apply', value: FilterState): void
  (e: 'clear'): void
  (e: 'close'): void
}>()

// 辅助：安全读取当前 price 模式
const priceIsRange = computed(() => isRangeSelected(props.modelValue))

// 当前选中的“段位 key”（以 label 作为 key）
const selectedRangeKey = computed<string | null>(() => {
  return priceIsRange.value ? (props.modelValue.price as any)?.rangeKey ?? null : null
})

// 派生输入框的 min/max：
// - 若为段位模式 → 使用配置 ranges 中该 label 对应的 min/max
// - 若为自定义输入 → 读取 modelValue.price 的 min/max
const derivedMin = computed<number | null>(() => {
  if (priceIsRange.value) {
    const key = selectedRangeKey.value
    const found = props.priceRanges.find(r => r.label === key)
    if (!found) return null
    return typeof found.min === 'number' ? found.min : null
  }
  const p = props.modelValue.price as any
  return typeof p?.min === 'number' ? p.min : null
})

const derivedMax = computed<number | null>(() => {
  if (priceIsRange.value) {
    const key = selectedRangeKey.value
    const found = props.priceRanges.find(r => r.label === key)
    if (!found) return null
    return typeof found.max === 'number' ? found.max : null
  }
  const p = props.modelValue.price as any
  return typeof p?.max === 'number' ? p.max : null
})

// 更新整体状态的帮助函数（不可变更新）
function patch(patchFn: (prev: FilterState) => FilterState) {
  const next = patchFn(props.modelValue)
  emit('update:modelValue', next)
}

// 价格段选择变化：设置为段位模式（rangeKey = label）
function onRangeKeyChange(label: string | null) {
  patch(prev => {
    const next: FilterState = {
      ...prev,
      price: label ? { rangeKey: label } : { min: (prev as any)?.price?.min ?? undefined, max: (prev as any)?.price?.max ?? undefined },
    }
    return next
  })
}

// 自定义输入变化：切换为自定义模式并清空段位
function onMinChange(min: number | null) {
  patch(prev => ({
    ...prev,
    price: { min: min ?? undefined, max: (prev as any)?.price?.max ?? undefined },
  }))
}
function onMaxChange(max: number | null) {
  patch(prev => ({
    ...prev,
    price: { min: (prev as any)?.price?.min ?? undefined, max: max ?? undefined },
  }))
}

// 其它标签组变化
function onRentTypesChange(v: string[] | string | null) {
  patch(prev => ({ ...prev, rentTypes: Array.isArray(v) ? v : (v ? [v] : []) }))
}
function onBedroomsChange(v: string[] | string | null) {
  patch(prev => ({ ...prev, bedrooms: Array.isArray(v) ? v : (v ? [v] : []) }))
}
function onAmenitiesChange(v: string[] | string | null) {
  patch(prev => ({ ...prev, amenities: Array.isArray(v) ? v : (v ? [v] : []) }))
}

function clearAll() {
  const cleared: FilterState = {
    price: { min: undefined, max: undefined },
    rentTypes: [],
    bedrooms: [],
    amenities: [],
  }
  emit('update:modelValue', cleared)
  emit('clear')
}

function applyAndClose() {
  emit('apply', props.modelValue)
  emit('update:open', false)
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
    :show-footer="true"
    @update:open="val => emit('update:open', val)"
    @close="onClose"
  >
    <template #title>
      <div class="flex items-center justify-between">
        <span class="text-base text-gray-900">筛选条件：</span>
        <button
          type="button"
          class="text-sm text-gray-500 hover:text-gray-800"
          @click="clearAll"
        >
          清除条件
        </button>
      </div>
    </template>

    <div class="space-y-6">
      <!-- 价格 -->
      <PriceRangeSection
        :ranges="priceRanges"
        :model-value="selectedRangeKey"
        :min="derivedMin"
        :max="derivedMax"
        @update:modelValue="onRangeKeyChange"
        @update:min="onMinChange"
        @update:max="onMaxChange"
      />

      <!-- 出租方式（多选） -->
      <section class="space-y-3">
        <h3 class="text-sm font-medium text-gray-900">出租方式</h3>
        <TagGroup
          :options="rentTypeOptions"
          mode="multiple"
          :model-value="modelValue.rentTypes"
          @update:modelValue="onRentTypesChange"
        />
      </section>

      <!-- 户型（多选） -->
      <section class="space-y-3">
        <h3 class="text-sm font-medium text-gray-900">户型</h3>
        <TagGroup
          :options="bedroomOptions"
          mode="multiple"
          :model-value="modelValue.bedrooms"
          @update:modelValue="onBedroomsChange"
        />
      </section>

      <!-- 配套（多选） -->
      <section class="space-y-3">
        <h3 class="text-sm font-medium text-gray-900">配套设施</h3>
        <TagGroup
          :options="amenityOptions"
          mode="multiple"
          :model-value="modelValue.amenities"
          @update:modelValue="onAmenitiesChange"
        />
      </section>
    </div>

    <template #footer>
      <button
        type="button"
        class="w-full rounded-md bg-teal-500 px-4 py-3 text-white font-semibold hover:bg-teal-600 active:bg-teal-700"
        @click="applyAndClose"
      >
        确定
      </button>
    </template>
  </BottomSheet>
</template>
