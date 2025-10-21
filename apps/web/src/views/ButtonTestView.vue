<template>
  <div class="container mx-auto py-8">
    <div class="mb-8">
      <button @click="$router.back()" class="mb-4 text-blue-600 hover:text-blue-800">
        ← 返回
      </button>
      <h1 class="text-3xl font-bold">BaseButton 组件测试</h1>
      <p class="text-gray-600">测试所有变体、尺寸和状态</p>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <!-- 基础变体测试 -->
      <div class="border rounded-lg p-6">
        <h2 class="text-xl font-semibold mb-4">基础变体</h2>
        <div class="flex flex-wrap gap-3">
          <BaseButton variant="primary">Primary</BaseButton>
          <BaseButton variant="secondary">Secondary</BaseButton>
          <BaseButton variant="ghost">Ghost</BaseButton>
          <BaseButton variant="link">Link</BaseButton>
        </div>
      </div>

      <!-- 尺寸测试 -->
      <div class="border rounded-lg p-6">
        <h2 class="text-xl font-semibold mb-4">尺寸</h2>
        <div class="flex flex-wrap items-center gap-3">
          <BaseButton size="small">Small</BaseButton>
          <BaseButton size="medium">Medium</BaseButton>
          <BaseButton size="large">Large</BaseButton>
        </div>
      </div>

      <!-- 状态测试 -->
      <div class="border rounded-lg p-6">
        <h2 class="text-xl font-semibold mb-4">状态</h2>
        <div class="flex flex-wrap gap-3">
          <BaseButton :loading="true">Loading</BaseButton>
          <BaseButton :disabled="true">Disabled</BaseButton>
          <BaseButton :block="true">Block Button</BaseButton>
        </div>
      </div>

      <!-- 图标测试 -->
      <div class="border rounded-lg p-6">
        <h2 class="text-xl font-semibold mb-4">图标</h2>
        <div class="flex flex-wrap gap-3">
          <BaseButton>
            <template #icon>
              <Plus class="w-4 h-4" />
            </template>
            前置图标
          </BaseButton>
          <BaseButton>
            后置图标
            <template #iconRight>
              <ArrowRight class="w-4 h-4" />
            </template>
          </BaseButton>
        </div>
      </div>

      <!-- 交互测试 -->
      <div class="border rounded-lg p-6">
        <h2 class="text-xl font-semibold mb-4">交互测试</h2>
        <div class="space-y-4">
          <BaseButton @click="handleClick" variant="primary">
            点击测试 (已点击: {{ clickCount }} 次)
          </BaseButton>
          <BaseButton @click="toggleLoading" :loading="isLoading">
            {{ isLoading ? '加载中...' : '切换加载状态' }}
          </BaseButton>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Plus, ArrowRight } from 'lucide-vue-next'
import { BaseButton } from '@sydney-rental-hub/ui'

const clickCount = ref(0)
const isLoading = ref(false)

const handleClick = () => {
  clickCount.value++
  console.log('Button clicked!')
}

const toggleLoading = () => {
  isLoading.value = !isLoading.value
}
</script>
