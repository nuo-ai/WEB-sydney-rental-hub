<script setup lang="ts">
/*
  文件职责：单个房源卡片（图片/价格/收藏/地址/规格/可入住）
  为什么：复用性强，列表/收藏页/推荐位等均可使用
  业务规则：
  - 收藏为本地切换态，同时向上 emit('toggle-favorite', id) 便于父级持久化
  - “更多”按钮预留 emit('more-actions', id)
  - 图片宽度自适应，16:9 容器裁切；无图兜底背景
*/

import { ref, watch } from 'vue'
import type { Property } from '@/types/ui'
import PriceBar from '../molecules/PriceBar.vue'
import SpecsList from '../molecules/SpecsList.vue'

const props = defineProps<{
  property: Property
}>()

const emit = defineEmits<{
  (e: 'toggle-favorite', id: string, next: boolean): void
  (e: 'more-actions', id: string): void
}>()

// 本地收藏态（初始取自 props）
const favorited = ref<boolean>(props.property.favorited ?? false)
watch(
  () => props.property.favorited,
  (v) => { favorited.value = !!v },
)

function onToggleFavorite() {
  favorited.value = !favorited.value
  emit('toggle-favorite', props.property.id, favorited.value)
}

function onMore() {
  emit('more-actions', props.property.id)
}
</script>

<template>
  <article class="rounded-lg bg-white shadow-sm overflow-hidden border border-gray-100">
    <!-- 图片区域（16:9 容器） -->
    <div class="relative w-full">
      <div class="w-full" style="aspect-ratio: 16 / 9;">
        <img
          v-if="property.imageUrl"
          class="h-full w-full object-cover"
          :src="property.imageUrl"
          alt="房源图片"
          loading="lazy"
          referrerpolicy="no-referrer"
        />
        <div v-else class="h-full w-full bg-gray-100 flex items-center justify-center text-gray-400 text-sm">
          无图片
        </div>
      </div>
    </div>

    <!-- 内容 -->
    <div class="p-4">
      <!-- 价格 + 操作 -->
      <div class="mb-2 flex items-center justify-between">
        <PriceBar :price="property.price" :period="property.period" />
        <div class="flex items-center gap-3 text-gray-500">
          <!-- 收藏按钮 -->
          <button
            type="button"
            class="text-lg leading-none hover:text-teal-600"
            :aria-pressed="favorited ? 'true' : 'false'"
            @click="onToggleFavorite"
            aria-label="收藏"
            title="收藏"
          >
            {{ favorited ? '★' : '☆' }}
          </button>
          <!-- 更多按钮 -->
          <button
            type="button"
            class="text-lg leading-none hover:text-gray-700"
            @click="onMore"
            aria-label="更多"
            title="更多"
          >
            ⋯
          </button>
        </div>
      </div>

      <!-- 地址（允许换行） -->
      <p class="mb-4 text-[15px] leading-snug text-gray-800 whitespace-pre-line">
        {{ property.address }}
      </p>

      <!-- 规格三元组 -->
      <div class="mb-4">
        <SpecsList :beds="property.beds" :baths="property.baths" :cars="property.cars" />
      </div>

      <!-- 可入住文案 -->
      <p class="text-sm text-gray-700">
        <span class="text-gray-500">空出日期:</span>
        <span class="ml-1">{{ property.availableText }}</span>
      </p>
    </div>
  </article>
</template>
