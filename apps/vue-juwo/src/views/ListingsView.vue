<script setup lang="ts">
import { RouterLink } from 'vue-router'
import Card from '@/components/ui/Card.vue'
import CardHeader from '@/components/ui/CardHeader.vue'
import CardTitle from '@/components/ui/CardTitle.vue'
import CardDescription from '@/components/ui/CardDescription.vue'
import CardContent from '@/components/ui/CardContent.vue'
</script>

<template>
  <main class="min-h-dvh bg-white text-gray-900">
    <header class="px-4 py-3 border-b">
      <h1 class="text-lg font-semibold">房源列表（占位）</h1>
    </header>

    <section class="p-4 space-y-4">
      <Card>
        <CardHeader>
          <CardTitle>示例房源 #1</CardTitle>
          <CardDescription>Sydney CBD · 2室1厅 · $550/周</CardDescription>
        </CardHeader>
        <CardContent>
          <p class="text-sm text-gray-600">
            这里将展示通过 /api/properties 获取的房源数据。当前为占位页面，用于验证"品牌欢迎页 → 进入列表页"的核心流程。
          </p>
        </CardContent>
      </Card>
      
      <Card>
        <CardHeader>
          <CardTitle>示例房源 #2</CardTitle>
          <CardDescription>Chatswood · 1室1厅 · $480/周</CardDescription>
        </CardHeader>
        <CardContent>
          <p class="text-sm text-gray-600">
            现代化装修，靠近火车站，交通便利。
          </p>
        </CardContent>
      </Card>
      
      <RouterLink
        to="/"
        class="inline-flex h-10 items-center justify-center rounded-md border px-4 text-sm font-medium hover:bg-gray-50 active:scale-[0.99] transition"
        aria-label="返回品牌页"
      >
        返回品牌页
      </RouterLink>
    </section>
  </main>
</template>

<style scoped></style>
