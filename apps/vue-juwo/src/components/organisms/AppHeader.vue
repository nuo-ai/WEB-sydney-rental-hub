<script setup lang="ts">
/*
  文件职责：找房页顶部 Header，包括城市展示与三大筛选入口（位置/排序/筛选）
  为什么：Header 是用户进入找房页的首层交互，统一封装便于各页复用与样式一致
  技术权衡：
  - 仅发出打开弹层事件（open:location/sort/filter），不持久化业务状态
  - 城市展示作为文案 props 注入，后续可接入定位/城市选择
*/

import { withDefaults } from 'vue'
import FilterBar from './FilterBar.vue'

const props = withDefaults(defineProps<{
  city: string
  locationActive?: boolean
  sortActive?: boolean
  filterActive?: boolean
}>(), {
  city: '上海',
  locationActive: false,
  sortActive: false,
  filterActive: false,
})

const emit = defineEmits<{
  (e: 'open:location'): void
  (e: 'open:sort'): void
  (e: 'open:filter'): void
}>()

function openLocation() { emit('open:location') }
function openSort() { emit('open:sort') }
function openFilter() { emit('open:filter') }
</script>

<template>
  <header class="bg-white border-b border-gray-200 px-4 pt-2 pb-2">
    <!-- 顶栏：城市/位置入口（预留图标位，当前仅文案） -->
    <div class="flex items-center justify-between mb-2">
      <button
        type="button"
        class="inline-flex items-center gap-1.5 text-base font-medium text-gray-900"
        @click="openLocation"
        aria-label="选择位置"
      >
        <!-- 预留图标位：后续可用 lucide-vue-next MapPin 图标 -->
        <!-- <span class="i-lucide-map-pin h-5 w-5 text-gray-600"></span> -->
        <span>{{ props.city }}</span>
      </button>

      <!-- 右侧预留区域：后续可放消息/搜索等入口 -->
      <slot name="actions" />
    </div>

    <!-- 筛选三按钮 -->
    <FilterBar
      :location-active="props.locationActive"
      :sort-active="props.sortActive"
      :filter-active="props.filterActive"
      @open:location="openLocation"
      @open:sort="openSort"
      @open:filter="openFilter"
    />
  </header>
</template>
