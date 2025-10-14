<template>
  <div class="container py-6">
    <h1 class="text-xl font-semibold mb-4 text-foreground">房源卡片 · 主题变量联动演示</h1>
    <p class="text-sm text-foreground mb-6">
      说明：以下为两张演示用房源卡片（假数据）。已接入 theme.css 的核心变量与 Tailwind 样式；明/暗切换将联动背景/边框/主色/焦点环。
    </p>

    <div class="flex flex-col gap-6 items-start">
      <PropertyCard
        v-for="p in demoProperties"
        :key="p.listing_id"
        :property="p"
        @click="onCardClick"
        @contact="onContact"
      />
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { usePropertiesStore } from '@/stores/properties'
import PropertyCard from '../components/PropertyCard.vue'

/* 演示用假数据（覆盖 PropertyCard 使用到的字段） */
const router = useRouter()
const propertiesStore = usePropertiesStore()

const demoProperties = [
  {
    listing_id: 3001,
    images: [
      'https://images.unsplash.com/photo-1501183638710-841dd1904471?q=80&w=1200&auto=format&fit=crop',
      'https://images.unsplash.com/photo-1502003148287-a82ef80a6abc?q=80&w=1200&auto=format&fit=crop',
    ],
    rent_pw: 920,
    address: '12 George St, Zetland',
    suburb: 'Zetland',
    postcode: '2017',
    bedrooms: 2,
    bathrooms: 2,
    parking_spaces: 1,
    available_date: '2025-10-20',
    inspection_times: 'Saturday 11:30am - 12:00pm',
  },
  {
    listing_id: 3002,
    images: [
      'https://images.unsplash.com/photo-1505691938895-1758d7feb511?q=80&w=1200&auto=format&fit=crop',
    ],
    rent_pw: 780,
    address: '88 Bourke St, Surry Hills',
    suburb: 'Surry Hills',
    postcode: '2010',
    bedrooms: 1,
    bathrooms: 1,
    parking_spaces: 0,
    available_date: '2025-11-01',
    inspection_times: 'Sunday 1:15pm - 1:45pm',
  },
]

/* 事件处理（简单提示） */
function onCardClick(property) {
  // 先把当前房源写入 store，再跳转到详情页，避免直接刷新的 404
  if (property) {
    propertiesStore.currentProperty = property
  }
  if (property?.listing_id) {
    router.push({ name: 'PropertyDetail', params: { id: property.listing_id } })
  }
}

function onContact(property) {
  console.log('联系房东：', property?.address || property?.listing_id)
}
</script>

<style scoped>
/* 可按需加入局部样式，这里留空 */
</style>
