<script setup lang="ts">
/*
  文件职责：房源卡片列表渲染容器
  为什么：列表/搜索结果页会复用该容器，统一间距与事件冒泡
  技术权衡：
  - 不持本地状态；仅将子项事件冒泡到父层（toggle-favorite/more-actions）
  - 样式保持最小（竖向间距），页面自行决定外层留白与滚动
*/

import type { Property } from '@/types/ui'
import PropertyCard from './PropertyCard.vue'

const props = defineProps<{
  items: Property[]
}>()

const emit = defineEmits<{
  (e: 'toggle-favorite', id: string, next: boolean): void
  (e: 'more-actions', id: string): void
}>()

function onToggleFavorite(id: string, next: boolean) {
  emit('toggle-favorite', id, next)
}

function onMore(id: string) {
  emit('more-actions', id)
}
</script>

<template>
  <div class="space-y-5">
    <PropertyCard
      v-for="item in items"
      :key="item.id"
      :property="item"
      @toggle-favorite="onToggleFavorite"
      @more-actions="onMore"
    />
  </div>
</template>
