<script setup lang="ts">
/*
  文件职责：位置筛选弹层（底部弹出），包含：已选标签、热门、A-Z 分组、右侧索引、清除/确定
  为什么：将 demo.html 的位置筛选逻辑组件化，统一交互与样式，便于复用与扩展
  业务规则：
  - 热门与分组双向联动；点击右侧索引滚动到对应字母分组
  - Badge 显示选中数量（0 时隐藏）；清除按钮清空；确定回传选中并关闭
  - v-model：由父组件持久化 selected 列表；本组件不复制本地状态，保持单一数据源
*/

import { computed } from 'vue'
import BottomSheet from './BottomSheet.vue'
import SelectedTags from './SelectedTags.vue'
import DistrictPanels from './DistrictPanels.vue'
import AlphabetIndex from './AlphabetIndex.vue'
import { groupDistricts } from '@/utils/ui'

const props = withDefaults(defineProps<{
  // 受控开关
  open?: boolean
  // 原始地区列表（可能包含 “--热” 标记）
  districts?: string[]
  // 显式热门列表（可选；若不传则从 districts 中的 “--热” 提取）
  hot?: string[]
  // v-model：已选地区
  modelValue: string[]
  // 弹层高度（默认 0.75）
  height?: number
}>(), {
  open: false,
  districts: () => [],
  hot: undefined,
  modelValue: () => [],
  height: 0.75,
})

const emit = defineEmits<{
  (e: 'update:open', value: boolean): void
  (e: 'update:modelValue', value: string[]): void
  (e: 'confirm', value: string[]): void
  (e: 'clear'): void
  (e: 'close'): void
}>()

// 解析热门（优先用 props.hot；否则从 '--热' 标记提取）与去标记后的完整列表
const normalizedAll = computed(() => {
  return (props.districts || []).map((d) => (d || '').replace('--热', '').trim()).filter(Boolean)
})

const derivedHot = computed<string[]>(() => {
  if (Array.isArray(props.hot) && props.hot.length > 0) return props.hot
  // 从原始 districts 中带标记的项提取热门
  const raw = props.districts || []
  return raw.filter((d) => d.includes('--热')).map((d) => d.replace('--热', '').trim())
})

// 分组（A-Z / 其它归入 '#'）
const groups = computed(() => groupDistricts(normalizedAll.value))

// 右侧索引字母（仅 A-Z，不包含 '#'）
const letters = computed(() => Object.keys(groups.value).filter((k) => /^[A-Z]$/.test(k)).sort())

// 选中数量
const selectedCount = computed(() => props.modelValue?.length || 0)

function updateSelected(next: string[]) {
  emit('update:modelValue', next)
}

function clearAll() {
  emit('update:modelValue', [])
  emit('clear')
}

function confirm() {
  emit('confirm', props.modelValue || [])
  emit('update:open', false)
}

function handleClose() {
  emit('update:open', false)
  emit('close')
}

// 右侧索引跳转：使用锚点 scrollIntoView，滚动由最近滚动容器处理（BottomSheet 内容区）
function onJump(letter: string) {
  const id = `district-group-${letter}`
  const el = document.getElementById(id)
  if (el && typeof el.scrollIntoView === 'function') {
    try {
      el.scrollIntoView({ behavior: 'smooth', block: 'start' })
    } catch {
      el.scrollIntoView()
    }
  }
}

function removeTag(name: string) {
  const set = new Set(props.modelValue || [])
  set.delete(name)
  updateSelected(Array.from(set))
}
</script>

<template>
  <BottomSheet
    :open="open"
    :height="height"
    :show-header="true"
    :show-footer="true"
    @update:open="val => emit('update:open', val)"
    @close="handleClose"
  >
    <template #title>
      <div class="flex items-center justify-between">
        <span class="text-base text-gray-900">
          按照位置搜索：
          <span
            v-if="selectedCount > 0"
            class="ml-2 inline-flex items-center rounded-full bg-teal-500 px-2 py-0.5 text-xs font-medium text-white"
          >
            {{ selectedCount }}
          </span>
        </span>
        <button
          type="button"
          class="text-sm text-gray-500 hover:text-gray-800"
          @click="clearAll"
        >
          清除条件
        </button>
      </div>
    </template>

    <!-- 已选标签（无选择时默认隐藏） -->
    <SelectedTags :selected="modelValue" @remove="removeTag" />

    <!-- 左侧面板 + 右侧索引（相对定位） -->
    <div class="relative">
      <!-- 左侧分组/热门 -->
      <DistrictPanels
        :groups="groups"
        :hot="derivedHot"
        :model-value="modelValue"
        @update:modelValue="updateSelected"
      />
      <!-- 右侧 A-Z 索引 -->
      <div class="absolute right-1 top-1/2 -translate-y-1/2">
        <AlphabetIndex :letters="letters" @jump="onJump" />
      </div>
    </div>

    <template #footer>
      <button
        type="button"
        class="w-full rounded-md bg-teal-500 px-4 py-3 text-white font-semibold hover:bg-teal-600 active:bg-teal-700"
        @click="confirm"
      >
        确定
      </button>
    </template>
  </BottomSheet>
</template>
