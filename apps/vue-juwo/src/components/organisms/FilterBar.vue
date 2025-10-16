<script setup lang="ts">
/*
  文件职责：顶部筛选栏，包含“位置 / 排序 / 筛选”三个入口按钮
  为什么：三入口是找房页的核心操作，统一封装便于各页复用与样式一致
  技术权衡：
  - 仅负责发出打开事件（open:location/sort/filter），不持久化业务状态
  - active 态通过 props 控制，父组件根据当前筛选条件决定是否高亮
*/

import FilterButton from '../molecules/FilterButton.vue'

const props = withDefaults(defineProps<{
  locationActive?: boolean
  sortActive?: boolean
  filterActive?: boolean
}>(), {
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
  <div class="flex items-center justify-around gap-2 py-1">
    <FilterButton
      label="位置"
      :active="props.locationActive"
      @click="openLocation"
    >
      <!-- 可选图标插槽
      <template #icon>
        <span class="i-lucide-map-pin h-4 w-4"></span>
      </template> -->
    </FilterButton>

    <FilterButton
      label="排序"
      :active="props.sortActive"
      @click="openSort"
    >
      <!-- <template #icon><span class="i-lucide-arrow-up-down h-4 w-4"></span></template> -->
    </FilterButton>

    <FilterButton
      label="筛选"
      :active="props.filterActive"
      @click="openFilter"
    >
      <!-- <template #icon><span class="i-lucide-sliders-horizontal h-4 w-4"></span></template> -->
    </FilterButton>
  </div>
</template>
