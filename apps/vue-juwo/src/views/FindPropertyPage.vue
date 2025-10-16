<script setup lang="ts">
/*
  页面职责：找房页拼装（Header / 列表 / 三个 BottomSheet / 底部导航）
  为什么：将 demo.html 的交互与结构真正组合成 Vue 页，便于后续路由接入与数据对接
  技术权衡：
  - 使用本地 mock 数据渲染 PropertyList，不接真实 API
  - 三个弹层（位置/排序/筛选）受控打开/关闭，状态集中在本页
  - 底部导航仅切换 active 态（后续可接 vue-router），当前保持在“找房”
*/

import { ref, computed } from 'vue'
import type { Property, FilterState, TabKey } from '@/types/ui'
import AppHeader from '@/components/organisms/AppHeader.vue'
import PropertyList from '@/components/organisms/PropertyList.vue'
import LocationFilterModal from '@/components/organisms/LocationFilterModal.vue'
import SortModal from '@/components/organisms/SortModal.vue'
import FilterModal from '@/components/organisms/FilterModal.vue'
import BottomTabBar from '@/components/organisms/BottomTabBar.vue'
import { isRangeSelected } from '@/utils/ui'

// 底部导航当前 Tab（默认找房）
const activeTab = ref<TabKey>('find')

// 三个弹层开关
const locationOpen = ref(false)
const sortOpen = ref(false)
const filterOpen = ref(false)

function openLocation() { locationOpen.value = true }
function openSort() { sortOpen.value = true }
function openFilter() { filterOpen.value = true }

// 位置筛选：已选地区
const selectedDistricts = ref<string[]>([])

// 排序：默认“最新上架”
const sortValue = ref<string>('最新上架')

// 综合筛选状态（最小闭环）
const filterState = ref<FilterState>({
  price: { min: undefined, max: undefined },
  rentTypes: [],
  bedrooms: [],
  amenities: [],
})

// Header 三按钮的“高亮”判定：有条件时高亮
const locationActive = computed(() => selectedDistricts.value.length > 0)
const sortActive = computed(() => sortValue.value !== '最新上架')
const filterActive = computed(() => {
  const p: any = filterState.value.price
  const hasCustom = typeof p?.min === 'number' || typeof p?.max === 'number'
  const hasRange = isRangeSelected(filterState.value)
  const hasOther =
    filterState.value.rentTypes.length > 0 ||
    filterState.value.bedrooms.length > 0 ||
    filterState.value.amenities.length > 0
  return hasCustom || hasRange || hasOther
})

// demo.html 的地区清单（含“--热”标记以支持热门）
const sydneyDistricts = [
  'Alexandria', 'Ashfield', 'Barangaroo', 'Beaconsfield', 'Bondi', 'Bondi Junction', 'Burwood--热', 'Camperdown',
  'Campsie', 'Carlingford', 'Centennial Park', 'Chatswood', 'Chippendale--热', 'Coogee', 'Darlinghurst', 'Darlington',
  'Dawes Point', 'Double Bay', 'Eastgardens', 'Eastlakes', 'Eastwood', 'Elizabeth Bay', 'Epping', 'Erskineville',
  'Forest Lodge', 'Gladesville', 'Glebe', 'Haymarket--热', 'Hurstville', 'Kensington--热', 'Kingsford', 'Lane Cove',
  'Macquarie Park--热', 'Maroubra', 'Marrickville', 'Marsfield', 'Mascot--热', 'Meadowbank', 'Millers Point', 'Mosman',
  'Newtown', 'North Rocks', 'North Ryde', 'Paddington', 'Parramatta', 'Petersham', 'Potts Point', 'Pyrmont', 'Randwick',
  'Redfern', 'Rhodes', 'Rockdale', 'Rosebery--热', 'Ryde', 'St Leonards', 'Stanmore', 'Surry Hills', 'Sydney--热',
  'Sydney Olympic Park', 'The Rocks', 'Ultimo--热', 'Waterloo--热', 'Wolli Creek--热', 'Woolloomooloo', 'Zetland--热'
]

// 列表数据（mock — 摘自 demo.html）
const properties = ref<Property[]>([
  {
    id: 'p1',
    imageUrl: 'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?q=80&w=2070&auto-format&fit=crop',
    price: 500,
    period: '每周',
    address: '5/37 South Parade,\nCAMPSIE NSW 2194',
    beds: 2,
    baths: 1,
    cars: 1,
    availableText: '立即入住',
    favorited: false,
  },
  {
    id: 'p2',
    imageUrl: 'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?q=80&w=2070&auto=format&fit=crop',
    price: 850,
    period: '每周',
    address: '12A Pitt Street,\nSYDNEY NSW 2000',
    beds: 3,
    baths: 2,
    cars: 1,
    availableText: '11月1日',
    favorited: false,
  },
])

// 收藏/更多占位交互
function onToggleFavorite(id: string, next: boolean) {
  const i = properties.value.findIndex(p => p.id === id)
  if (i >= 0) {
    const current = properties.value[i]!
    properties.value[i] = { ...current, favorited: next }
  }
}
function onMoreActions(id: string) {
  // TODO: 打开操作菜单（分享/举报 等）；当前仅 console 占位
  console.debug('more-actions for', id)
}

// 底部 Tab 切换：当前仅切换激活态；页面还是 Find，自行根据项目路由接入
function onTabChange(tab: TabKey) {
  activeTab.value = tab
  // TODO: 接入 vue-router 后，跳转到对应视图
}
</script>

<template>
  <div class="min-h-screen bg-white">
    <!-- 顶部 Header -->
    <AppHeader
      city="上海"
      :location-active="locationActive"
      :sort-active="sortActive"
      :filter-active="filterActive"
      @open:location="openLocation"
      @open:sort="openSort"
      @open:filter="openFilter"
    />

    <!-- 内容（可滚动） -->
    <main class="mx-auto w-full max-w-[420px] px-4 py-3">
      <PropertyList
        :items="properties"
        @toggle-favorite="onToggleFavorite"
        @more-actions="onMoreActions"
      />
      <!-- 避免被底部导航遮挡的安全区 -->
      <div class="h-20"></div>
    </main>

    <!-- 位置筛选 -->
    <LocationFilterModal
      v-model:open="locationOpen"
      :districts="sydneyDistricts"
      v-model="selectedDistricts"
      :height="0.75"
      @confirm="() => { locationOpen = false }"
      @clear="() => {}"
    />
    <!-- 排序 -->
    <SortModal
      v-model:open="sortOpen"
      v-model="sortValue"
      :options="['最新上架', '最新发布', '离我最近']"
    />
    <!-- 综合筛选 -->
    <FilterModal
      v-model:open="filterOpen"
      v-model="filterState"
      @apply="() => { filterOpen = false }"
      @clear="() => {}"
    />

    <!-- 底部导航 -->
    <BottomTabBar :active="activeTab" @change="onTabChange" />
  </div>
</template>
